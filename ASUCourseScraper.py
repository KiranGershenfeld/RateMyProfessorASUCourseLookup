from bs4 import BeautifulSoup
import requests
import json
import lxml

#Initialization Information
TeachersWithoutEntries = []
TeachersWithNoReviews = []

def CreateTeacherList(inputURL):
    ProfessorsTeachingThisClass = []
    #Asks user for the url of the ASU Course Catalouge page that they want queried
    url = inputURL.replace("classlist", "myclasslistresults")
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "lxml")

    for tags in soup.findAll("a", {"class":"nametip"}):
        #teacherName = tags.get('title')
        #teacherName = teacherName[11:]
        teacherName = tags.text.strip()
        if teacherName not in ProfessorsTeachingThisClass and teacherName != "Staff":
            ProfessorsTeachingThisClass.append(teacherName)
            numASUProfessors = len(ProfessorsTeachingThisClass)
    return ProfessorsTeachingThisClass

#Use this function to get RMP teacher ids for a given professor name. This is necessary to find their actual RMP page.
def GetProfessorData(professor):
    #This URL is a JSON page for RMP teacher data
    QueryURL = "https://solr-aws-elb-production.ratemyprofessors.com//solr/rmp/select/?solrformat=true&rows=20&wt=json&json.wrf=noCB&callback=noCB&q=" + professor + "+AND+schoolid_s%3A45&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=20&start=0&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq="
    wrappedPage = requests.get(QueryURL)
    wrappedJSON = BeautifulSoup(wrappedPage.content, "lxml").find("p").text.strip()
    trimmedJSON = wrappedJSON[5:-1]
    JSONdata = json.loads(trimmedJSON)
    #This JSON data contains the number of teachers for that name and their IDs. these will be used in GetRMPData()
    response = JSONdata["response"]
    return response

#Iterates through the list of professors gathered from the ASU course catalog
def GetRMPData(inputURL):
    ProfessorsTeachingThisClass = CreateTeacherList(inputURL)
    RMPData = {} #This will be the JSON returned to the webpage

    for professor in ProfessorsTeachingThisClass:
        response = GetProfessorData(professor)
        #Conditions for whether professor was found and has reviews
        if response["numFound"] > 0:
            profData = response["docs"][0]
            if profData["total_number_of_ratings_i"] > 0:
                #--THIS IS WHERE THE ACTUAL DATA IS FOUND--
                condensedProfData = {}
                #Gathering name and id of professor
                profID = profData["pk_id"]
                profName = profData["teacherfirstname_t"] + " " + profData["teacherlastname_t"]

                #Ask Ratemyprofessor for data for this teacher using their ID
                actualRMPURL = requests.get("https://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(profID) + "&showMyProfs=true")
                RMPSoup = BeautifulSoup(actualRMPURL.content.decode('utf-8', 'ignore'), "lxml")

                #Add name to dictionary
                condensedProfData["name"] = profName

                #Add URL to dictionary
                RMPURL = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(profID) + "&showMyProfs=true"
                condensedProfData["RateMyProfessorURL"] = RMPURL

                #Add Quality to dictionary
                overallQuality = RMPSoup.find("div", {"class":"RatingValue__Numerator-qw8sqy-2 gxuTRq"}).text.strip()
                condensedProfData["Overall Quality"] = overallQuality

                #Add Would Take Again and Difficulty to dictionary
                description = ["Would Take Again", "Difficulty"]
                descriptionNumber = 0
                for grade in RMPSoup.findAll("div", {"class":"FeedbackItem__FeedbackNumber-uof32n-1 bGrrmf"}):
                    condensedProfData[description[descriptionNumber]] = grade.text.strip()
                    descriptionNumber+=1

                #Add number of reviews to dictionary
                reviewDiv = RMPSoup.find("div", {"class":"RatingValue__NumRatings-qw8sqy-0 jvzMox"})
                numberOfReviews = reviewDiv.find("a").text.strip()
                print(numberOfReviews)
                numberOfReviews = numberOfReviews.replace('\xa0', ' ') #Replaces BS4 space with an actual space so that the JSON can be parsed properly
                condensedProfData["numberOfReviews"] = numberOfReviews

                #Add school teaching at to dictionary
                schoolDiv = RMPSoup.find("div", {"class":"NameTitle__Title-dowf0z-1 wVnqu"})
                deptAndSchool = schoolDiv.find("a").text.strip()
                condensedProfData["departmentAndSchool"] = deptAndSchool

                #--END DATA GATHERING--
                RMPData[profName] = condensedProfData

            else:
                TeachersWithNoReviews.append(professor)
        else:
            TeachersWithoutEntries.append(professor)

    profData["NoReviews"] = TeachersWithNoReviews
    profData["NoEntries"] = TeachersWithoutEntries
    return RMPData

#Run Project
#GetRMPData("https://webapp4.asu.edu/catalog/classlist?t=2207&s=CSE&n=110&hon=F&promod=F&e=open&page=1")
