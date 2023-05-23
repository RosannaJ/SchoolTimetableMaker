import csv
import os
import copy

#Person Class
class Person:
    def __init__ (self, id, courses, alts):
        self.id = id
        self.courses = courses
        self.alts = alts
        self.timetable = Timetable()

    def __str__(self):
        return f'\n>>>>>>>>>>>>>\nID is {self.id}' #\n {self.courses} \n {self.alts} \n>>>>>>>>>>>>>\n'
    
    def __repr__(self):
        return self.__str__()
    
    
    def getID(self):
        return self.id
    
    def getCourses(self):
        return self.courses
    
    def getAlts(self):
        return self.alts


    def getID(self):
        return self.id
    
    def getCourses(self):
        return self.courses
    
    def getAlts(self):
        return self.alts

#Course Class   
class Course:
    def __init__(self, classID, name, baseTermsPerYear, coveredTermsPerYear, maxEnrollment, PPC, sections):
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
    
    def getClassID(self):
        return self.classID
            
#Timetable Class
class Timetable:
    def __init__(self):
        self.assignedCourses = []
        
        
    def addCourse(self, course):
        self.assignedCourses.append(course)

#Block Class
class Block:
    def __init__(self, course):
        self.courses = course #this stores the course object
        self.maxEnrollment = self.courses[0].maxEnrollment
        self.studentList = []

    def __repr__(self):
        return f'\n\nCourses in block: {self.courses}\n Students in: {self.studentList}'# Max enrollment: {self.maxEnrollment} \n Students: {self.studentList}'

#Main   
people = []
classes = []
tempCourses = []
altCourses = []
id = 0
first = True

allBlocks = []

##stores sequecning
sequencing = {}

globalTimetable = [[], [], [], [], [], [], [], []] #indexes 0 - 7 represent all 8 blocks in both semesters

#Methods
def getCourse(courseID):
    for course in classes:
        if(course.classID == courseID):
            return course

#Main

#Fills the classes array with each class
with open('data/Course Information.csv') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if (row[0] != "" and row [2] != ""):
            #print(row)
            newCourse = Course(row[0], row[2], row[7], row[8], row[9], row[10], row[14])
            classes.append(newCourse)

#Fills the people array with student objects containing course requests
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
            altCourses.append(getCourse(row[0]))
        else: tempCourses.append(getCourse(row[0]))

courseBlocking = [] 

#Fills the courseBlocking array with arrays of course objects that are blocked together
#Removes those courses from the original classes array
with open('data/Course Blocking Rules.csv') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if(row[1] == "Course - Blocking"):
            string = row[2].split(",")
            temp = []
            for i in range(len(string)):
                temp.append(getCourse(string[i].split(" ")[1]))
                    
            courseBlocking.append(temp)

#print(classes)

for course in classes:
    tempList = []
    tempList.append(course)
    tempBlock = Block(tempList)
    allBlocks.append(tempBlock)
    
for course in courseBlocking:
    tempBlock = Block(course)
    allBlocks.append(tempBlock)

# process sequencing run
with open('data/Course Sequencing Rules.csv') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
         if(row[1] == "Course - Sequencing"):
            string = row[2].split(" ")
            tempKey = getCourse(string[1])
            tempValues = []

            for i in range(3, len(string)):
                tempStr = string[i].replace(",", "")
                tempValues.append(getCourse(tempStr))

            sequencing.update({tempKey: tempValues})

#print(allBlocks)

currBlock = 0

blockFound = False
    
for p in people:
    for wantedCourse in p.courses:
        for period in globalTimetable:

            for block in period:
                if wantedCourse in block.courses:
                    #add course to persons timetable
                    #add person to block
                    if (len(block.studentList) < int(block.maxEnrollment)):
                        block.studentList.append(p)
                        blockFound = True
                        
                    else:
                        newBlock = Block(block.courses)
                        newBlock.studentList.append(p)
                        globalTimetable[currBlock].append(newBlock)
                        currBlock = currBlock + 1
                        if(currBlock == 8):
                            currBlock = 0
                        blockFound = True
                    break
            if(blockFound):
                break
            
        if(not blockFound):
            tempBlockCourses = [wantedCourse]
            for blocking in courseBlocking:
                if wantedCourse in blocking:
                    tempBlockCourses = blocking
                    break
            newBlock = Block(tempBlockCourses)
            newBlock.studentList.append(p)
            globalTimetable[currBlock].append(newBlock)
            currBlock = currBlock + 1
            if(currBlock == 8):
                     currBlock = 0
    
    
print(globalTimetable)
                        
            


