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


        list_images = []
        used_images = []
        #génère liste de réponses correcpondant à q_id 1
        microscopy_answer = [x.answer for x in Answers.objects.filter(q_id=1).all()]
        images = list(Images.objects.filter(img_mode__in=microscopy_answer).all())


        ## For each question
        for items in listItems:

            ## We take images whose the microscopy type corresponds to our microscopy answer
            ## We choose a picture randomly in the databaseAnd we add it to the dictionnary_images and
            ## to the used images

            random_choice = random.choice(images)
            img_name = str(random_choice.img_name)
            file_ext = ".jpg"
            filepath = path_img + img_name + file_ext
            list_images.append({'id': random_choice.id, 'filepath': filepath})
            used_images.append(random_choice.id)
            images.remove(random_choice)

        request.session['choiceQuestion'] = question.quest_type
        request.session['question'] = question.quest
        request.session['images'] = list_images

        return render(request, "Quizz/Quizz_microscopy.html",
                      {'choiceQuestion': request.session.get('choiceQuestion'),
                       'question': request.session.get('question'), 'form': QuizzMicro.form,
                       'images': request.session.get('images'),
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
            list_description=[]
            images_iter = iter(request.session['images'])

            for answer in list_answers:
                question = Question.objects.filter(quest_id=1)
                image = Images.objects.filter(id=next(images_iter)['id']).first()
                point_val = question.values('quest_point').first()['quest_point']

                if answer == image.img_mode:
                    list_quest_to_answer.append("True")
                    points_gained += point_val

                else:
                    list_quest_to_answer.append("False")

                list_correction.append(image.img_mode)
                list_description.append(image.img_description)

            user_id = User.objects.get(id=request.user.id)
            profile_obj = Profile.objects.get(user_id=user_id)
            profile_obj.score = profile_obj.score + points_gained
            profile_obj.save()

            request.session['list_quest_to_answer'] = list_quest_to_answer
            request.session['list_correction'] = list_correction
            request.session['list_description'] = list_description

            print(list_answers)
            print(list_correction)
            print(points_gained)
            print(list_quest_to_answer)

            return redirect('microscopy_correction')

        else:
            print(form.errors)

def microscopy_correction(request):

    user_id = User.objects.get(id=request.user.id)
    score = Profile.objects.get(user_id=user_id)
    score = score.score

    return render(request, "Quizz/microscopy_correction.html",
        {'images': request.session.get('images'),
        'list_quest_to_answer': request.session.get('list_quest_to_answer'),
         'list_correction': request.session.get('list_correction'),
         'list_description':request.session.get('list_description'),
         'list_choices': [('fluorescence microscopy', 0),  ('scanning electron microscopy (SEM)', 1),
          ('transmission electron microscopy (TEM)', 2), ('phase contrast microscopy', 3)],
          'list_answers': request.session.get('list_answers'),'score': score})



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
