from django.db import models

class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class Test(models.Model):
    name = models.CharField(max_length=100)
    time_for_pass = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)

class Question(models.Model):
    name = models.CharField(max_length=100)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    progress = models.FloatField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

class Answer(models.Model):
    name = models.CharField(max_length=100)
    correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
