from django import forms
from django.contrib.auth.models import User
from .models import Test, Question, Answer, Result

class LoginForm(forms.Form):
    email = forms.EmailField(label='email', max_length=100, required=True)
    password = forms.CharField(label='password', strip=True, widget=forms.PasswordInput, required=True)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']  # Включаем confirm_password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# class TestForm(forms.ModelForm):
#     class Meta:
#         model = Test
#         fields = ['id', 'name', 'time_for_pass', 'category']
#         widgets = {
#             'id': forms.HiddenInput(),  # Скрытое поле для хранения идентификатора теста
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'time_for_pass': forms.NumberInput(attrs={'class': 'form-control'}),
#             'category': forms.TextInput(attrs={'class': 'form-control'}),
#         }



# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['name', 'test']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'test': forms.Select(attrs={'class': 'form-control'}),
#         }
#
# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer
#         fields = ['name', 'correct', 'question']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'question': forms.Select(attrs={'class': 'form-control'}),
#         }
#
# class ResultForm(forms.ModelForm):
#     class Meta:
#         model = Result
#         fields = ['user', 'progress', 'test']
#         widgets = {
#             'user': forms.Select(attrs={'class': 'form-control'}),
#             'progress': forms.NumberInput(attrs={'class': 'form-control'}),
#             'test': forms.Select(attrs={'class': 'form-control'}),
#         }