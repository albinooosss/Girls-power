from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from .models import Test, Result, Answer, Question, Category, Choice
from .forms import LoginForm, RegisterForm, TestForm
from django.views.generic import ListView



def categories_views(request, id):
    categories = Category.objects.all()
    tests = Test.objects.filter(category_id=id)
    # Получаем ID авторов тестов
    authors_ids = tests.values_list('author_id', flat=True)
    # Получаем объекты авторов
    users = User.objects.filter(id__in=authors_ids)

    return render(request, 'test/main_page.html', {'tests': tests, 'categories': categories, "users": users})

@login_required
def main_page(request):
    category_id = request.GET.get('category_id')
    categories = Category.objects.all()
    if not category_id or not category_id.isdigit():
        tests = Test.objects.all()
    else:
        tests = Test.objects.filter(category_id=int(category_id))

    # Получаем ID авторов тестов
    authors_ids = tests.values_list('author_id', flat=True)
    # Получаем объекты авторов
    users = User.objects.filter(id__in=authors_ids)

    context = {
        "tests": tests,
        "categories": categories,
        "users": users,
    }
    return render(request, 'test/main_page.html', context)

@login_required
def my_tests(request):
    category_id = request.GET.get('category_id')
    categories = Category.objects.all()
    if not category_id or not category_id.isdigit():
        tests = Test.objects.all()
    else:
        tests = Test.objects.filter(category_id=int(category_id))
    user = request.user  # Получаем текущего пользователя
    tests = tests.filter(author_id=user)  # Фильтруем тесты по автору
    # Получаем ID авторов тестов
    authors_ids = tests.values_list('author_id', flat=True)
    # Получаем объекты авторов
    users = User.objects.filter(id__in=authors_ids)
    context = {
        "tests": tests,
        "categories": categories,
        "users": users,
    }
    return render(request, 'test/my_tests.html', context)

@login_required
def passed_tests(request):
    category_id = request.GET.get('category_id')
    categories = Category.objects.all()
    if not category_id or not category_id.isdigit():
        tests = Test.objects.all()
        completed_tests = {test.id: Result.objects.filter(user=request.user, test=test, progress=100.0).exists() for
                           test in
                           tests}
    else:
        tests = Test.objects.filter(category_id=int(category_id))
        completed_tests = {test.id: Result.objects.filter(user=request.user, test=test, progress=100.0).exists() for
                           test in
                           tests}
    user = request.user  # Получаем текущего пользователя
    tests = tests.filter(author_id=user)  # Фильтруем тесты по автору
    # Получаем ID авторов тестов
    authors_ids = tests.values_list('author_id', flat=True)
    # Получаем объекты авторов
    users = User.objects.filter(id__in=authors_ids)
    context = {
        "completed_tests": completed_tests,
        "categories": categories,
        "users": users,
    }
    return render(request, 'test/my_tests.html', context)

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
                if user is not None:
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
                messages.success(request, 'Аккаунт успешно создан!')
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
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    return JsonResponse({'status': 'success'})


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


@login_required
def edit_test(request, id):
    test = get_object_or_404(Test, id=id)

    if request.method == 'POST':
        if 'delete_test' in request.POST:
            test.delete()
            return redirect('/test/my_tests/')

        test_form = TestForm(request.POST, instance=test)
        if test_form.is_valid():
            test = test_form.save(commit=False)
            test.author = request.user
            test.save()

            # Обновляем существующие вопросы и ответы
            for question in test.question_set.all():
                question_name = request.POST.get(f'question_{question.id}_name')
                if question_name:
                    question.name = question_name
                    question.save()

                    for answer in question.answer_set.all():
                        answer_name = request.POST.get(f'question_{question.id}_answer_{answer.id}_name')
                        if answer_name:
                            answer.name = answer_name
                            answer.correct = request.POST.get(f'question_{question.id}_answer_{answer.id}_is_correct') == 'on'
                            answer.save()
                        else:
                            answer.delete()
                else:
                    question.delete()

            # Добавляем новые вопросы и ответы
            for i in range(1, 51):  # Максимум 50 вопросов
                if not any(f'question_{question.id}_name' == f'question_{i}_name' for question in test.question_set.all()):
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
        test_form = TestForm(instance=test)

    return render(request, 'test/edit_test.html', {'test_form': test_form, 'test': test})




@login_required
def passing_the_test(request, id):
    test = get_object_or_404(Test, id=id)
    questions = test.question_set.all()

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
    result.progress.set(user_answers)
    result.save()

    # Перенаправляем на страницу результатов
    return redirect('/test/<int:test_id>/results/', test_id=test_id)


@login_required
def test_results(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.question_set.all()
    print(questions)
    user = request.user

    total_questions = questions.count()
    correct_answers = 0
    user_answers_arr = []
    for question in questions:
        selected_answer = request.POST.get(f'answer_{question.id}')
        print(selected_answer)
        # Choice.objects.create(user=user, question=question, answer_id=selected_answer)
        user_choices = Choice.objects.filter(user=user, question=question, answer=Answer.objects.get(id=selected_answer))
        if selected_answer:
            user_answers_arr.append(int(selected_answer))
        if user_choices.exists():
            print(user_choices)
            user_answer = user_choices.first().answer
            if user_answer.correct:
                correct_answers += 1

    percentage_correct = 0
    if total_questions > 0:
        percentage_correct = (correct_answers / total_questions) * 100

    Choice.objects.create(user=user, question=question, answer_id=selected_answer)
    Result.objects.create(user=user, progress=percentage_correct, test=test)

    context = {
        'test': test,
        'correct_answers': correct_answers,
        'total_questions': total_questions,
        'percentage_correct': percentage_correct
    }

    return render(request, 'test/results.html', context)


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

class TestSearchView(View):
    def get(self, request):
        query = request.GET.get('q')
        if query:
            tests = Test.objects.filter(name__icontains=query)
            users = User.objects.all()  # Получаем всех пользователей, если необходимо
        else:
            tests = Test.objects.none()
            users = User.objects.none()

        context = {
            'tests': tests,
            'users': users,
        }
        return render(request, 'test/search_results.html', context)



