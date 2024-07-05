from django.db import models

class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Test(models.Model):
    name = models.CharField(max_length=100)
    time_for_pass = models.IntegerField()
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)

    def publish(self):
        self.save()

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

    def __str__(self):
        return self.progress

class Answer(models.Model):
    name = models.CharField(max_length=100)
    correct = models.BooleanField()
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
