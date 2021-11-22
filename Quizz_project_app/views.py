from django.shortcuts import render, redirect
from Quizz_project_app.forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Quizz_project_app.forms import SearchBar, SearchBarList, QuizzMicroscopy, QuizzComponent
from Quizz_project_app.models import Profile as profileUser
from Quizz_project_app.models import Images, Question, Answers, Profile
from django.contrib.auth.models import User
import random
from django.views import View

''' 
function:register
This function is used when a user registers, it redirects the 
user to the login page if they have correctly filled in the form, 
otherwise it displays an error message. 
'''

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

''' 
function:login_user
This function is used when a user log in, it redirects the 
user to the home page called choice where the user can 
choose to play a quizz or explore data when he correctly 
filled in the form.
'''
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

''' 
function:choice
This function is used to direct to the home page path
containing the user score 
'''
@login_required(login_url='login')
def choice(request):
    user_id = User.objects.get(id=request.user.id)
    score = Profile.objects.get(user_id=user_id)
    score = score.score

    return render(request, 'choice.html', {'score':score})


''' 
function:logoutUser
This function is used to direct to the login page path
'''
def logoutUser(request):
    logout(request)
    return redirect('login')


#path to images directory
path_img = "/static/Quizz_project_app/img/img_microscopy/"

''' 
function: explo
This function is used to display elements needed to
the exploration page path et redirect to page containing 
the result of the search
'''
@login_required(login_url='login')
def explo(request):
    form = SearchBar(request.POST)
    form_searchBar = SearchBarList(request.POST)

    #if the search bar is filled it redirects the user to the corresponding result page
    if (form.is_valid()):
        request.session['feature'] = form.cleaned_data['searchBar']
        return redirect('exploResults')

    return render(request, 'Exploration/searchBar.html',
                  {'form': form, 'formsearchBar': form_searchBar})


''' 
function : autocompletion
autocomplete the search bar according to selected item 
among the Images attributes thanks to library ajax from jquery 
'''
def autocompletion(request):
    #category correspond to the selected item in the listbox (script in searchBar.html)
    if (request.is_ajax and request.method == 'POST'):
        category = request.POST['category']
        request.session['category'] = category
        images = Images.objects.values(category)
        images_values = []

        #store the Image values in the selected category in a new list
        for i in range(0, len(images)):
            images_values.append(str(images[i][category]))

        #display the list in a listbox when the user write in the search bar
        images_values = list(dict.fromkeys(images_values))
        return JsonResponse(images_values, safe=False)

'''
function : exploResult 
This function allows to return elements corresponding to 
the search to another page, the exploration result page.
for each result corresponding to the search a key is created with
an associated list containing all the attribute of the searched image.
'''
def exploResults(request, ):
    category = request.session['category']
    feature = request.session['feature']

    images = Images.objects.filter(**{category: feature}).all()
    dicoImages = {}
    counter = 0

    for i in images:
        img_name = str(i.img_name)
        img_src = path_img + img_name + ".jpg"
        dicoImages[counter] = []
        dicoImages[counter].append(img_src)
        dicoImages[counter].append(i.img_description)
        dicoImages[counter].append(i.img_mode)
        dicoImages[counter].append(i.img_cell_type)
        dicoImages[counter].append(i.img_component)
        dicoImages[counter].append(i.img_doi)
        dicoImages[counter].append(i.img_organism)
        counter += 1

    return render(request, 'Exploration/searchResults.html',
                  {'dicoImages': dicoImages})


'''
Class QuizzMicro
class to store methods concerning the microscopy quizz
'''
class QuizzMicro(View):
    form = QuizzMicroscopy

    '''
    method : get
    This method allows to display quizz microscopy elements 
    and especially the random selection of microscopy images
    '''
    def get(self, request):
        #associate score to user_id logged
        user_id = User.objects.get(id=request.user.id)
        score = Profile.objects.get(user_id=user_id)
        score = score.score

        if (score == None):
            score = 0

        # Retrieve the question concerning the microscopy
        question = Question.objects.get(quest_type='microscopy')

        # 5 questions
        listItems = range(0, 5)
        # this list store a dictionary containing image id and image path
        list_images = []
        # this list store image id used
        used_images = []

        # Generate a list of images related to answers corresponding to a q_id=1 (microscopy)
        microscopy_answer = [x.answer for x in Answers.objects.filter(q_id=1).all()]
        images = list(Images.objects.filter(img_mode__in=microscopy_answer).all())

        # for each question
        for items in listItems:

            # Select an image randomly and extract its name
            # construct a filepath : path of the selected image and store it
            # store image id in used_images list
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

        #return the elements to display in the html page
        return render(request, "Quizz/Quizz_microscopy.html",
                      {'choiceQuestion': request.session.get('choiceQuestion'),
                       'question': request.session.get('question'), 'form': QuizzMicro.form,
                       'images': request.session.get('images'),
                       'score': score})

    '''
    method : post
    This method allows to retrieve the user's answers, compare them to 
    real good answers, attribute corresponding points won to user score
    and redirect to correction page
    '''
    def post(self, request):

        form = QuizzMicro.form(request.POST)

        # retrieve answers in a list only if the user has chosen at least one answer for each question
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

            # compare user's answers and correction answers in list_correction
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

            #add the points won to the user score and save it
            user_id = User.objects.get(id=request.user.id)
            profile_obj = Profile.objects.get(user_id=user_id)
            profile_obj.score = profile_obj.score + points_gained
            profile_obj.save()

            request.session['list_quest_to_answer'] = list_quest_to_answer
            request.session['list_correction'] = list_correction
            request.session['list_description'] = list_description

            # redirect to correction page
            return redirect('microscopy_correction')

        else:
            print(form.errors)


'''
function : microscopy_correction 
This function allows to display correction of the answers corresponding to the images
and the new user score
'''
def microscopy_correction(request):

    user_id = User.objects.get(id=request.user.id)
    score = Profile.objects.get(user_id=user_id)
    score = score.score

    #return the elements to display in the html page
    return render(request, "Quizz/microscopy_correction.html",
        {'images': request.session.get('images'),
        'list_quest_to_answer': request.session.get('list_quest_to_answer'),
         'list_correction': request.session.get('list_correction'),
         'list_description':request.session.get('list_description'),
         'list_choices': [('fluorescence microscopy', 0),  ('scanning electron microscopy (SEM)', 1),
          ('transmission electron microscopy (TEM)', 2), ('phase contrast microscopy', 3)],
          'list_answers': request.session.get('list_answers'),'score': score})


'''
Class QuizzMicro
class to store methods concerning the component quizz
'''
path_img = "/static/Quizz_project_app/img/img_microscopy/"

class QuizzCompo(View):

    form = QuizzComponent

    def get(self, request):
        #associate score to user_id logged
        user_id = User.objects.get(id=request.user.id)
        score = Profile.objects.get(user_id=user_id)
        score = score.score

        if (score == None):
            score = 0

        # Retrieve the question concerning the microscopy
        question = Question.objects.get(quest_type='component')

        # 5 questions
        listItems = range(0,5)
        # this list store a dictionary containing image component and image path
        list_images = []
        # this list store image id used
        used_images = []
        #list to store a dictionnary containing image id
        list_id=[]

        # Generate a list of images related to answers corresponding to a q_id=1 (microscopy)
        component_answer = [y.answer for y in Answers.objects.filter(q_id=2).all()]

        images = list(Images.objects.filter(img_component__in=component_answer).all())
        print(images)


        # for each question
        for items in listItems:
                list_img_choices = []
                # Select an image randomly and extract its name
                # construct a filepath : path of the selected image and store it
                # store image id in used_images list
                random_choice = random.choice(images)
                img_name = str(random_choice.img_name)
                file_ext = ".jpg"
                filepath = path_img + img_name + file_ext

                # retrieve images with same component in a list
                compo_choice = random_choice.img_component

                for i in images:
                    if i.img_component == compo_choice:
                            list_img_choices.append(i)
                #delete the image already selected
                list_img_choices.remove(random_choice)

                # second image randomly choose in this new list
                random_choice_2 = random.choice(list_img_choices)
                #print(random_choice_2)
                img_name_2 = str(random_choice_2.img_name)
                file_ext = ".jpg"
                filepath_2 = path_img + img_name_2 + file_ext
                images.remove(random_choice_2)

                # list_image append dico key : compo, values : 2 paths
                list_images.append({'compo': random_choice.img_component, 'filepath1':filepath,'filepath2':filepath_2})
                list_id.append({'id': random_choice.id, 'filepath': filepath})
                used_images.append(random_choice.id)
                used_images.append(random_choice_2.id)

        request.session['choiceQuestion'] = question.quest_type
        request.session['question'] = question.quest
        request.session['images'] = list_images
        request.session['ids'] = list_id

        #return the elements to display in the html page
        return render(request, "Quizz/Quizz_component.html",
                      {'choiceQuestion': request.session.get('choiceQuestion'),
                       'question': request.session.get('question'), 'form': QuizzCompo.form,
                       'images': request.session.get('images'),
                       'id':request.session.get('ids'),
                       'score': score})


    def post(self, request):

        form = QuizzCompo.form(request.POST)

        # retrieve answers in a list only if the user has chosen at least one answer for each question
        if (form.is_valid()):

            list_answers = [form.cleaned_data['firstQuestion'],
                            form.cleaned_data['secondQuestion'],
                            form.cleaned_data['thirdQuestion'],
                            form.cleaned_data['fourthQuestion'],
                            form.cleaned_data['fifthQuestion']
                            ]

            request.session['list_answers'] = list_answers
            print(request.session['list_answers'])
            points_gained = 0
            list_quest_to_answer=[]
            list_correction =[]
            id_images_iter = iter(request.session['ids'])

            # compare user's answers and correction answers in list_correction
            for answer in list_answers:
                question = Question.objects.filter(quest_id=2)
                image_id = Images.objects.filter(id=next(id_images_iter)['id']).first()
                point_val = question.values('quest_point').first()['quest_point']

                if answer == image_id.img_component:
                    list_quest_to_answer.append("True")
                    points_gained += point_val

                else:
                    list_quest_to_answer.append("False")

                list_correction.append(image_id.img_component)

            #add the points won to the user score and save it
            user_id = User.objects.get(id=request.user.id)
            profile_obj = Profile.objects.get(user_id=user_id)
            profile_obj.score = profile_obj.score + points_gained
            profile_obj.save()

            request.session['list_quest_to_answer'] = list_quest_to_answer
            request.session['list_correction'] = list_correction

            print(request.session['list_correction'])
            print(request.session['list_quest_to_answer'])
            print(points_gained)
            return redirect('component_correction')

        else:
            print(form.errors)

def component_correction(request):

    user_id = User.objects.get(id=request.user.id)
    score = Profile.objects.get(user_id=user_id)
    score = score.score

    #return the elements to display in the html page for Quizz component correction
    return render(request, "Quizz/component_correction.html",
        {'images': request.session.get('images'),
        'list_quest_to_answer': request.session.get('list_quest_to_answer'),
         'list_correction': request.session.get('list_correction'),
         'list_choices': [('pollen wall', 0),  ('dendrite', 1),
                          ('synaptic vesicle', 2), ('microtubule cytoskeleton', 3),('desmosome', 4),
                          ('axoneme', 5),('endoplasmic reticulum', 6),('mitochondrion',7)],
          'list_answers': request.session.get('list_answers'),'score': score})
