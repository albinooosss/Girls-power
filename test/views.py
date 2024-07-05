from django.shortcuts import render, get_object_or_404
from .models import Test, User, Result, Question
from .forms import TestForm
from django.shortcuts import redirect


def test_list(request):
    tests = Test.objects.all
    return render(request, 'test/main_page.html', {"tests": tests})


def category_list(request):
    categories = Test.category.objects.all  # ???
    return render(request, 'test/main_page.html', {"categories": categories})


def my_tests(request):
    #tests = Test.objects.filter(author_id=User.pk)
    return render(request, 'test/my_tests.html', '''{'tests': tests}''')



def passed_tests(request):
    results = Result.objects.filter(user_id=User.pk)
    tests = Test.objects.filter(pk=results.test_id)
    return render(request, 'test/passed_tests.html', {'tests': tests})



def show_result(request):
    all_questions_count = Question.objects.filter(
        test_id=Test.pk).count()  # так ли считается кол-во всем вопросов в тесте
    # correct_answered_questions_count = Question.objects. как посчитать на сколько вопросов пользователь ответил правильно
    result = Result.objects.filter(user_id=User.pk)  # нужно ли в бд поле progress?
    # return render(request, 'test/show_result_html', ('results': all_questions_count - correct_answered_questions_count))
    # узнать у насти правильное название html


def passing_the_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    return render(request, 'test/passing_the_test.html', {'test': test})


def create_test(request):
    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.author = request.user
            test.save()
            return redirect('passing_the_test', pk=test.pk)
    else:
        form = TestForm()
    return render(request, 'test/create_test.html', {'form': form})


def edit_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.method == "POST":
        form = TestForm(request.POST, instance=test)
        if form.is_valid():
            test = form.save(commit=False)
            test.author = request.user
            test.save()
            return redirect('post_detail', pk=test.pk)
    else:
        form = TestForm(instance=test)
    return render(request, 'test/edit_test.html', {'form': form})


def FAQ(request):
    return render(request, 'test/FAQ.html')
