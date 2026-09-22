students=[("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sort_index=int(input())
sorted_students=sorted(students, key=lambda x: x[sort_index])
print(sorted_students)