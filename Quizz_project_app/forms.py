from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Quizz_project_app.models import Images, Answers
from django import forms

''' 
Class: SearchBar
This class allows to initialize the search bar
field in order to search images
'''
class SearchBar(forms.Form):
    searchBar = forms.CharField(max_length=200)


''' 
Class: SearchBarList
This class allows to initialize the list box in order to
select the item to allow autocompleting of the search bar 
and fill the choice list with elements refering to the selected item
'''
class SearchBarList(forms.Form):
	columnNames = [field.name for field in Images._meta.get_fields()]
	choices = []
	choices.append(("", ""))
	for i in columnNames:
		choices.append((i, i))

	listbox = forms.CharField(widget=forms.Select(choices=choices))

''' 
Class: CreateUserForm
This class allows to initialize form to register a new user
'''
class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']


''' 
Class: QuizzMicroscopy
This class allows to initialize form to Answer to the 
questions about microscopy
'''
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


''' 
Class: QuizzComponent
This class allows to initialize form to Answer to the 
questions about cellular component
'''
class QuizzComponent(forms.Form):
	choices = []
	answer = Answers.objects.filter(q_id=2)

	for j in answer.all():
		choices.append((j.answer, j.answer))

	firstQuestion = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
	secondQuestion = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
	thirdQuestion = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
	fourthQuestion = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
	fifthQuestion = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
