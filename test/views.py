from django.shortcuts import render, get_object_or_404
from .models import Test
from .forms import TestForm


def test_list(request):
    tests = Test
    return render(request, 'test/test_list.html', {"tests": tests})

def create_test(request):
    form = TestForm()
    return render(request, 'test/create_test.html', {'form': form})

def passing_the_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    return render(request, 'test/passing_the_test.html', {'test': test})


