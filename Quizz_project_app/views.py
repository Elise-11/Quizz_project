from django.shortcuts import render, redirect
from Quizz_project_app.forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Quizz_project_app.forms import SearchBar, SearchBarList, QuizzMicroscopy
from Quizz_project_app.models import Profile as profileUser
from Quizz_project_app.models import Images, Question, Answers, AnswerUser, Profile
from django.contrib.auth.models import User
import random
from django.views import View

#import hashlib


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created for ' + user.get_username())

            return redirect('login')

        else:
            messages.info(request, 'Your password must be more than 9 characters long,'
                                   ' must not be entirely numeric and must be different from your username !')

    context = {'form': form}
    return render(request, 'Registration/register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('choice')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'registration/login.html', context)

@login_required(login_url='login')
def choice(request):
    return render(request, 'choice.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def explo(request):
    return render(request, 'Exploration/searchBar.html')



path_img = "/static/Quizz_project_app/img/img_microscopy/"

class QuizzMicro(View):
    form = QuizzMicroscopy

    def get(self, request):
        #associate score to user_id logged
        user_id= User.objects.get(id=request.user.id)
        score = Profile.objects.get(user_id=user_id)
        score = score.score

        if (score == None):
            score = 0

        ## We extract the question concerning the microscopy
        question = Question.objects.get(quest_type='microscopy')

        ## For each quizz, 10 Questions
        listItems = range(0, 4)

        ## Creations a dictionnary to store the URLs per question

        dico_url = {}

        ## For each question
        for iterator in listItems:

            ## Initializing the list of URLs
            dico_url[iterator] = []

            microscopy = Answers.objects.filter(q_id=1)
            microscopy = microscopy.all()
            random_microscopy = random.choice(microscopy)
            microscopy = random_microscopy.answer

            ## Creating a dictionnary to store the images
            ## And a list to store already used images

            dico_images = {}
            used_images = []

            ## For the four pictures

            for iterator2 in range(0, 2):

                ## If the dictionnary of images is empty
                if (dico_images == {}):

                    ## We take images whose the microscopy type corresponds to our microscopy answer
                    images = Images.objects.filter(img_mode=microscopy)
                    images = images.all()

                    ## We choose a picture randomly in the databaseAnd we add it to the dictionnary_images and
                    ## to the used images

                    random_choice = random.choice(images)
                    img_name = str(random_choice.img_name)
                    file_ext = ".jpg"
                    filepath = path_img + img_name + file_ext
                    dico_images[iterator2] = filepath
                    used_images.append(filepath)

                else:

                    ## If the dictionnary of images is not empty We take images whose the microscopy type
                    ## corresponds to our microscopy answerWe choose a picture randomly in the database

                    images = Images.objects.filter(img_mode=microscopy)
                    images = images.all()
                    random_choice = random.choice(images)
                    img_name = str(random_choice.img_name)
                    file_ext = ".jpg"
                    filepath = path_img + img_name + file_ext

                    ## If the random picture corresponds to a already, used picture, so, While the picture corresponds
                    ## to a already used picture, we choose another picture

                    while (filepath in used_images):
                        random_choice = random.choice(images)
                        img_name = str(random_choice.img_name)
                        file_ext = ".jpg"
                        filepath = path_img + str(img_name) + file_ext


                    ## And then, we add it to the dictionnary of imagesand to the used images

                    dico_images[iterator2] = filepath
                    used_images.append(filepath)

            ## For all the elements in the dictionnary of pictures
            for iterator3 in dico_images:
                ## We replace all the spaces by plus sign to get the URL of the picture
                ## And we append the URL to the URL dictionnary

                dico_url[iterator].append(dico_images[iterator3])

        request.session['choiceQuestion'] = question.quest_type
        request.session['question'] = question.quest
        request.session['dico_url'] = dico_url

        return render(request, "Quizz/Quizz_microscopy.html",
                      {'choiceQuestion': request.session.get('choiceQuestion'),
                       'question': request.session.get('question'), 'form': QuizzMicro.form,
                       'dico_url': request.session.get('dico_url'),
                       'score': score})


    def post(self, request):

        user_id = User.objects.get(id=request.user.id)
        score = Profile.objects.get(user_id=user_id)
        score = score.score

        if (score == None):
            score = 0

        form = QuizzMicro.form(request.POST)

        if (form.is_valid()):

            list_answers = [form.cleaned_data['firstQuestion'],
                            form.cleaned_data['secondQuestion'],
                            form.cleaned_data['thirdQuestion'],
                            form.cleaned_data['fourthQuestion']
                            ]

            request.session['list_answers'] = list_answers

            list_answer_to_answer = []
            list_description_answer = []

            gainedScore = 0

            for iterator4 in range(0, 4):
                user = User.objects.get(username="{}".format(request.user.username))

                usernameComposed = request.user.username + "_{}".format(
                    request.session['userGameActive']) + "_{}".format(iterator4)
                userAnswer = AnswerUser.objects.get(user_question=usernameComposed)

                answers = Answers.objects.get(answer_id=userAnswer.goodAnswerId)

                score = Question.objects.get(question_id=1)

                if (list_answers[iterator4] == answers.answer):
                    list_answer_to_answer.append("TrueQuestion")
                    gainedScore += score.points


                else:
                    list_answer_to_answer.append("FalseQuestion")

                list_description_answer.append(answers.definition)

            Profile.score += gainedScore
            Profile.save()
            request.session['gainedScore'] = gainedScore

            request.session['list_answer_to_answer'] = list_answer_to_answer
            request.session['list_description_answer'] = list_description_answer

            return redirect('explo')

        else:
            print(form.errors)


def searchBarExplo(request, ):
    if (request.method == "POST"):
        form = SearchBar(request.POST)
        formsearchBar = SearchBarList(request.POST)

        score = profileUser.objects.get(username=request.user.username)
        score = score.score

        if (score == None):
            score = 0

        if (form.is_valid()):
            request.session['feature'] = form.cleaned_data['searchBar']
            return redirect('searchResults')

    else:
        form = SearchBar
        formsearchBar = SearchBarList
        score = profileUser.objects.get(username=request.user.username)
        score = score.score

        if (score == None):
            score = 0

    return render(request, 'Exploration/searchBar.html',
                  {'form': form, 'formsearchBar': formsearchBar, 'score': score})


def searchResults(request, ):
    score = profileUser.objects.get(username=request.user.username)
    score = score.score

    if (score == None):
        score = 0

    category = request.session['category']
    feature = request.session['feature']

    images = Images.objects.filter(**{category: feature}).all()
    dictionnaryImages = {}
    counter = 0


    for i in images:
        dictionnaryImages[counter] = []
        dictionnaryImages[counter].append(i.img_name)
        dictionnaryImages[counter].append(i.img_description)
        dictionnaryImages[counter].append(i.img_mode)
        dictionnaryImages[counter].append(i.img_cell_type)
        dictionnaryImages[counter].append(i.img_component)
        dictionnaryImages[counter].append(i.img_doi)
        dictionnaryImages[counter].append(i.img_organism)
        counter += 1

    return render(request, 'ImagesSearchBar/searchResults.html',
                  {'dictionnaryImages': dictionnaryImages, 'score': score})
