from django.test import TestCase

# Create your tests here.
"""
                # see if there is a student in that class with the specific phone number
                try:
                    studentInClass = tempClass.get(Student=studentNumber)
                    #Student.objects.filter(phoneNumber=studentNumber).exists()  # does the student exist?
                except:
                    print("Error: the student already exists")

                try:
                    if(Student.objects.filter(phoneNumber=studentNumber).exists()):  # if the student exists, dont do anything
                        print("An error occured. The student already exists")
                        return HttpResponse("Message Recieved")#return render(request, 'pollingSite/test.html',locals())
                    else:  # if the student doesnt exist, create the student
                        studentCreate = Student.objects.create(name=incoming_text[1], lastname=incoming_text[2], studentID=incoming_text[3], phoneNumber=studentNumber)
                        print(studentCreate)
                        # get classroom with that class key
                        Classroom.objects.get(classKey=incoming_text[4].upper()).students.add(studentCreate)
                        print("Created a student")
                except:
                    print("An error occured when trying to add a student")
                    traceback.print_exc()
                    # now only need to add the student to the class
                    #return render(request, 'pollingSite/test.html',locals
"""
