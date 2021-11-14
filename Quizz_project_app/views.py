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
        user_id = User.objects.get(id=request.user.id)
        score = Profile.objects.get(user_id=user_id)
        score = score.score

        if (score == None):
            score = 0

        ## We extract the question concerning the microscopy
        question = Question.objects.get(quest_type='microscopy')

        # 5 questions
        listItems = range(0, 5)

        ## Creations a dictionnary to store the URLs per question

        dico_images_path = {}
        dico_images = {}
        used_images = []

        ## For each question
        for iterator in listItems:

            ## Initializing the list of URLs
            dico_images_path[iterator] = []

            microscopy = Answers.objects.filter(q_id=1)
            microscopy = microscopy.all()
            random_microscopy = random.choice(microscopy)
            microscopy = random_microscopy.answer

            ## Creating a dictionnary to store the images
            ## And a list to store already used images

            ## For the five picture

            for iterator2 in range(0, 1):

                ## If the dictionnary of images is empty
                if (dico_images == {}):

                    ## We take images whose the microscopy type corresponds to our microscopy answer
                    images = Images.objects.filter(img_mode=microscopy)
                    images = images.all()

                    ## We choose a picture randomly in the databaseAnd we add it to the dictionnary_images and
                    ## to the used images
                    random_choice = random.choice(images)

                    if random_choice.img_name in used_images:
                        random_choice = random.choice(images)
                        img_name = str(random_choice.img_name)
                        file_ext = ".jpg"
                        filepath = path_img + img_name + file_ext
                        dico_images[iterator2] = filepath
                        used_images.append(random_choice.img_name)

                    else:
                        img_name = str(random_choice.img_name)
                        file_ext = ".jpg"
                        filepath = path_img + img_name + file_ext
                        dico_images[iterator2] = filepath
                        used_images.append(random_choice.img_name)

                else:

                    ## If the dictionnary of images is not empty We take images whose the microscopy type
                    ## corresponds to our microscopy answerWe choose a picture randomly in the database

                    images = Images.objects.filter(img_mode=microscopy)
                    images = images.all()

                    random_choice = random.choice(images)

                    if random_choice.img_name in used_images:
                        random_choice = random.choice(images)
                        img_name = str(random_choice.img_name)
                        file_ext = ".jpg"
                        filepath = path_img + img_name + file_ext
                        dico_images[iterator2] = filepath
                        used_images.append(random_choice.img_name)

                    else:
                        img_name = str(random_choice.img_name)
                        file_ext = ".jpg"
                        filepath = path_img + img_name + file_ext
                        dico_images[iterator2] = filepath
                        used_images.append(random_choice.img_name)

            ## For all the elements in the dictionnary of pictures
            for iterator3 in dico_images:
                ## We replace all the spaces by plus sign to get the URL of the picture
                ## And we append the URL to the URL dictionnary

                dico_images_path[iterator].append(dico_images[iterator3])

        request.session['choiceQuestion'] = question.quest_type
        request.session['question'] = question.quest
        request.session['dico_images_path'] = dico_images_path

        return render(request, "Quizz/Quizz_microscopy.html",
                      {'choiceQuestion': request.session.get('choiceQuestion'),
                       'question': request.session.get('question'), 'form': QuizzMicro.form,
                       'dico_images_path': request.session.get('dico_images_path'),
                       'score': score})



    def post(self, request):



        form = QuizzMicro.form(request.POST)

        if (form.is_valid()):

            list_answers = [form.cleaned_data['firstQuestion'],
                            form.cleaned_data['secondQuestion'],
                            form.cleaned_data['thirdQuestion'],
                            form.cleaned_data['fourthQuestion'],
                            form.cleaned_data['fifthQuestion']
                            ]

            request.session['list_answers'] = list_answers

            points_gained = 0
            list_quest_to_answer=[]
            list_correction =[]

            for iterator4 in range(0, 5):

                point_val = Question.objects.filter(quest_id=1).values('quest_point')

                if (list_answers[iterator4] == Answers.answer):
                    list_quest_to_answer.append("True")
                    points_gained += point_val

                else:
                    list_quest_to_answer.append("False")

                list_correction.append(Answers.definition)
            print(Profile.score)
            print(list_quest_to_answer)
            print(list_correction)
            print(list_answers)

            user_id = User.objects.get(id=request.user.id)
            profile_obj = Profile.objects.get(user_id=user_id)
            profile_obj.score = profile_obj.score + points_gained
            profile_obj.save()

            request.session['list_quest_to_answer'] = list_quest_to_answer
            request.session['list_correction'] = list_correction

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
