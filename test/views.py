from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Test, Result, Answer, Question, Choice
from .forms import LoginForm, RegisterForm, TestForm
from django.shortcuts import redirect

@login_required
def main_page(request):
    category_id = request.GET.get('category_id')
    if not category_id or not category_id.isdigit():
        tests = Test.objects.all()
    else:
        tests = Test.objects.filter(category_id=int(category_id))
    return render(request, 'test/main_page.html', {"tests": tests})

@login_required
def my_tests(request):
    user = request.user  # Получаем текущего пользователя
    tests = Test.objects.filter(author_id=user)  # Фильтруем тесты по автору
    category_id = request.GET.get('category_id')
    if category_id and category_id.isdigit():
        tests = tests.filter(category_id_id=int(category_id))
    return render(request, 'test/my_tests.html', {'tests': tests})

@login_required
def passed_tests(request):
    user_id = request.user.id
    category_id = request.GET.get('category_id')
    results = Result.objects.filter(user_id=user_id)
    test_ids = results.values_list('test_id', flat=True)
    tests = Test.objects.filter(id__in=test_ids)
    if category_id and category_id.isdigit():
        tests = tests.filter(category__id=int(category_id))
    return render(request, 'test/passed_tests.html', {'tests': tests})


@login_required
def passing_the_test(request, id):
    test = get_object_or_404(Test, id=id)
    questions = test.question_set.all()

    # Проверяем, есть ли уже результат для этого пользователя и теста
    try:
        result = Result.objects.get(user=request.user, test=test)
        user_answers = result.choice_set.all()
    except Result.DoesNotExist:
        result = None
        user_answers = []

    if request.method == 'POST':
        # Обработка данных формы
        user_answers = []
        for question in test.question_set.all():
            selected_answer = request.POST.get(f'answer_{question.id}')
            if selected_answer:
                user_answers.append(int(selected_answer))

        # Обновляем результаты
        if result:
            result.choice_set.set(user_answers)
            result.save()
        else:
            result = Result.objects.create(user=request.user, test=test, choice_set=user_answers)

        # Перенаправляем на страницу результатов
        return redirect('/test/<int:test_id>/results/', test_id=test.id)

    context = {
        'test': test,
        'questions': questions,
        'user_answers': user_answers,
        'result': result
    }
    return render(request, 'test/passing_the_test.html', context)




@login_required
def FAQ(request):
    return render(request, 'test/FAQ.html')


@login_required
def create_test(request):
    if request.method == 'POST':
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            test = test_form.save(commit=False)
            test.author = request.user
            test.save()

            # Получаем данные для вопросов и ответов из POST запроса
            for i in range(1, 51):  # Максимум 50 вопросов
                question_name = request.POST.get(f'question_{i}_name')
                if question_name:
                    question = Question.objects.create(
                        name=question_name,
                        test=test
                    )
                    for j in range(1, 7):  # Максимум 6 ответов на вопрос
                        answer_name = request.POST.get(f'question_{i}_answer_{j}_name')
                        if answer_name:
                            Answer.objects.create(
                                name=answer_name,
                                correct=request.POST.get(f'question_{i}_answer_{j}_is_correct') == 'on',
                                question=question
                            )

            return redirect('/test/my_tests/')
    else:
        test_form = TestForm()

    return render(request, 'test/create_test.html', {'test_form': test_form})



#@login_required
# def test_edit(request, test_id):
#     test = get_object_or_404(Test, pk=test_id)
#
#     if request.method == 'POST':
#         test_form = TestForm(request.POST, instance=test)
#         if test_form.is_valid():
#             test = test_form.save(commit=False)
#             if not (1 <= test.time_for_pass <= 60):
#                 return HttpResponseBadRequest("Time for pass must be between 1 and 60 minutes.")
#             test.save()
#
#             time_for_pass = request.POST.get('time_for_pass') # нужно время добавить
#
#
#             # Обработка вопросов и ответов
#             questions = request.POST.getlist('questions[]')
#             answers = request.POST.getlist('answers[]')
#             correct_answers = request.POST.getlist('correct[]')
#             question_ids = request.POST.getlist('question_ids[]')
#
#             # Обновляем или создаем новые вопросы и ответы
#             for idx, question_text in enumerate(questions):
#                 if question_ids[idx]:
#                     question = Question.objects.get(pk=question_ids[idx])
#                     question.name = question_text
#                     question.save()
#                 else:
#                     question = Question.objects.create(name=question_text, test_id=test)
#
#                 answers_list = answers[idx]
#                 correct_list = correct_answers[idx]
#                 #проверку на то не больше ли уже 6 вопросов будет нужно написать
#                 # Обновляем или создаем новые ответы
#                 for answer_text in answers_list:
#                     answer_id = request.POST.get(f'answer_{question.id}_{answer_text}_id', None)
#                     if answer_id:
#                         answer = Answer.objects.get(pk=answer_id)
#                         answer.name = answer_text
#                         answer.correct = answer_text in correct_list
#                         answer.save()
#                     else:
#                         Answer.objects.create(name=answer_text, correct=(answer_text in correct_list), question_id=question)
#
#             return redirect('test_list')  # Замените 'test_list' на ваше актуальное имя URL для списка тестов
#
#     else:
#         test_form = TestForm(instance=test)
#
#     # Получаем все вопросы и ответы для текущего теста
#     questions = list(test.questions.all())
#     answers = {question.id: list(question.answers.all()) for question in questions}
#     question_forms = [QuestionForm(instance=question) for question in questions]
#     answer_forms = {question.id: [AnswerForm(instance=answer) for answer in answers[question.id]] for question in questions}
#
#     context = {
#         'test_form': test_form,
#         'question_forms': question_forms,
#         'answer_forms': answer_forms,
#         'test_id': test_id,
#     }
#
#     return render(request, 'test/edit_test.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('main_page')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                try:
                    user = User.objects.get(username=username)
                except:
                    messages.error(request, 'Такого пользователя нет в системе')
                user = authenticate(username=username, password=password)
                if user is not None :
                    login(request, user)
                    return redirect(request.GET['next'] if 'next' in request.GET else 'main_page')
                else:
                    form.add_error(None, 'Неверный логин или пароль')
                    return redirect('login')
        else:
            form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('main_page')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                messages.success(request,'Аккаунт успешно создан!')
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, user)
                return redirect('login')
            else:
                messages.error(request, "Во время регистрации возникла ошибка")
        else:
            form = RegisterForm()
        return render(request, 'test/register.html', {'form': form})



@login_required
def grade_question(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    # Проверяем, есть ли уже результат для этого пользователя и теста
    try:
        result = Result.objects.get(user=request.user, test=test)
    except Result.DoesNotExist:
        result = Result.objects.create(user=request.user, test=test)

    # Получаем выбранные ответы
    user_answers = []
    for question in test.question_set.all():
        selected_answer = request.POST.get(f'answer_{question.id}')
        if selected_answer:
            user_answers.append(int(selected_answer))

    # Обновляем результаты
    result.choice_set.set(user_answers)
    result.save()

    # Перенаправляем на страницу результатов
    return redirect('/test/<int:test_id>/results/', test_id=test_id)


@login_required
def test_results(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.question_set.all()
    results = Result.objects.filter(user=request.user,
        test=test).values()
    correct = results[0]['correct'] if results else 0
    context = {'test': test,
    'correct': correct,
    'number': len(questions)}
    return render(request,
        'test/results.html', context)


@login_required
def display_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    user = request.user

    # Проверяем, есть ли у пользователя результаты по этому тесту
    results = Result.objects.filter(user=user, test=test)

    if results.exists():
        # Если результаты есть, определяем последний пройденный вопрос
        last_question_id = results.latest('id').choice_set.latest('id').question_id
        return redirect(reverse('tests:display_question', kwargs={'test_id': test_id, 'question_id': last_question_id}))
    else:
        # Если результатов нет, начинаем с первого вопроса
        question = test.question_set.first()
        return redirect(reverse('tests:display_question', kwargs={'test_id': test_id, 'question_id': question.id}))


@login_required
def display_question(request, test_id, question_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.question_set.all()
    current_question = None
    next_question = None

    # Находим текущий вопрос и следующий
    for ind, question in enumerate(questions):
        if question.pk == question_id:
            current_question = question
            if ind != len(questions) - 1:
                next_question = questions[ind + 1]
            break  # Прерываем цикл, как только нашли нужный вопрос

    context = {
        'test': test,
        'question': current_question,
        'next_question': next_question
    }

    return render(request, 'test/display.html', context)




