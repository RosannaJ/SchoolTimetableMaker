import csv

#Person Class
class Person:
    def __init__ (self, id, courses, alts):
        self.id = id
        self.courses = courses
        self.alts = alts
        self.timetable = Timetable()

    def __str__(self):
        return f'\n>>>>>>>>>>>>>\nID is {self.id} \n {self.courses} \n {self.alts} \n>>>>>>>>>>>>>\n'
    
    def __repr__(self):
        return self.__str__()
    
    def getID(self):
        return self.id
    
    def getCourses(self):
        return self.courses
    
    def getAlts(self):
        return self.alts

#Course Class   
class Course:
    def __init__(self, classID, name, baseTermsPerYear , coveredTermsPerYear, maxEnrollment, PPC, sections):
        self.classID = classID
        self.name = name
        self.baseTermsPerYear = baseTermsPerYear
        self.coveredTermsPerYear = coveredTermsPerYear
        self.maxEnrollment = maxEnrollment
        self.PPC = PPC
        self.sections = sections
    
    def __str__(self):
        return f'\n>>>>>>>>>>>>>\n{self.classID}: {self.name} \n{self.baseTermsPerYear}, {self.coveredTermsPerYear} \n{self.maxEnrollment}, {self.PPC}, {self.sections} \n>>>>>>>>>>>>>\n'
    
    def __repr__(self):
        return self.__str__()
    
    def getMaxEnroll(self):
        return self.maxEnrollment

class Timetable:
    def __init__(self):
        self.assignedCourses = []
        
    def addCourse(self, course):
        self.assignedCourses.append(course)

class Block:
    def __init__(self, course):
        self.courses = course #this stores the course object
        self.maxEnrollment = Course.getMaxEnroll(course[0])
        self.studentList = []

#Main   
people = []
classes = []
tempCourses = []
altCourses = []
id = 0
first = True



globalTimetable = [[], [], [], [], [], [], [], []] #indexes 0 - 7 represent all 8 blocks in both semesters
    
with open('data/requests.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        #resetting temp arrays + saving previous person to people array
        if (first):
            id = row[1]
            first = False
            continue
        if (row[0] == "Course"):
            continue
        if (row[0] == "ID"):
            person = Person(id, tempCourses, altCourses)
            ##print(tempCourses)
            ##print(person)
            id = row[1]
            tempCourses = []
            altCourses = []
            people.append(person)
            
        elif (row[11] == "Y"):
            altCourses.append(row[0])
        else: tempCourses.append(row[0])

with open('data/Course Information.csv') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        #print(row)
        if (row[0] != "" and row [1] != ""):
            newCourse = Course(row[0], row[2], row[7], row[8], row[9], row[10], row[14])
            classes.append(newCourse)


courseBlocking = []

with open("data/Course Blocking Rules.csv") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if(row[1] == "Course - Blocking"):
            string = row[2].split(",")
            temp = []
            for i in len(string):
                if(i == 0):
                    temp.append(string[i].split(" ")[1])
                elif(i == len(string) - 1):
                    temp.append(string[i].split(" ")[0])
                else:
                    temp.append[i]
            courseBlocking.append(temp)

for i in courseBlocking:
    print(i)

#print(classes)

