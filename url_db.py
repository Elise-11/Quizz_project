# -*- coding: utf-8 -*-

import urllib.request
from MicroscopyQuizz.models import Images
import random


def run():
    ## Creation of a dictionnary to put url pictures

    dictionnary_URL = {}

    ## Taking all the pictures from the database

    images = Images.objects.all()

    ## For all the pictures

    for i in images:

        ## We look for on the cellimage library rhe page associated to the i picture
        ## And we load the content of the webpage in a variable

        url = "http://www.cellimagelibrary.org/images/" + "{}".format(i.image_name)
        webContent = urllib.request.urlopen(url)
        image_name = i.image_name

        ## Initialising of a counter line to count the number of lines
        ## of the webpage contain

        contentNumber = 0

        while (webContent.readline()):
            contentNumber += 1

        ## Reopening of the WebPage contain

        webContent = urllib.request.urlopen(url)

        ## Creation of a variable to count the number
        ## of reference tags allowing to parse the wanted url
        ## in the webpage source code and creation of a variable
        ## to count the number of line until we find the occurence
        ## number of the reference tag

        ContainerTagNumber = 0
        numberLine = 0

        ## For all the lines of the webpage source code

        for j in range(0, contentNumber):

            ## Reading the line

            line = webContent.readline()

            ## If we find the reference tag for the parse
            ## we increment the variable counter
            ## If we have found three reference tags
            ## we memorize the line number in a variable

            if (line.find(b'<div class="container">') != -1):
                ContainerTagNumber += 1

            if (ContainerTagNumber == 3):
                numberLine = j
                ContainerTagNumber += 1

        ## Reopening the WebPage source code

        webContent = urllib.request.urlopen(url)

        ## For all the lines in the WebPage source code

        for k in range(0, contentNumber):

            ## If k is inferior to the line number of
            ## reference, we read the line

            if (k < numberLine):
                webContent.readline()

            else:

                line = webContent.readline()

                ## if we find an image
                ## we convert bytes of the webPage source code

                if (line.find(b'<img  alt=') != -1):
                    lineToRegister = line.decode('utf-8')

        ## Initialisation to memorize the number of quotes
        ## to parse the url of the picture
        ## and to memorize the url address of the picture

        counterQuote = 0
        address = ""

        ## Reading all the characters of the line to parse

        for l in lineToRegister:
            if (l == '"'):
                ## If we find a quote
                ## We increment the counter

                counterQuote += 1

            ## If we met three quotes already
            ## We begin to memorize the url

            if (counterQuote == 3):
                address += l

        ## If the address begins by https
        ## We directly memorize the address

        if (address.find('https') != -1):
            address = address[1:len(address)]

        ## else, we add an extension for website
        ## may read the picture from the cell image
        ## library website

        else:
            address = address[2:len(address)]
            address = "http://www.cellimagelibrary.org/" + address

        ## Then we add the url to the picture in the database

        imagesToRegister = Images.objects.filter(image_name=image_name)

        for l in imagesToRegister:
            l.url = address
            l.save()




