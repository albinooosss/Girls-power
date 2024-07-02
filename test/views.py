from django.shortcuts import render
from .models import Test
from .forms import TestForm


def test_list(request):
    tests = Test
    return render(request, 'test/test_list.html', {"tests": tests})

def test_new(request):
    form = TestForm()
    return render(request, 'test/test_edit.html', {'form': form})


