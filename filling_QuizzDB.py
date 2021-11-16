# -*- coding: utf-8 -*-
from Quizz_project.wsgi import application
from Quizz_project_app.models import Answers, Question, Images
import os

'''
This script allows to fill the tables of the database 
from tables in csv format 
'''
def run():
    # Load the table folder
    newPath = os.path.abspath("Quizz_project_app/tables/")
    os.chdir(newPath)

    #Open the Answer table
    file = open('table_answer.csv', 'r')
    counterTableAnswer = 0

    #Count the number of line in the file
    while (file.readline()):
        counterTableAnswer += 1

    file.close()

    file = open('table_answer.csv', 'r')

    # Create a dictionary to store parsed data
    dictionnary_lineAnswers = {}

    for iterator in range(0, counterTableAnswer):
        line = file.readline().replace('\n', '')

        # If we don't read the first line
        if (iterator != 0):

            # Split the line by comma
            line_splitted = line.split(',')

            # Create a list to store elements to parse
            list_to_register = []

            # append the first elements to parse
            list_to_register.append(line_splitted[0])
            list_to_register.append(line_splitted[1])
            list_to_register.append(line_splitted[2])

            # Extract the last element to parse
            elements_to_parse = line_splitted[3:len(line_splitted)]

            # Reformate this element and store in the list
            last_element = ','.join(elements_to_parse)
            last_element = last_element[1:len(last_element) - 1]
            list_to_register.append(last_element)

            # Save the parse elements of the line in the dictionary
            dictionnary_lineAnswers[iterator] = list_to_register

    file.close()


    for iterator in range(1, counterTableAnswer):

        # Create an element in the database
        answer = Answers(answer_id=int(dictionnary_lineAnswers[iterator][0]),
                                                  q_id=int(dictionnary_lineAnswers[iterator][1]),
                                                  answer=dictionnary_lineAnswers[iterator][2],
                                                  definition=dictionnary_lineAnswers[iterator][3])

        # if the element doesn't exist in the database, create it
        if (not Answers.objects.filter(answer_id=int(dictionnary_lineAnswers[iterator][0]),
                                        q_id=int(dictionnary_lineAnswers[iterator][1]),
                                        answer=dictionnary_lineAnswers[iterator][2],
                                        definition=dictionnary_lineAnswers[iterator][3]).exists()):
                                            answer.save()


    # Open the Question table
    file = open('table_question.csv', 'r')
    counterTableQuestion = 0

    while (file.readline()):
        counterTableQuestion += 1

    file.close()

    file = open('table_question.csv', 'r')

    dictionnary_lineQuestion = {}

    for iterator in range(0, counterTableAnswer):
        line = file.readline().replace('\n', '')

        if (iterator != 0):
            line_splitted = line.split(',')
            dictionnary_lineQuestion[iterator] = line_splitted

    file.close()

    for iterator in range(1, counterTableQuestion):

        question = Question(quest_id=int(dictionnary_lineQuestion[iterator][0]),
                             quest=dictionnary_lineQuestion[iterator][1],
                             quest_type=dictionnary_lineQuestion[iterator][2],
                             quest_image_field=dictionnary_lineQuestion[iterator][3],
                             quest_point =int(dictionnary_lineQuestion[iterator][4]),
                             n_answer=int(dictionnary_lineQuestion[iterator][5]),
                             n_image=int(dictionnary_lineQuestion[iterator][6]))

        if (not Question.objects.filter(quest_id=int(dictionnary_lineQuestion[iterator][0]),
                                         quest=dictionnary_lineQuestion[iterator][1],
                                         quest_type=dictionnary_lineQuestion[iterator][2],
                                         quest_image_field=dictionnary_lineQuestion[iterator][3],
                                         quest_point =int(dictionnary_lineQuestion[iterator][4]),
                                         n_answer=int(dictionnary_lineQuestion[iterator][5]),
                                         n_image=int(dictionnary_lineQuestion[iterator][6])).exists()):
                    question.save()


    file = open('tables_images.csv', 'r')
    counterTableImages = 0

    while (file.readline()):
        counterTableImages += 1

    file.close()

    file = open('tables_images.csv', 'r')

    dictionnary_lineImages = {}

    for iterator in range(0, counterTableImages):
        line = file.readline().replace('\n', '')

        if (iterator != 0):

            # If presence of quotes
            if line.find("\"") != -1:

                # If the number of quotes is superior to 2
                if (line.count("\"")) > 2:

                    # split the line by comma and then take first and the second element
                    line_splitted = line.split(",")
                    list_to_register = []
                    list_to_register.append(line_splitted[0])
                    list_to_register.append(line_splitted[1])

                    list_to_parse = line_splitted[2:len(line_splitted)]

                    string_to_parse = ','.join(list_to_parse)

                    # count the number of quotes in the string list positions of them
                    counter_quote = 0
                    quote_in_string = string_to_parse.find('\"', counter_quote)
                    list_quote_in_string = []
                    list_quote_in_string.append(quote_in_string)

                    # While wuotes in the string
                    while (quote_in_string != -1):
                        # look for the others quotes and ist them too
                        counter_quote = quote_in_string + 1
                        list_quote_in_string.append(counter_quote - 1)
                        quote_in_string = string_to_parse.find('\"', counter_quote)

                    # constitue a new string from the coordinate of the last quote in the string until the end
                    # of the string
                    stringParse = string_to_parse[counter_quote:len(string_to_parse)]

                    # Split the line by comma
                    list_to_parse = stringParse.split(',')

                    # Cleaning the list from the first empty element
                    list_to_parse = list_to_parse[1:len(list_to_parse)]

                    # Decrement the counter quote
                    counter_quote = len(list_quote_in_string) - 1

                    # If there is a quote after the end of the second field corresponding to the img_description
                    if (len(list_to_parse) != 5):
                        while (len(list_to_parse) != 5):
                            counter_quote = counter_quote - 1
                            stringParse = string_to_parse[list_quote_in_string[counter_quote]: len(string_to_parse)]
                            list_to_parse = stringParse.split(',')
                            list_to_parse = list_to_parse[1:len(list_to_parse)]

                            if ('"' in list_to_parse):
                                list_to_parse.remove('"')

                    # append the string
                    list_to_register.append(string_to_parse[1:list_quote_in_string[counter_quote]])

                    #append the others elements
                    list_to_register.append(list_to_parse[0])
                    list_to_register.append(list_to_parse[1])
                    list_to_register.append(list_to_parse[2])
                    list_to_register.append(list_to_parse[3])
                    list_to_register.append(list_to_parse[4])

                    dictionnary_lineImages[iterator] = list_to_register

                else:

                    # If the number of quotes is equaled to 2
                    # Take the description between the two quotes
                    line_splitted = line.split(',')
                    list_to_register = []
                    list_to_register.append(line_splitted[0])
                    list_to_register.append(line_splitted[1])
                    line_splitted = line.split("\"")
                    linequotes = line_splitted[1]
                    linequotes = linequotes
                    list_to_register.append(linequotes)

                    elements_to_parse = line_splitted[len(line_splitted) - 1]
                    line_splitted = elements_to_parse.split(',')
                    line_splitted = line_splitted[1:len(line_splitted)]

                    # If organism name absent
                    # Append none at the end of the list

                    if (len(line_splitted) != 4):

                        list_to_register.append(line_splitted[0])
                        list_to_register.append(line_splitted[1])
                        list_to_register.append(line_splitted[2])
                        list_to_register.append(line_splitted[3])
                        list_to_register.append(line_splitted[4])

                    else:
                        list_to_register.append(line_splitted[0])
                        list_to_register.append(line_splitted[1])
                        list_to_register.append(line_splitted[2])
                        list_to_register.append(line_splitted[3])
                        list_to_register.append('None')

                    dictionnary_lineImages[iterator] = list_to_register

            else:
                # no quotes in the string, split the line by comma and extract the informations
                line_splitted = line.split(',')
                if (len(line_splitted) != 8):
                    line_splitted.append('None')

                line_splitted[2] = line_splitted[2]
                dictionnary_lineImages[iterator] = line_splitted

    file.close()

    for iterator in range(1, counterTableImages):

        images = Images(img_name=int(dictionnary_lineImages[iterator][1]),
                         img_description=dictionnary_lineImages[iterator][2],
                         img_mode=dictionnary_lineImages[iterator][3],
                         img_cell_type=dictionnary_lineImages[iterator][4],
                         img_component=dictionnary_lineImages[iterator][5],
                         img_doi=dictionnary_lineImages[iterator][6],
                         img_organism=dictionnary_lineImages[iterator][7])


        if (not Images.objects.filter(img_name=int(dictionnary_lineImages[iterator][1]),
                                       img_description=dictionnary_lineImages[iterator][2],
                                       img_mode=dictionnary_lineImages[iterator][3],
                                       img_cell_type=dictionnary_lineImages[iterator][4],
                                       img_component=dictionnary_lineImages[iterator][5],
                                       img_doi=dictionnary_lineImages[iterator][6],
                                       img_organism=dictionnary_lineImages[iterator][7]).exists()):
            images.save()

if __name__ == "__main__":
    print("filling database...")
    run()