import csv
import random

#Person Class
class Person:
    def __init__ (self, id, courses, alts, outsides, linear):
        self.id = id
        self.courses = courses
        self.mainRequests = courses[:]
        self.alts = alts
        self.altRequests = alts[:]
        self.outsides = outsides
        self.linear = linear
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
        self.isLinear = False
    
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
        
for x in range(1):
    if x % 100 == 0:
        print(str(x))

    #Main   
    people = []
    classes = []
    tempCourses = []
    altCourses = []
    outsides = []
    id = 0
    linear = [] 
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

    # new metrics
    allMain = []
    oneLessMain = []
    twoLessMain = []

    allWithAlt = []
    oneLessWithAlt = []
    twoLessWithAlt = []

    outside_the_timetable = [
        'XC---09--L', 'MDNC-09C-L', 'MDNC-09M-L', 'XBA--09J-L', 'XLDCB09S-L', 'YCPA-0AX-L',
        'MDNCM10--L', 'YED--0BX-L', 'MMUCC10--L', 'YCPA-0AXE-', 'MMUOR10S-L', 'MDNC-10--L',
        'MIDS-0C---', 'MMUJB10--L', 'MDNC-11--L', 'YCPA-1AX-L', 'MDNCM11--L', 'YCPA-1AXE-',
        'MGRPR11--L', 'MGMT-12L--', 'YED--1EX-L', 'MWEX-2A--L', 'MCMCC11--L', 'MWEX-2B--L',
        'MIMJB11--L', 'MMUOR11S-L', 'MDNC-12--L', 'YCPA-2AX-L', 'MDNCM12--L', 'YCPA-2AXE-',
        'MGRPR12--L', 'MGMT-12L--', 'YED--2DX-L', 'YED--2FX-L', 'MCMCC12--L', 'MWEX-2A--L',
        'MIMJB12--L', 'MWEX-2B--L', 'MMUOR12S-', ''
    ]

    linear_courses = []

    #Methods
    def getCourse(courseID):
        for course in classes:
            if(course.classID == courseID):
                return course
        return False

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
            csvwriter.writerow(["A","B","C","D","A","B","C","D", "Outside"])
            
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

        with open("students.csv", 'w', newline="") as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            
            for std in people:
                outsideCourses = ""
                csvwriter.writerow([std.id])
                for i in range(8):
                    course = ""
                    for block in std.timetable[i]:
                        course += str(block) + ", "
                    csvwriter.writerow(["Semester: " + str(i // 4 + 1) + ", Block: " + chr(i % 4 + 65), course])
                for block in std.timetable[8]:
                    outsideCourses += "["
                    for course in block.courses:
                        outsideCourses += course.name + ","
                    outsideCourses += "]"
                csvwriter.writerow(["Outside", outsideCourses])
                csvwriter.writerow([])

        with open("scores.csv", 'w', newline="") as csvfile:

            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Scores"])
            csvwriter.writerow([str(len(allMain) / len(people) + len(oneLessMain) / len(people) + len(twoLessMain) / len(people))])
            csvwriter.writerow([str(len(allWithAlt) / len(people) + len(oneLessWithAlt) / len(people) + len(twoLessWithAlt) / len(people))])
            

    def giveSequences (personsRequests, student):
        for request in personsRequests:

            # checking if sequencing rule applies for this request
            if request in sequencing.keys():
            
                for course in sequencing[request]:
                    if (course in personsRequests):
                        
                        # if they get the prerequisite course in first semester, try to give the next course
                        if (giveCourse(request, [0, 1, 2, 3], student)):
                            student.courses.remove(request)
                            if (giveCourse(course, [4, 5, 6, 7], student)):
                                student.courses.remove(course)
                            break
                        
                        # try to give prerequisite in second semester
                        if(giveCourse(request, [4, 5, 6, 7], student)):
                            student.courses.remove(request)
                    
    def giveCourse(request, periods, student):
        # random.shuffle(periods)
        
        # loop through periods
        for period in periods:

            # check if period is available (if the student does not already have a course in it)
            if (len(student.timetable[period]) > 0):
                continue

            # loop through blocks in globalTimetable[currPeriod]
            for block in globalTimetable[period]:
                
                # check if requested course is in this block
                if (request not in block.courses):
                    continue
                        
                
                # check if max enrolment reached (or remove from availableClasses)
                if (block not in availableClasses):
                    continue

                if (len(block.studentList) >= int(block.maxEnrollment)): 
                    availableClasses.remove(block)
                    continue
                
                # add student to block
                student.timetable[period].append(block)
                block.studentList.append(student)
                return True

        # loop through periods (and shuffle?)
        # random.shuffle(periods)
        
        for period in periods:
            
            # check if period is available and remove period if not?
            if (len(student.timetable[period]) > 0):
                periods.remove(period)
                continue
            
            # create block
            tempBlockCourses = [request]
            for blocking in courseBlocking:
                if request in blocking:
                    tempBlockCourses = blocking
                    break

            # check if max sections reached
            if tempBlockCourses[0].sections >= tempBlockCourses[0].maxSections:
                continue

            # update number of sections for each course in block
            for course in tempBlockCourses:
                course.sections = course.sections + 1

            # create block
            newBlock = Block(tempBlockCourses)

            # add student to block, add block to globalTimetable
            newBlock.studentList.append(student)
            student.timetable[period].append(newBlock)
            globalTimetable[period].append(newBlock)
            availableClasses.append(newBlock)
            return True
        return False

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

    def getLeastBlocks():
        lengths = []
        x = 0
        

        while(len(lengths) < 8):
            
            for i in range(8):
                if len(globalTimetable[i]) == x:
                    lengths.append(i)

            x = x + 1
        return lengths
        # sort

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

    # gives the student their main requests if available
    def giveAvailableCourses(requestedCourses, student, currBlock):     

        for wantedCourse in requestedCourses:
            blockFound = False

            # give courses that already exist
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

                for blockWithLowestCourses in getLeastBlocks():
                    if len(student.timetable[blockWithLowestCourses]) > 0:
                        # currBlock = currBlock + 1      
                        # if(currBlock == 8):
                        #     currBlock = 0
                        continue

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
                    
                    # otherBlock = currBlock - 4 if currBlock >= 4 else currBlock + 4


                    newBlock = Block(tempBlockCourses)
                    newBlock.studentList.append(student)
                    student.timetable[blockWithLowestCourses].append(newBlock)
                    globalTimetable[blockWithLowestCourses].append(newBlock)
                    availableClasses.append(newBlock)
                    # currBlock = currBlock + 1      
                    # if(currBlock == 8):
                    #     currBlock = 0
                    break

                    # if tempBlockCourses[0].isLinear:
                    #     globalTimetable[otherBlock].append(newBlock)
                    #     student.timetable[otherBlock].append(newBlock)

                
        return currBlock # TODO: temp

    # gives students their alt requests if available
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

                    # check if max enrolment reached
                    if (len(block.studentList) >= int(block.maxEnrollment)): 
                        availableClasses.remove(block)
                        continue

                    # check if wanted course found
                    if (course in block.courses):
                        student.timetable[period].append(block)
                        block.studentList.append(student)
                        altCourses.remove(course)
                        foundCourse = True
                        break
                    
                if(foundCourse):
                    break

        availableBlocks = [0, 1, 2, 3, 4, 5, 6, 7]

        # while they still have empty periods or there are still unfulfilled alt requests
        while (len(altCourses) > 0 and len(availableBlocks) > 0):
            rand = random.randint(0, len(availableBlocks)-1)
            # if there is already a course in this period, continue
            if len(student.timetable[availableBlocks[rand]]) > 0:
                availableBlocks.remove(availableBlocks[rand])
                continue   
            
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
            student.timetable[availableBlocks[rand]].append(newBlock)
            globalTimetable[availableBlocks[rand]].append(newBlock)
            availableClasses.append(newBlock)
            altCourses.remove(altCourses[0])

    def giveLinearCourses(linearCourses, student):
        for period in range(8):
            altPeriod = period - 4 if period >= 4 else period + 4
            foundCourse = False
            
            # if there is already a course in this period, continue
            if len(student.timetable[period]) > 0:
                continue

            # loop through linear requests
            for course in linearCourses:
                for block in globalTimetable[period]:
                    
                    # checks if max enrolment reached
                    if (block not in availableClasses):
                        continue

                    # check if wanted course found
                    if (course in block.courses):
                        student.timetable[period].append(block)
                        student.timetable[altPeriod].append(block)
                        block.studentList.append(student)
                        linearCourses.remove(course)
                        for lincourse in block.courses:
                            if lincourse in student.courses:
                                student.courses.remove(lincourse)
                            elif lincourse in student.alts:
                                student.alts.remove(lincourse)
                            elif lincourse in linearCourses:
                                linearCourses.remove(lincourse)
                        foundCourse = True
                        break
                    
                if(foundCourse):
                    break

        availableBlocks = [0, 1, 2, 3, 4, 5, 6, 7]

        # while they still have empty periods or there are still unfulfilled alt requests
        while (len(linearCourses) > 0 and len(availableBlocks) > 0):
            rand = random.randint(0, len(availableBlocks)-1)
            otherPeriod = availableBlocks[rand] - 4 if availableBlocks[rand] >= 4 else availableBlocks[rand] + 4

            # if there is already a course in this period, continue
            if len(student.timetable[availableBlocks[rand]]) > 0 or len(student.timetable[otherPeriod]) > 0:
                availableBlocks.remove(availableBlocks[rand])
                continue   
            
            tempBlockCourses = [linearCourses[0]]
            for blocking in courseBlocking:
                if linearCourses[0] in blocking:
                    tempBlockCourses = blocking
                    break
            
            # if max sections reached, break
            if tempBlockCourses[0].sections >= tempBlockCourses[0].maxSections:
                linearCourses.remove(linearCourses[0])
                for lincourse in tempBlockCourses:
                    if lincourse in student.courses:
                        student.courses.remove(lincourse)
                    elif lincourse in student.alts:
                        student.alts.remove(lincourse)                        
                    elif lincourse in linearCourses:
                            linearCourses.remove(lincourse)
                continue

            # update number of sections for each course in block
            for course in tempBlockCourses:
                course.sections = course.sections + 1

            newBlock = Block(tempBlockCourses)
            newBlock.studentList.append(student)
            student.timetable[availableBlocks[rand]].append(newBlock)
            globalTimetable[availableBlocks[rand]].append(newBlock)
            
            globalTimetable[otherPeriod].append(newBlock)
            student.timetable[otherPeriod].append(newBlock)

            availableClasses.append(newBlock)
            linearCourses.remove(linearCourses[0])
            for lincourse in tempBlockCourses:
                if lincourse in student.courses:
                    student.courses.remove(lincourse)
                elif lincourse in student.alts:
                    student.alts.remove(lincourse)
                elif lincourse in linearCourses:
                    linearCourses.remove(lincourse)
                                            
    # give outside of timetable courses to students
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
    # sorts list of students by number of fulfilled requests, then by ID
    def sortStudents(students):
        temp = []
        sorted = []

        # sort students by id
        sortStudentsByID(students)

        # create separate list for each amount of fulfilled course requests
        temp = sortStudentsByFulfilled(students)

        # append lists together
        for x in reversed(range(len(temp))):
            sorted += temp[x]

        return sorted

    # sorts list of students by ID
    def sortStudentsByID(students):
        students.sort(key=lambda student: int(student.id))
        return students

    # returns a list of 9 lists of students (0 - 8 fulfilled requests)
    def sortStudentsByFulfilled(students):
        fulfilled = [[],[],[],[],[],[],[],[],[]]

        # loop through students
        for student in students:
            # print(student.id + "'s fulfilled requests: ", end="")
            fulfilledRequests = 0
            
            # loop through each period
            for period in student.timetable[0:8]:

                # check if block is not empty
                if (len(period) > 0):
                    fulfilledRequests += 1

            # print(fulfilledRequests)
            # print()
            fulfilled[fulfilledRequests].append(student)

        
        return fulfilled
    #Main

    #Fills the classes array with each class
    with open('data/Course Information.csv') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if (row[0] != "" and row [2] != ""):
                newCourse = Course(row[0], row[2], row[7], row[8], row[9], row[10], row[14])
                if(newCourse.classID in outside_the_timetable):
                    newCourse.outsideTimetable = True
                elif (newCourse.classID[-1] == "L"):
                    newCourse.isLinear = True
                    linear_courses.append(row[0])
                classes.append(newCourse)
                
    for course in classes:
        if course.classID in outside_the_timetable:
            course.outsideTimetable = True

    with open('data/Updated Course Information.csv') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if (row[0] == "" and row [1] != "Number" and row[1] != ""):
                if not getCourse(row[1]):
                    # print(row[1] + " doesn't exist")
                    continue
                
                if (getCourse(row[1]).maxSections != int(float(row[13]))):
                    getCourse(row[1]).maxSections = int(float(row[13]))
                    # print(row[1] + " changed")
        

        
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
                person = Person(id, tempCourses, altCourses, outsides, linear)
                id = row[1]
                tempCourses = []
                altCourses = []
                outsides = []
                linear = []
                people.append(person)
            elif not getCourse(row[0]):
                continue  
            elif getCourse(row[0]).outsideTimetable:
                outsides.append(getCourse(row[0]))
            elif getCourse(row[0]).isLinear:
                linear.append(getCourse(row[0]))
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

    random.shuffle(people)

    for p in people:
        giveLinearCourses(p.linear, p)

    for p in people:
        giveSequences(p.courses, p)

    for p in people:
        currBlock = giveAvailableCourses(p.courses, p, currBlock)

    for p in people:
        giveAltCourses(p.alts, p)

    for p in people:
        giveOutsideCourses(p.outsides, p)

    score = scoreTimetable(score)

    fullTimetableStudents = []
    fullAltTimetableStudents = []

    spares = [0]*9
    requestsFulfilled = [0]*9

    for std in people:
        numCourses = 0
        mainFulfilled = 0

        # counting main requests and fulfilled main requests
        for course in std.courses:
            maxReqCourseScore += 1
            for i in range(len(std.timetable)-1):
                for block in std.timetable[i]:
                    if course in block.courses:
                        reqCourseScore += 1
                        break

        # counting students with 8/8 courses (requested only)
        fullTimetable = True
        for period in std.timetable[0:8]:
            if (len(period) == 0):
                fullTimetable = False
                break
            for block in period:
                isRequested = False
                for course in block.courses:
                    if course in std.courses or course in std.linear:
                        isRequested = True
                if not isRequested:
                    fullTimetable = False
                    break
            if not fullTimetable:
                break
        if(fullTimetable):
            numReqTimetable += 1   
            fullTimetableStudents.append(std)
        
        # counting students with 8/8 courses (requested or alternate)
        fullTimetable = True
        for period in std.timetable[0:8]:
            if (len(period) == 0):
                fullTimetable = False
                break
            for block in period:
                isRequested = False
                for course in block.courses:
                    if ((course in std.courses) or std.linear or
                         (course in std.altRequests)):
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

        # counting num of spares
        numSpares = 0
        for period in std.timetable[0:8]:
            if (len(period) == 0):
                numSpares += 1
                continue
            for course in period[0].courses:
                if course in std.mainRequests or course in std.linear:
                    mainFulfilled += 1
                    break
                
        spares[numSpares] += 1
        requestsFulfilled[mainFulfilled] += 1
    
    # sort Students
    people = sortStudents(people)

    # calculate and print new metrics

    for std in people:
        mainFulfilled = 0
        fulfilledCourses = 0

        # count number of main requests
        numMainRequests = len(std.mainRequests)
        # count alt requests (?)
        numAltRequests = len(std.altRequests)


        # loop through periods of timetable
        for period in std.timetable[0:8]:
            if len(period) == 0:
                continue

            fulfilledCourses += 1
            # loop through courses in this block
            for course in period[0].courses:
                # check if fulfills main or alt request
                if course in std.mainRequests:
                    mainFulfilled += 1
                    break


        # add student to list of fulfillsAll, oneLess, twoLess
        if mainFulfilled == numMainRequests:
            allMain.append(std)
        elif mainFulfilled == numMainRequests - 1:
            oneLessMain.append(std)
        elif mainFulfilled == numMainRequests - 2:
            twoLessMain.append(std)

        total = numMainRequests + numAltRequests
        if (total > 8):
            total = 8
        
        if fulfilledCourses == total:
            allWithAlt.append(std)
        elif fulfilledCourses == total - 1:
            oneLessWithAlt.append(std)
        elif fulfilledCourses == total - 2:
            twoLessWithAlt.append(std)


    print("main requests fulfilled: " + str(reqCourseScore / maxReqCourseScore))
    print("main/alt requests fulfilled: " + str((reqCourseScore + altCourseScore) / (maxReqCourseScore + maxAltCourseScore)))
    print()
    print("All main requests fulfilled: " + str(len(allMain) / len(people)))
    print("One main request not fulfilled: " + str(len(oneLessMain) / len(people)))
    print("Two main requests not fulfilled: " + str(len(twoLessMain) / len(people)))
    print("Sum: " + str(len(allMain) / len(people) + len(oneLessMain) / len(people) + len(twoLessMain) / len(people)))
    print()
    print("All main or alt requests fulfilled: " + str(len(allWithAlt) / len(people)))
    print("One main or alt request not fulfilled: " + str(len(oneLessWithAlt) / len(people)))
    print("Two main or alt requests not fulfilled: " + str(len(twoLessWithAlt) / len(people)))
    print("Sum: " + str(len(allWithAlt) / len(people) + len(oneLessWithAlt) / len(people) + len(twoLessWithAlt) / len(people)))
    print()
    print("Students with 3-8 not fulfilled (main and alt): " + str((len(people) - len(allWithAlt) - len(oneLessWithAlt) - len(twoLessWithAlt)) / len(people)))

print("Done")
writeToCSV()

