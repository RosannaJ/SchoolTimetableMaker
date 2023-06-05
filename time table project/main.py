import csv
import random

#Person Class
class Person:
    def __init__ (self, id, courses, alts, outsides):
        self.id = id
        self.courses = courses
        self.alts = alts
        self.altRequests = alts[:]
        self.outsides = outsides
        self.timetable = [[], [], [], [], [], [], [], [], []]

    def __str__(self):
        return f'\n{self.id}'
    
    def __repr__(self):
        return self.__str__()

#Course Class   
class Course:
    def __init__(self, classID, name, baseTermsPerYear, coveredTermsPerYear, maxEnrollment, PPC, sections):
        self.classID = classID
        self.name = name
        self.baseTermsPerYear = baseTermsPerYear
        self.coveredTermsPerYear = coveredTermsPerYear
        self.maxEnrollment = maxEnrollment
        self.PPC = PPC
        self.maxSections = int(sections)
        self.outsideTimetable = False
        self.sections = 0
    
    def __str__(self):
        return f'\n>>>>>>>>>>>>>\n{self.classID}: {self.name} \n Max: {self.maxEnrollment}\n>>>>>>>>>>>>>\n'
    
    def __repr__(self):
        return self.__str__()

#Block Class
class Block:
    def __init__(self, course):
        self.courses = course #this stores the course object
        self.maxEnrollment = self.courses[0].maxEnrollment
        self.studentList = []
        # self.sections

    def __repr__(self):
        return f'\n\nCourses in block: {self.courses}\n Students in: {self.studentList}'# Max enrollment: {self.maxEnrollment} \n Students: {self.studentList}'

    def __str__(self):
        txt = ""
        for course in self.courses:
            txt += course.name + ", "
        return txt
        

#Main   
people = []
classes = []
tempCourses = []
altCourses = []
outsides = []
id = 0
first = True

##stores sequecning
sequencing = {}

globalTimetable = [[], [], [], [], [], [], [], [], []] #indexes 0 - 7 represent all 8 blocks in both semesters, index 8 is outside timetable
availableClasses = [] # stores classes that are not at max capacity

score = 0
reqCourseScore = 0
maxReqCourseScore = 0
altCourseScore = 0
maxAltCourseScore = 0
numReqTimetable = 0         # students with 8/8 requested courses
numReqAltTimetable = 0      # students with 8/8 requested or alt courses


outside_the_timetable = [
    'XC---09--L', 'MDNC-09C-L', 'MDNC-09M-L', 'XBA--09J-L', 'XLDCB09S-L', 'YCPA-0AX-L',
    'MDNCM10--L', 'YED--0BX-L', 'MMUCC10--L', 'YCPA-0AXE-', 'MMUOR10S-L', 'MDNC-10--L',
    'MIDS-0C---', 'MMUJB10--L', 'MDNC-11--L', 'YCPA-1AX-L', 'MDNCM11--L', 'YCPA-1AXE-',
    'MGRPR11--L', 'MGMT-12L--', 'YED--1EX-L', 'MWEX-2A--L', 'MCMCC11--L', 'MWEX-2B--L',
    'MIMJB11--L', 'MMUOR11S-L', 'MDNC-12--L', 'YCPA-2AX-L', 'MDNCM12--L', 'YCPA-2AXE-',
    'MGRPR12--L', 'MGMT-12L--', 'YED--2DX-L', 'YED--2FX-L', 'MCMCC12--L', 'MWEX-2A--L',
    'MIMJB12--L', 'MWEX-2B--L', 'MMUOR12S-'
]

#Methods
def getCourse(courseID):
    for course in classes:
        if(course.classID == courseID):
            return course

def printGlobalTimetable(): #prints the classes in each block (without printing students)
    x = 0
    for period in globalTimetable:
        print()
        print("PERIOD: ", end="")
        print(x)
        print()

        x = x + 1
        for block in period:
            for course in block.courses:
                print(course.classID, end=" ")
            print(":", end=" ")
            for student in block.studentList:
                print(student.id, end=",")
            print()

# write globalTimetable to CSV
def writeToCSV():  

    # writing to csv file
    with open("output.csv", 'w', newline="") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        
        # write the headings
        csvwriter.writerow(["Semester 1", "", "", "", "Semester 2"])
        csvwriter.writerow(["A","B","C","D","A","B","C","D"])
        
        # writing data
        fullestBlock = getFullestBlock()
        txt = []

        # loop through each row of the table
        for row in range(len(globalTimetable[fullestBlock])):
            # loop through blocks (A to D in each semester)
            for x in range(9):
                # skip column if no more courses in this block
                if len(globalTimetable[x]) <= row:
                    txt.append("")
                    continue
                txt.append(str(globalTimetable[x][row]))
            csvwriter.writerow(txt)
            txt = []
            

def drawLine(x):
    txt = ""
    for i in range(x):
        txt += "-"
    return txt

def drawTableHeading(semester):
    txt = drawLine(183) + "\n"
    txt += "{:^183}|\n".format("Semester" + str(semester))
    txt += drawLine(183) + "|\n"
    txt += "{:^45}|{:^45}|{:^45}|{:^45}|\n".format("A", "B", "C", "D")
    txt += drawLine(183) + "|\n"
    return txt

def printAllCourses():

    # print semester 1
    txt = drawTableHeading(1)
    fullestBlock = getFullestBlock()

    # loop through each row of the table
    for row in range(len(globalTimetable[fullestBlock])):
        # loop through blocks (A to D)
        for x in range(4):
            # continue if no more courses in this block
            if len(globalTimetable[x]) <= row:
                txt += "{:<45}|".format()
                continue
            txt += "{:<45}|".format(str(globalTimetable[x][row]))
        txt += "\n"
    print(txt)

    # print semester 2
    txt = drawTableHeading(2)
    fullestBlock = getFullestBlock()
    for row in range(len(globalTimetable[fullestBlock])):
        for x in range(4,8):
            if len(globalTimetable[x]) <= row:
                txt += "{:<45}|".format()
                continue
            txt += "{:<45}|".format(str(globalTimetable[x][row]))
        txt += "\n"
    print(txt)

def getStudent(id):
    student = None
    for person in people:
        if person.id == id:
            student = person
    return student

def printStudentTimetable(student):
    print("Student " + str(student.id) + "'s Timetable:")
    for i in range(8):
        print("Semester: " + str(i // 4 + 1) + ", Block: " + chr(i % 4 + 65), end=" ")
        for block in student.timetable[i]:
            print(str(block), end="")
        print()
    print("Outside Timetable: ", end="")
    for block in student.timetable[8]:
        print("[", end="")
        for course in block.courses:
            print(course.name, end=", ")
        print("]" , end="")
    print()
    print()
            
def scoreTimetable(tempScore):
    # scoring the timetable
    for student in people:
        for block in student.timetable:

            if (len(block) == 0):
                # print("add to Score")
                tempScore += 1
                
    return tempScore

def getFullestBlock():
    max = 0
    maxIndex = 0
    for i in range(len(globalTimetable)):
        if len(globalTimetable[i]) > max:
            maxIndex = i
            max = len(globalTimetable[i])
    return maxIndex

def giveAvailableCourses(requestedCourses, student, currBlock):
    for wantedCourse in requestedCourses:
        blockFound = False
        for currPeriod in range(8):

            # if there's already a course in this period, continue
            if len(student.timetable[currPeriod]) > 0:
                continue
            for block in globalTimetable[currPeriod]:
                if wantedCourse in block.courses:
                    
                    # check if block is at max capacity
                    if block not in availableClasses:
                        continue

                    #if the requested class is found and not at max capacity, add student
                    if (len(block.studentList) + 1 <= int(block.maxEnrollment)): 
                        
                        block.studentList.append(student)
                        student.timetable[currPeriod].append(block)
                        blockFound = True
                        break

                    # remove the block from availableClasses if at max capacity
                    else:
                        availableClasses.remove(block)
            if(blockFound):
                break
        
        #if there is no course that the student wants in the schedule, make new course
        if(not blockFound):
            tempBlockCourses = [wantedCourse]
            for blocking in courseBlocking:
                if wantedCourse in blocking:
                    tempBlockCourses = blocking
                    break

            # if max sections reached, break
            if tempBlockCourses[0].sections >= tempBlockCourses[0].maxSections:
                break

            # update number of sections for each course in block
            for course in tempBlockCourses:
                course.sections = course.sections + 1

            newBlock = Block(tempBlockCourses)
            newBlock.studentList.append(student)
            student.timetable[currBlock].append(newBlock)
            globalTimetable[currBlock].append(newBlock)
            availableClasses.append(newBlock)
            currBlock = currBlock + 1
            if(currBlock == 8):
                currBlock = 0
    return currBlock # TODO: temp

def giveAltCourses(altCourses, student):
    for period in range(8):
        foundCourse = False
        
        # if there is already a course in this period, continue
        if len(student.timetable[period]) > 0:
            continue

        # loop through alt requests
        for course in altCourses:
            for block in globalTimetable[period]:
                
                # checks if max enrolment reached
                if (block not in availableClasses):
                    continue

                # check if wanted course found
                if (course in block.courses):
                    student.timetable[period].append(block)
                    block.studentList.append(student)
                    altCourses.remove(course)
                    foundCourse = True
                    print("added to " + str(block))
                    break
                
            if(foundCourse):
                break

    availableBlocks = [0, 1, 2, 3, 4, 5, 6, 7]

    while (len(altCourses) > 0 and len(availableBlocks) > 0):
        rand = random.randint(0, len(availableBlocks)-1)
        # if there is already a course in this period, continue
        if len(student.timetable[availableBlocks[rand]]) > 0:
            availableBlocks.remove(availableBlocks[rand])
            continue   
        
        #print(str(rand))  
        tempBlockCourses = [altCourses[0]]
        for blocking in courseBlocking:
            if altCourses[0] in blocking:
                tempBlockCourses = blocking
                break
        
        # if max sections reached, break
        if tempBlockCourses[0].sections >= tempBlockCourses[0].maxSections:
            altCourses.remove(altCourses[0])
            continue

        # update number of sections for each course in block
        for course in tempBlockCourses:
            course.sections = course.sections + 1

        newBlock = Block(tempBlockCourses)
        newBlock.studentList.append(student)
        student.timetable[rand].append(newBlock)
        globalTimetable[rand].append(newBlock)
        availableClasses.append(newBlock)
        altCourses.remove(altCourses[0])
        #availableBlocks.remove(availableBlocks[rand])
        print("new alt course")

def giveOutsideCourses(outsides, student):
    
    for wantedCourse in outsides:
        courseFound = False        
        for block in globalTimetable[8]:
            if wantedCourse in block.courses:
                
                # check if block is at max capacity
                if block not in availableClasses:
                    continue

                #if the requested class is found and not at max capacity, add student
                if (len(block.studentList) + 1 <= int(block.maxEnrollment)): 
                    block.studentList.append(student)
                    student.timetable[8].append(block)
                    courseFound = True
                    break

                # remove the block from availableClasses if at max capacity
                else:
                    availableClasses.remove(block)

        if not courseFound:
            tempBlockCourses = [wantedCourse]
            for blocking in courseBlocking:
                if wantedCourse in blocking:
                    tempBlockCourses = blocking
                    break

            # if max sections reached, break
            if tempBlockCourses[0].sections >= tempBlockCourses[0].maxSections:
                break

            # update number of sections for each course in block
            for course in tempBlockCourses:
                course.sections = course.sections + 1

            newBlock = Block(tempBlockCourses)
            newBlock.studentList.append(student)
            student.timetable[8].append(newBlock)
            globalTimetable[8].append(newBlock)
            availableClasses.append(newBlock)

#Main

#Fills the classes array with each class
with open('data/Course Information.csv') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if (row[0] != "" and row [2] != ""):
            newCourse = Course(row[0], row[2], row[7], row[8], row[9], row[10], row[14])
            if(newCourse.classID in outside_the_timetable):
                newCourse.outsideTimetable = True
            classes.append(newCourse)
            


for course in classes:
    if course.classID in outside_the_timetable:
        course.outsideTimetable = True
    

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
            person = Person(id, tempCourses, altCourses, outsides)
            id = row[1]
            tempCourses = []
            altCourses = []
            outsides = []
            people.append(person)
            
        elif getCourse(row[0]).outsideTimetable:
            outsides.append(getCourse(row[0]))
        elif (row[11] == "Y"):
            altCourses.append(getCourse(row[0]))
        else: 
            tempCourses.append(getCourse(row[0]))

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

currBlock = 0

#random.shuffle(people)
for p in people:
    currBlock = giveAvailableCourses(p.courses, p, currBlock)
    

for p in people:

    # loop through main requests
    giveAltCourses(p.alts, p)

for p in people:

    # loop through main requests
    giveOutsideCourses(p.outsides, p)

score = scoreTimetable(score)

writeToCSV()

fullTimetableStudents = []
fullAltTimetableStudents = []

for std in people:

    # counting main requests and fulfilled main requests
    for course in std.courses:
        maxReqCourseScore += 1
        for period in std.timetable:
            for block in period:
                if course in block.courses:
                    reqCourseScore += 1

        
    # counting students with 8/8 courses (requested only)
    fullTimetable = True
    for period in std.timetable:
       # if (len(period) == 0):
          #  fullTimetable = False
        for block in period:
            isRequested = False
            for course in block.courses:
                if course in std.courses:
                    isRequested = True
            if not isRequested:
                fullTimetable = False
                break
        if not fullTimetable:
            break
    if(fullTimetable):
        numReqTimetable += 1   
        fullTimetableStudents.append(std)
        #printStudentTimetable(std)  
    

    # counting students with 8/8 courses (requested or alternate)
    fullTimetable = True
    for period in std.timetable:
        #if (len(period) == 0):
        #    fullTimetable = False
        for block in period:
            isRequested = False
            for course in block.courses:
                if ((course in std.courses) or (course in std.altRequests)):
                    isRequested = True
            if not isRequested:
                fullTimetable = False
                break
        if not fullTimetable:
            break
    if(fullTimetable):
        numReqAltTimetable += 1    
        fullAltTimetableStudents.append(std)        
    
    # count number of alt requests and fulfilled alt requests
    for alt in std.altRequests:
        maxAltCourseScore += 1
        for period in std.timetable:
            for block in period:
                if alt in block.courses:
                    altCourseScore += 1
    
print("1) " + str(score))
print("2) " + str(reqCourseScore / maxReqCourseScore))
print("3) " + str((reqCourseScore + altCourseScore) / (maxReqCourseScore + maxAltCourseScore)))
print("4) " + str(numReqTimetable / len(people)))
print("5) " + str(numReqAltTimetable / len(people)))

print()

print("3 students with full requested timetables:")

for i in range(3):
    printStudentTimetable(fullTimetableStudents[i])
