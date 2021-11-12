from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Quizz_project_app.models import Images, Answers
from django import forms


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']


class QuizzMicroscopy(forms.Form):
	choices = []
	answer = Answers.objects.filter(q_id=1)

	for i in answer.all():
		choices.append((i.answer, i.answer))

	firstQuestion = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
	secondQuestion = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
	thirdQuestion = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
	fourthQuestion = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
	fifthQuestion = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)

class SearchBar(forms.Form):
    searchBar = forms.CharField(max_length=200)


class SearchBarList(forms.Form):
	columnNames = [field.name for field in Images._meta.get_fields()]
	choices = []
	choices.append(("", ""))
	for i in columnNames:
		choices.append((i, i))

	listbox = forms.CharField(widget=forms.Select(choices=choices))