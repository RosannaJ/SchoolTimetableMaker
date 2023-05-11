import csv

#Person Class
class Person:
    def __init__ (self, id, courses, alts):
        self.id = id
        self.courses = courses
        self.alts = alts

    def __str__(self):
        return f'\n>>>>>>>>>>>>>\nID is {self.id} \n {self.courses} \n {self.alts} \n>>>>>>>>>>>>>\n'
    
    def __repr__(self):
        return self.__str__()

#Main   
people = []
tempCourses = []
altCourses = []
id = 0
first = True
    
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

print(people)