from django.shortcuts import render, get_object_or_404
from .models import Test
from .forms import TestForm
from django.shortcuts import redirect


def test_list(request):
    tests = Test
    return render(request, 'test/test_list.html', {"tests": tests})


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


def passing_the_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    return render(request, 'test/passing_the_test.html', {'test': test})


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

def my_tests(request):
    #me = User.objects.get(username=)
    test = Test#.objects.filter(author=me)
    return render(request, 'test/my_tests.html', {'test': test})

def passed_tests(request):
    test = Test#.objects.filter(passed=True)
    return render(request, 'test/passed_tests.html', {'test': test})

def FAQ(request):
    return render(request, 'test/FAQ.html', {})