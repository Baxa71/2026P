class Student:
    school="KBTU"
    def __init__(self, name):
        self.name=name
student1=input("name1")
student2=input("name2")
s1 = Student(student1)
s2 = Student(student2)
print(f"Stud 1: {s1.name}, unik: {s1.school}")
print(f"Stud 2: {s2.name}, unik: {s2.school}")