from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.generic import ListView, CreateView, DetailView
from .models import Event, Preferences,Interested
from django.contrib.auth.decorators import login_required

import time
import datetime
import csv
import numpy as np
from numpy import *
import logging

# Function used to transfer data from CSV file to Django database
def transferToBD():
    DATA_SRC2 = '/Users/dominiknair/Desktop/backupOfProject/version1/finalYearProject/project/eventData2.csv'
    with open(DATA_SRC2, 'r' , encoding = "ISO-8859-1") as csv_file2:
        csv_reader2 = csv.reader(csv_file2)
        next(csv_reader2)
        for line2 in csv_reader2:
                transfer = Event(title = line2[0], date = line2[1], location = line2[2], link=line2[3], category=line2[4], price=line2[5])
                transfer.save()

@login_required
def home(request):
# CHECK IF INTERESTED EVENT IS EXPIRED AND FORCE USER TO RATE IT:
    var =Interested.objects.filter(user = request.user)
    # print(len(var))

    currentTS = datetime.datetime.now().timestamp()
    # print(currentTS)
    for i in range(len(var)):
        interestedTimestamp = getTimestamp(var[i].date)
        if currentTS > interestedTimestamp:
            # print("event has finished")

            posts=[]
            posts.append({
                                            'id' : var[i].id,
                                            'title' : var[i].title.replace("|", ","),
                                            'date' : var[i].date.replace("|", ","),
                                            'location' : var[i].location.replace("|", ","),
                                            'link' : var[i].link,
                                            'category' : var[i].category,
                                            'price' : var[i].price.replace("|",",")
                                            })
            context={
                'posts' : posts
            }
            try:
                ineterstedDelete = Event.objects.get(title = var[i].title)
                ineterstedDelete.delete()
            except:
                return render(request, 'project/rateInterestedEvent.html',context)

            return render(request, 'project/rateInterestedEvent.html',context)

# ------------------------------------------------------------ PART 1 ------------------------------------------------------------
    var =Preferences.objects.filter(user = request.user)
    if len(var) >= 20:
        lengthOfLoop = len(var)
        categories = ["health","science-and-tech","sports-and-fitness","business","music","arts","charity-and-causes","community","environment","coding","talks","media","tours","history","economy","career","cultural","investment","networking","dance"]
        userProfile = []
        eventMatrixFinal=[]

        for i in range(lengthOfLoop):
            # declare empty array of format of the matrix row, and read the second column of csv and split it where there is a comma, each new word is stored in a new index in array tempEventList
            eventMatrix =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            categories = var[i].category

            tempEventList = categories.split(',')
            userProfile.append(int(var[i].rating))

            # Check the category and get the index of that category
            for j in range(len(tempEventList)):
                temp = tempEventList[j]

                temp.strip()
                if temp == "health":
                    index = 0
                if temp == "science-and-tech":
                    index = 1
                if temp == "sports-and-fitness":
                    index = 2
                if temp == "business":
                    index = 3
                if temp == "music":
                    index = 4
                if temp == "arts":
                    index = 5
                if temp == "charity-and-causes":
                    index = 6
                if temp == "community":
                    index = 7
                if temp == "environment":
                    index = 8
                if temp == "coding":
                    index = 9
                if temp == "talks":
                    index = 10
                if temp == "media":
                    index = 11
                if temp == "tours":
                    index = 12
                if temp == "history":
                    index = 13
                if temp == "economy":
                    index = 14
                if temp == "career":
                    index = 15
                if temp == "cultural":
                    index = 16
                if temp == "investment":
                    index = 17
                if temp == "networking":
                    index = 18
                if temp == "dance":
                    index = 19
                # Append a 1 to the list in poisition of index value
                eventMatrix[index] = 1
            # append to finalmatrix list first row of the matrix
            for x in range(20):
                eventMatrixFinal.append(eventMatrix[x])

		    # LINE BELOW CONVERTS THE 'eventMatrixFinal' into a matrix that has 20 columns
            b = np.reshape(eventMatrixFinal, (-1, 20))
            bmatrix = matrix(b)
            # converts the userProfile into a matrix
            m = matrix(userProfile)
            # multiplication of matrix and store outcome matrix in weightedGenreMatrix variables
            weightedGenreMatrix = m*bmatrix

            # converts the matrix with multiplication result into a list
            weightedGenreList = np.squeeze(np.asarray(weightedGenreMatrix))

            # gets the sum of the matrix values from the list
            sumOfList = sum(weightedGenreList)
            # normalizes by dividing the value at an index by the sum of the matrix, then the outcome gets put into a weightedProfile list
            weightedProfile =[]
            for d in range(len(weightedGenreList)):
                normalizedVal = weightedGenreList[d] / sumOfList

                weightedProfile.append(normalizedVal)
        recEvent = {}
    # ------------------------------------------------------------ PART 2 ------------------------------------------------------------
    #READING THE EVENTS DATASET AND PUTTING IT INTO A MATRIRX
        event = Event.objects.all()

        user = request.user
        #FOR EACH EVENT
        for j in range(len(event)):
                eventMatrix =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                # print(event[j].title)
                eventTimestamp = getTimestamp(event[j].date)

                # Check if an event is expired, if it is then delete it from the database
                if currentTS > eventTimestamp:
                    eventDelete = Event.objects.get(title = event[j].title)
                    eventDelete.delete()
                else:

                    # INSERT FOR LOOP TO SEE IF THE EVENT FROM EVENTS TABLE IS PRESENT IN THE INTERESTED TABLE, IF IT IS THEN SKIP IT IF NOT THEN PROCESS IT
                    var =Interested.objects.filter(user = request.user)
                    # Cheeck if the user already has the event in their interested page, if they do set the "ispresent" variable to true
                    ispresent = False
                    for i in range(len(var)):
                        if var[i].title == event[j].title:
                            ispresent = True
                    # If event is not in interested then get the index of the category of the event.
                    if ispresent == False:
                            tempEventList2 = event[j].category.split(',')
                            for i in range(len(tempEventList2)):
                                temp = tempEventList2[i]
                                temp.strip()
                                if temp == "health":
                                    index = 0
                                if temp == "science-and-tech":
                                    index = 1
                                if temp == "sports-and-fitness":
                                    index = 2
                                if temp == "business":
                                    index = 3
                                if temp == "music":
                                    index = 4
                                if temp == "arts":
                                    index = 5
                                if temp == "charity-and-causes":
                                    index = 6
                                if temp == "community":
                                    index = 7
                                if temp == "environment":
                                    index = 8
                                if temp == "coding":
                                    index = 9
                                if temp == "talks":
                                    index = 10
                                if temp == "media":
                                    index = 11
                                if temp == "tours":
                                    index = 12
                                if temp == "history":
                                    index = 13
                                if temp == "economy":
                                    index = 14
                                if temp == "career":
                                    index = 15
                                if temp == "cultural":
                                    index = 16
                                if temp == "investment":
                                    index = 17
                                if temp == "networking":
                                    index = 18
                                if temp == "dance":
                                    index = 19

                                # Append a 1 to "eventMatrix" list in the position of index
                                eventMatrix[index] = 1
                            temp=[]

                            for t in range(len(eventMatrix)):
                                # append into temp variable the ouctome of the multiplication of weightedProfile and eventMatrix at the same index
                                temp.append(weightedProfile[t] * eventMatrix[t])
                                # store the sum of the values from temp in a variable called tempSum
                                tempSum= sum(temp)
                            # Set the key variable to be the title of the event
                            key = event[j].title
                            # Append to "recEvent" dictionary the "key" variable as the key and "tempSum" as value
                            recEvent[key] = tempSum

    # ------------------------------------------------------------ PART 3 ------------------------------------------------------------
    # THIS PART OF THE RECOMMENDATION ALGORITHM TAKES THE DICTIONARY OF THE EVENTS AND OUTPUTS A TOP30 LIST

        # Sorts the dictionary into reverse order (highest scores first)
        sorted_dict2 = sorted(recEvent.items(), key=lambda t:t[1],reverse=True)
        newList = []
        # Appends to "newList" list the first 30 values of the dictionary
        for i in range(30):
            newList.append(sorted_dict2[i])
        posts=[]
        # for loop to obtain further details of the top recommended events
        for k in range(len(event)):
            for m in range(30):
                if newList[m][0] == event[k].title:
                    # Appends: id, title, date, location, link, category, score and price to the dictionary "posts"
                    posts.append({
                                                    'id' : event[k].id,
    		                                        'title' : newList[m][0].replace("|", ","),
    		                                        'date' : event[k].date.replace("|", ","),
    		                                        'location' : event[m].location.replace("|", ","),
    		                                        'link' : event[k].link,
    		                                        'category' : event[k].category.replace(",", "|"),
                                                    'score' : newList[m][1],
                                                    'price' : event[k].price.replace("|",",")
    		                                        })
                context={
                    'posts' : posts
                }
        # Renders the home page with all of the users recommended events
        return render(request, 'project/home.html',context)
    # Else statement renders the preference page as the user does not have at least 20 preferences.
    else:
        print("redirect to preference page")
        return render(request, 'project/preference1.html')

class EventDetailView(DetailView):
    model = Event

class interestedDetailView(DetailView):
    model = Interested

# Preference page view function takes the input frorm the HTML pagee and adds it to the database for the current logged in user
@login_required
def preference1(request):
    redirect =[]
    var =Preferences.objects.filter(user = request.user)
    if len(var) >= 8:
        redirect.append({
            'sentence' : 'You have already filled in the preference page, please go to homepage!'
        })
        context={
            'redirect' :redirect
        }
        return render(request, 'project/home.html',context)
    else:
        if request.method == 'POST':
            health = request.POST['health']
            print(health)
            science_and_tech = request.POST['science_and_tech']
            print(science_and_tech)
            sports_and_fitness = request.POST['sports_and_fitness']
            print(sports_and_fitness)
            business = request.POST['business']
            print(business)
            music = request.POST['music']
            print(music)
            arts = request.POST['arts']
            print(arts)
            charity = request.POST['charity']
            print(charity)
            community = request.POST['community']
            print(community)

            environment = request.POST['environment']
            print(environment)
            coding = request.POST['coding']
            print(coding)
            talks = request.POST['talks']
            print(talks)
            media = request.POST['media']
            print(media)
            tours = request.POST['tours']
            print(tours)
            history = request.POST['history']
            print(history)
            economy = request.POST['economy']
            print(economy)
            career = request.POST['career']
            print(career)
            cultural = request.POST['cultural']
            print(cultural)
            investment = request.POST['investment']
            print(investment)
            networking = request.POST['networking']
            print(networking)
            dance = request.POST['dance']
            print(dance)


            user = request.user
            preferences = Preferences(user = user, category ='health', rating = health)
            preferences.save()
            preferences = Preferences(user = user, category ='science-and-tech', rating = science_and_tech)
            preferences.save()
            preferences = Preferences(user = user, category ='sports-and-fitness', rating = sports_and_fitness)
            preferences.save()
            preferences = Preferences(user = user, category ='business', rating = business)
            preferences.save()
            preferences = Preferences(user = user, category ='music', rating = music)
            preferences.save()
            preferences = Preferences(user = user, category ='arts', rating = arts)
            preferences.save()
            preferences = Preferences(user = user, category ='charity-and-causes', rating = charity)
            preferences.save()
            preferences = Preferences(user = user, category ='community', rating = community)
            preferences.save()

            preferences = Preferences(user = user, category ='environment', rating = environment)
            preferences.save()
            preferences = Preferences(user = user, category ='coding', rating = coding)
            preferences.save()
            preferences = Preferences(user = user, category ='talks', rating = talks)
            preferences.save()
            preferences = Preferences(user = user, category ='media', rating = media)
            preferences.save()
            preferences = Preferences(user = user, category ='tours', rating = tours)
            preferences.save()
            preferences = Preferences(user = user, category ='history', rating = history)
            preferences.save()
            preferences = Preferences(user = user, category ='economy', rating = economy)
            preferences.save()
            preferences = Preferences(user = user, category ='career', rating = career)
            preferences.save()
            preferences = Preferences(user = user, category ='cultural', rating = cultural)
            preferences.save()
            preferences = Preferences(user = user, category ='investment', rating = investment)
            preferences.save()
            preferences = Preferences(user = user, category ='networking', rating = networking)
            preferences.save()
            preferences = Preferences(user = user, category ='dance', rating = dance)
            preferences.save()

        return render(request, 'project/home.html')

def addInterested(request):
    user = request.user
    if request.method == 'POST':
        date = request.POST['date']
        location = request.POST['location']
        link = request.POST['link']
        title = request.POST['title']
        category = request.POST['category']
        price = request.POST['price']
        var =Interested.objects.all()

        ispreasent = False
        for i in range(len(var)):

            if var[i].user == user and var[i].title == title:
                print("event is already marked as interested!")
                ispreasent = True
                break
        if ispreasent == False:
            interested = Interested(user = user, title=title, date=date, location=location, link=link, category=category, price=price)
            interested.save()

    return render(request, 'project/home.html')

# Function deletes events from interesteede
def deleteInterested(request):

    user = request.user
    if request.method == 'POST':
        id = request.POST['id']
        var =Interested.objects.all()
        ineterstedDelete = Interested.objects.get(id = id)
        ineterstedDelete.delete()
        # for i in range(len(var)):
        #
        #     if var[i].user == user and var[i].title == title:
        #         print("event is already marked as interested!")
        #         ispreasent = True
        #         break
        # if ispreasent == False:
        #     interested = Interested(user = user, title=title, date=date, location=location, link=link, category=category, price=price)
        #     interested.save()
        print("ID IS!!!!!!!!!!!!!!!!!!!!")
        print(id)

    return render(request, 'project/home.html')
# Function renders all of the users events that they have added to their interested
def interestedEvents(request):
    currentLoggedinUser = request.user
    numOfUserInterests =Interested.objects.filter(user = currentLoggedinUser)
    redirect =[]
    if len(numOfUserInterests) >=1:
        var =Interested.objects.all()
        posts=[]
        for i in range(len(var)):

            if var[i].user == currentLoggedinUser:

                posts.append({
                                                'id' : var[i].id,
                                                'title' : var[i].title.replace("|", ","),
                                                'date' : var[i].date.replace("|", ","),
                                                'location' : var[i].location.replace("|", ","),
                                                'link' : var[i].link,
                                                'category' : var[i].category.replace(",", "|"),
                                                'price' : var[i].price.replace("|",",")
                                                })
        context={
            'posts' : posts
        }
        return render(request, 'project/interestedEvents.html',context)
    else:
        redirect.append({
            'sentence' : 'You currently have no events that you are interested in. Please go to the homepage and select events that you may like'
        })

        context={
            'redirect' : redirect
        }
        return render(request, 'project/interestedEvents.html',context)


class PreferencesCreateView(CreateView):
    model = Preferences
    fields=['category', 'rating']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        return render(request, 'project/home.html')
# Render about page
def about(request):
    return render(request, 'project/about.html', {'title':'about'})

def addToUserProfile(request):

    user = request.user
    if request.method == 'POST':
        rating = request.POST['rating']
        category = request.POST['category']
        id = request.POST['id']

        ineterstedDelete = Interested.objects.get(id = id)
        ineterstedDelete.delete()

        preferences = Preferences(user = user, category =category, rating = rating)
        preferences.save()

    return render(request, 'project/preference1.html')


# Function to retrieve timestamp given a time/date as an input parameter
def getTimestamp(date):

    temp = date.split("| ")

    date = temp[1].split(" ")
    # print(date[0])
    # print(date[1])



    if date[0] == "Jan" or date[0] == "jan" :
        dateToConvert=date[1]+ "/" + "01" + "/"+"2021"
    if date[0] == "Feb" or date[0] == "feb" :
        dateToConvert=date[1]+ "/" + "02" + "/"+"2021"
    if date[0] == "Mar" or date[0] == "mar" :
        dateToConvert=date[1]+ "/" + "03" + "/"+"2020"
    if date[0] == "Apr" or date[0] == "apr" :
        dateToConvert=date[1]+ "/" + "04" + "/"+"2020"
    if date[0] == "May" or date[0] == "may" :
        dateToConvert=date[1]+ "/" + "05" + "/"+"2020"
    if date[0] == "Jun" or date[0] == "jun" :
        dateToConvert=date[1]+ "/" + "06" + "/"+"2020"
    if date[0] == "Jul" or date[0] == "jul" :
        dateToConvert=date[1]+ "/" + "07" + "/"+"2020"
    if date[0] == "Aug" or date[0] == "aug" :
        dateToConvert=date[1]+ "/" + "08" + "/"+"2020"
    if date[0] == "Sep" or date[0] == "sep" :
        dateToConvert=date[1]+ "/" + "09" + "/"+"2020"
    if date[0] == "Oct" or date[0] == "oct" :
        dateToConvert=date[1]+ "/" + "10" + "/"+"2020"
    if date[0] == "Nov" or date[0] == "nov" :
        dateToConvert=date[1]+ "/" + "11" + "/"+"2020"
    if date[0] == "Dec" or date[0] == "dec" :
        dateToConvert=date[1]+ "/" + "12" + "/"+"2020"

    date = datetime.datetime.strptime(dateToConvert, "%d/%m/%Y")
    interestedTimestamp = datetime.datetime.timestamp(date)

    return interestedTimestamp

@login_required
def searchEvent(request):
    return render(request, 'project/searchEvent.html')

def searchview1(request):
    return JsonResponse({
        'Event': list( Event.objects.values()),
    })
