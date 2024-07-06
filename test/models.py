from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Test(models.Model):
    name = models.CharField(max_length=100)
    time_for_pass = models.IntegerField()
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=100)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Result(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    progress = models.FloatField()
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)


class Answer(models.Model):
    name = models.CharField(max_length=100)
    correct = models.BooleanField()
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
