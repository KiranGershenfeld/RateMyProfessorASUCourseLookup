from bs4 import BeautifulSoup
import requests
import json
import os
import lxml

#Initialization Information
TeachersWithoutEntries = []
TeachersWithNoReviews = []
text_file = open("Output.txt", "w")
text_file.write("The Following Data was collected from RateMyProfessor.com as well as the ASU Course Catalog using the Department and Class Number that you entered.")

def CreateTeacherList():
    ProfessorsTeachingThisClass = []
    #Asks user for the url of the ASU Course Catalouge page that they want queried
    print("Enter url of ASU Course Search Catalouge page you want queried")
    userUrl = input()
    url = userUrl.replace("classlist", "myclasslistresults")
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "lxml")

    for tags in soup.findAll("a", {"class":"nametip"}):
        #teacherName = tags.get('title')
        #teacherName = teacherName[11:]
        teacherName = tags.text.strip()
        if teacherName not in ProfessorsTeachingThisClass and teacherName != "Staff":
            ProfessorsTeachingThisClass.append(teacherName)
            numASUProfessors = len(ProfessorsTeachingThisClass)
    print(ProfessorsTeachingThisClass)
    return ProfessorsTeachingThisClass

#Use this function to get RMP teacher ids for a given professor name. This is necessary to find their actual RMP page.
def GetProfessorData(professor):
    #This URL is a JSON page for RMP teacher data
    QueryURL = "https://solr-aws-elb-production.ratemyprofessors.com//solr/rmp/select/?solrformat=true&rows=20&wt=json&json.wrf=noCB&callback=noCB&q=" + professor + "+AND+schoolid_s%3A45&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=20&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq="
    wrappedPage = requests.get(QueryURL)
    wrappedJSON = BeautifulSoup(wrappedPage.content, "lxml").find("p").text.strip()
    print(wrappedJSON)
    trimmedJSON = wrappedJSON[5:-1]
    JSONdata = json.loads(trimmedJSON)
    #This JSON data contains the number of teachers for that name and their IDs. these will be used in GetRMPData()
    response = JSONdata["response"]
    return response

#Iterates through the list of professors gathered from the ASU course catalog
def GetRMPData():
    ProfessorsTeachingThisClass = CreateTeacherList()
    for professor in ProfessorsTeachingThisClass:
        response = GetProfessorData(professor)
        #Conditions for whether professor was found and has reviews
        if response["numFound"] > 0:
            profData = response["docs"][0]
            if profData["total_number_of_ratings_i"] > 0:
                #Gathering name and id of professor
                profID = profData["pk_id"]
                profName = profData["teacherfirstname_t"] + " " + profData["teacherlastname_t"]
                #Ask Ratemyprofessor for data for this teacher using their ID
                actualRMPURL = requests.get("https://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(profID) + "&showMyProfs=true")
                RMPSoup = BeautifulSoup(actualRMPURL.content, "lxml")

                text_file.write("\n\n" + profName +"\n")
                text_file.write("https://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(profID) + "&showMyProfs=true\n")
                text_file.write("Overall Quality: " + RMPSoup.find("div", {"class":"RatingValue__Numerator-qw8sqy-2 gxuTRq"}).text.strip() + "\n")
                description = ["Would Take Again", "Difficulty"]
                descriptionNumber = 0
                for grade in RMPSoup.findAll("div", {"class":"FeedbackItem__FeedbackNumber-uof32n-1 bGrrmf"}):
                    print(description[descriptionNumber] + ": " + grade.text.strip())
                    text_file.write(description[descriptionNumber] + ": " + grade.text.strip() + "\n")
                    descriptionNumber+=1
            else:
                TeachersWithNoReviews.append(professor)
        else:
            TeachersWithoutEntries.append(professor)
    print("")
    text_file.write("\n\nThe Following Teachers Had 0 Reviews\n")
    for teacher in TeachersWithNoReviews:
        print(teacher)
        text_file.write(teacher + "\n")
    print("")
    text_file.write("\nThe Following Teachers Couldnt Be Found\n")
    for teacher in TeachersWithoutEntries:
        print(teacher)
        text_file.write(teacher + "\n")

    text_file.close()
    os.startfile("Output.txt")

#Run Project
GetRMPData()
