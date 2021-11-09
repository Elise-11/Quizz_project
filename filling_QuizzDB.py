# -*- coding: utf-8 -*-
from Quizz_project.wsgi import application
from Quizz_project_app.models import Answers, Question, Images
import os

def run():
    ## Loading the folder

    newPath = os.path.abspath("Quizz_project_app/tables/")
    os.chdir(newPath)

    ## Opening the Answer table

    file = open('table_answer.csv', 'r')
    counterTableAnswer = 0

    ## Counting the number of line in the file

    while (file.readline()):
        counterTableAnswer += 1

    file.close()

    file = open('table_answer.csv', 'r')

    ## Creating a dictionnary to store parsed data
    ## For each line

    dictionnary_lineAnswers = {}

    ## For all the lines in the Answers table

    for iterator in range(0, counterTableAnswer):
        line = file.readline().replace('\n', '')

        ## If we don't read the first line

        if (iterator != 0):
            ## Splitting the line by comma

            line_splitted = line.split(',')

            ## Creating a list to store elements to parse

            list_to_register = []

            ## Appending the first elements to parse

            list_to_register.append(line_splitted[0])
            list_to_register.append(line_splitted[1])
            list_to_register.append(line_splitted[2])

            ## Extracting the last element to parse

            elements_to_parse = line_splitted[3:len(line_splitted)]

            ## Reformating this element and saving in the list

            last_element = ','.join(elements_to_parse)
            last_element = last_element[1:len(last_element) - 1]
            list_to_register.append(last_element)

            ## Saving the parse elements of the line in
            ## the dictionnary

            dictionnary_lineAnswers[iterator] = list_to_register

    ## Closing the file

    file.close()

    ## For each line of the dictionnary

    for iterator in range(1, counterTableAnswer):

        ## Creating an element in the database

        answer = Answers(answer_id=int(dictionnary_lineAnswers[iterator][0]),
                                                  q_id=int(dictionnary_lineAnswers[iterator][1]),
                                                  answer=dictionnary_lineAnswers[iterator][2],
                                                  definition=dictionnary_lineAnswers[iterator][3])

        ## if the element doesn't exist in the database
        ## So we create it

        if (not Answers.objects.filter(answer_id=int(dictionnary_lineAnswers[iterator][0]),
                                        q_id=int(dictionnary_lineAnswers[iterator][1]),
                                        answer=dictionnary_lineAnswers[iterator][2],
                                        definition=dictionnary_lineAnswers[iterator][3]).exists()):
                                            answer.save()



    ## Opening the Question table

    file = open('table_question.csv', 'r')
    counterTableQuestion = 0

    ## Reading and counting lines of the file

    while (file.readline()):
        counterTableQuestion += 1

    file.close()

    file = open('table_question.csv', 'r')

    ## Creating a dictionnary to store parsed data
    ## For each line

    dictionnary_lineQuestion = {}

    ## For each line, reading the line

    for iterator in range(0, counterTableAnswer):
        line = file.readline().replace('\n', '')

        ## If we don't read the first line
        ## Splitting of the line by coma
        ## And registering the parsed line in the dictionnary

        if (iterator != 0):
            line_splitted = line.split(',')
            dictionnary_lineQuestion[iterator] = line_splitted

    file.close()

    for iterator in range(1, counterTableQuestion):

        ## Creating an element in the database

        question = Question(quest_id=int(dictionnary_lineQuestion[iterator][0]),
                             quest=dictionnary_lineQuestion[iterator][1],
                             quest_type=dictionnary_lineQuestion[iterator][2],
                             quest_image_field=dictionnary_lineQuestion[iterator][3],
                             quest_point =int(dictionnary_lineQuestion[iterator][4]),
                             n_answer=int(dictionnary_lineQuestion[iterator][5]),
                             n_image=int(dictionnary_lineQuestion[iterator][6]))

        ## If we don't read the first line
        ## Splitting of the line by coma
        ## And registering the parsed line in the dictionnary

        if (not Question.objects.filter(quest_id=int(dictionnary_lineQuestion[iterator][0]),
                                         quest=dictionnary_lineQuestion[iterator][1],
                                         quest_type=dictionnary_lineQuestion[iterator][2],
                                         quest_image_field=dictionnary_lineQuestion[iterator][3],
                                         quest_point =int(dictionnary_lineQuestion[iterator][4]),
                                         n_answer=int(dictionnary_lineQuestion[iterator][5]),
                                         n_image=int(dictionnary_lineQuestion[iterator][6])).exists()):
                    question.save()



    ## Opening the images table

    file = open('tables_images.csv', 'r')
    counterTableImages = 0

    ## Counting the lines in the table

    while (file.readline()):
        counterTableImages += 1

    file.close()

    file = open('tables_images.csv', 'r')

    ## Creating a dictionnary to store all the parsed text
    ## For all the lines of the text

    dictionnary_lineImages = {}

    ## For all the lines of the text

    for iterator in range(0, counterTableImages):
        line = file.readline().replace('\n', '')

        ## If we don't read the first line

        if (iterator != 0):

            ## If we find quotes

            if line.find("\"") != -1:

                ## If the number of quotes is superior to 2

                if (line.count("\"")) > 2:

                    ## We split the line by comma and then
                    ## We take first and the second element

                    line_splitted = line.split(",")
                    list_to_register = []
                    list_to_register.append(line_splitted[0])
                    list_to_register.append(line_splitted[1])

                    ## Then, we extract only the others elements to parse

                    list_to_parse = line_splitted[2:len(line_splitted)]

                    ## We make a string from the list

                    string_to_parse = ','.join(list_to_parse)

                    ## We count the number of quotes in the string
                    ## And we list positions of them

                    counter_quote = 0
                    quote_in_string = string_to_parse.find('\"', counter_quote)
                    list_quote_in_string = []
                    list_quote_in_string.append(quote_in_string)

                    ## While we find quotes in the string

                    while (quote_in_string != -1):
                        ## We look for the others quotes and
                        ## we list them too

                        counter_quote = quote_in_string + 1
                        list_quote_in_string.append(counter_quote - 1)
                        quote_in_string = string_to_parse.find('\"', counter_quote)

                    ## We constitue a new string from the coordinate
                    ## of the last quote in the string until the end
                    ## of the string

                    stringParse = string_to_parse[counter_quote:len(string_to_parse)]

                    ## Splitting the line by comma

                    list_to_parse = stringParse.split(',')

                    ## Cleaning the list from the first empty element

                    list_to_parse = list_to_parse[1:len(list_to_parse)]

                    ## Decrement the counter quote

                    counter_quote = len(list_quote_in_string) - 1

                    ## If there is a quote after the end of the second
                    ## field cooresponding to the descrition, we need to
                    ## take the precedent quote until
                    ## to have all elements of the database

                    if (len(list_to_parse) != 5):
                        while (len(list_to_parse) != 5):
                            counter_quote = counter_quote - 1
                            stringParse = string_to_parse[list_quote_in_string[counter_quote]: len(string_to_parse)]
                            list_to_parse = stringParse.split(',')
                            list_to_parse = list_to_parse[1:len(list_to_parse)]

                            if ('"' in list_to_parse):
                                list_to_parse.remove('"')

                    ## When we have the correct string, we append it

                    list_to_register.append(string_to_parse[1:list_quote_in_string[counter_quote]])

                    ## Then, we append the others elements

                    list_to_register.append(list_to_parse[0])
                    list_to_register.append(list_to_parse[1])
                    list_to_register.append(list_to_parse[2])
                    list_to_register.append(list_to_parse[3])
                    list_to_register.append(list_to_parse[4])

                    dictionnary_lineImages[iterator] = list_to_register

                else:

                    ## If the number of quotes is equaled to 2
                    ## We take the description between the two quotes

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

                    ## If there is not the organism name
                    ## We append none at the end of the list

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
                ## Finally, if there is not quotes in the string
                ## We split the line by comma and extract the
                ## informations

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
    print("filling database.")
    run()