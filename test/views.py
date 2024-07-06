from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from .models import Test, Result, Answer, Question
from .forms import LoginForm, RegisterForm
from django.shortcuts import redirect


def main_page(request):
    category_id = request.GET.get('category_id')
    if not category_id or not category_id.isdigit():
        tests = Test.objects.all()
    else:
        tests = Test.objects.filter(category_id=int(category_id))
    return render(request, 'test/main_page.html', {"tests": tests})


def my_tests(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Перенаправляем на страницу входа, если пользователь не авторизован
    user = request.user  # Получаем текущего пользователя
    tests = Test.objects.filter(author=user)  # Фильтруем тесты по автору
    category_id = request.GET.get('category_id')
    if category_id and category_id.isdigit():
        tests = tests.filter(category_id=int(category_id))
    return render(request, 'test/my_tests.html', {'tests': tests})


def passed_tests(request):
    user_id = request.user.id
    category_id = request.GET.get('category_id')
    results = Result.objects.filter(user_id=user_id)
    test_ids = results.values_list('test_id', flat=True)
    tests = Test.objects.filter(id__in=test_ids)
    if category_id and category_id.isdigit():
        tests = tests.filter(category__id=int(category_id))
    return render(request, 'test/passed_tests.html', {'tests': tests})


def passing_the_test(request, id):
    test = get_object_or_404(Test, id=id)
    return render(request, 'test/passing_the_test.html', {'test': test})


def FAQ(request):
    return render(request, 'test/FAQ.html')


# def create_test(request):
#     if request.method == 'POST':
#         test_name = request.POST.get('name')
#         time_for_pass = request.POST.get('time_for_pass')
#         category = request.POST.get('category')
#         questions = request.POST.getlist('questions[]')
#         answers = request.POST.getlist('answers[]')
#         correct_answers = request.POST.getlist('correct[]')
#
#         if not (1 <= int(time_for_pass) <= 60):
#             return HttpResponseBadRequest("Time for pass must be between 1 and 60 minutes.")
#
#         test = Test.objects.create(name=test_name, time_for_pass=time_for_pass, category=category, author_id=request.user)
#
#         for question_text in questions:
#             question = Question.objects.create(name=question_text, test_id=test)
#             question_index = questions.index(question_text)
#             answers_list = answers[question_index]
#             correct_list = correct_answers[question_index]
#
#             for answer_text in answers_list:
#                 is_correct = answer_text in correct_list
#                 Answer.objects.create(name=answer_text, correct=is_correct, question_id=question)
#
#         return redirect('test_list')  # Replace 'test_list' with your actual URL name for test listing
#
#     return render(request, 'test/create_test.html')
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


def login(request):
    if request.method == 'POST':
        print("login")
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('main_page')
    else:
        form = LoginForm()
    return render(request, 'test/main_page.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, email=email, password=password)
            login(request, user)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
