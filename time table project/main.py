import csv

#Person Class
class Person:
    def __init__ (self, id, courses, alts):
        self.id = id
        self.courses = courses
        self.alts = alts
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
        self.sections = sections
    
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
id = 0
first = True

allBlocks = []

##stores sequecning
sequencing = {}

globalTimetable = [[], [], [], [], [], [], [], []] #indexes 0 - 7 represent all 8 blocks in both semesters, index 8 is outside timetable

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
            for x in range(8):
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
        for block in student.timetable[i]:
            semester = 1
            if(i > 3):
                semester = 2
            print("Semester: " + str(semester) + ", Block: " + chr(i % 4 + 65) + "  ", end="")
            for course in block.courses:
                if (course in student.courses):
                    print(course.name, end="")
            print()
    print("Outside Timetable: ")
    for block in student.timetable[8]:
        for course in block.courses:
            print(course.name, end=", ")

def getFullestBlock():
    max = 0
    maxIndex = 0
    for i in range(len(globalTimetable)):
        if len(globalTimetable[i]) > max:
            maxIndex = i
            max = len(globalTimetable[i])
    return maxIndex


#Main

#Fills the classes array with each class
with open('data/Course Information.csv') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if (row[0] != "" and row [2] != ""):
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
            id = row[1]
            tempCourses = []
            altCourses = []
            people.append(person)
            
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

currBlock = 0
blockFound = False
availableClasses = [] # stores classes that are not at max capacity
    
temp = 0


for p in people:
    # print(p.id)

    for wantedCourse in p.courses: # breaks out of this loop if block found
        # print("requesting: ", end="")
        # print(wantedCourse.classID, end=" ")
        blockFound = False
        for period in globalTimetable:

            for block in period:
                if wantedCourse in block.courses:
                    if block not in availableClasses:
                        continue

                    #if the requested class is found and not at max capacity, add student
                    if (len(block.studentList) < int(block.maxEnrollment) and len(p.timetable[currBlock]) == 0): 
                        block.studentList.append(p)
                        p.timetable[currBlock].append(block)
                        blockFound = True
                        

                        currBlock = currBlock + 1
                        if(currBlock == 8):
                            currBlock = 0
                        break

                    # remove the block from availableClasses if at max capacity
                    else:
                        availableClasses.remove(block)
            if(blockFound):
                break
        
        #if there is no course that the student wants in the schedule, make new course
        if(not blockFound):
            # print("creating new block")
            tempBlockCourses = [wantedCourse]
            for blocking in courseBlocking:
                if wantedCourse in blocking:
                    tempBlockCourses = blocking
                    break
            newBlock = Block(tempBlockCourses)
            newBlock.studentList.append(p)
            p.timetable[currBlock].append(newBlock)
            globalTimetable[currBlock].append(newBlock)
            availableClasses.append(newBlock)
            currBlock = currBlock + 1
            if(currBlock == 8):
                     currBlock = 0

# printGlobalTimetable()

score = 0
maxScore = 0

# scoring the timetable
for student in people:
    for period in student.timetable:
        maxScore = maxScore + 2

        for block in period:
            for course in student.courses:
                if (course in block.courses):
                    score = score + 2
            for course in student.alts:
                if (course in block.courses):
                    score = score + 1           

#printAllCourses()
writeToCSV()
print("Score: " + str(score))
print("Max Score: " + str(maxScore))
print("Percent: " + str(score / maxScore))
print()
printStudentTimetable(getStudent("1278"))
printStudentTimetable(getStudent("1002"))
