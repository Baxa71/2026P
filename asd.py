import pandas as pd
from sklearn.linear_model import LinearRegression

# 1. ТӘЖІРИБЕЛІК ДЕРЕКТЕР ЖИНАҒЫ (Модельді үйретуге арналған)
data = {
    'BJB_TJB': [85, 90, 45, 60, 95, 70, 50, 88, 65, 40],[cite: 2]
    'Attendance': [95, 98, 70, 80, 100, 85, 75, 92, 85, 60],[cite: 2]
    'Homework': [90, 95, 50, 65, 98, 75, 55, 90, 70, 45],[cite: 2]
    'Final_Grade': [89, 93, 50, 67, 97, 74, 56, 90, 71, 43][cite: 2]
}

df = pd.DataFrame(data)[cite: 2]

# 2. МОДЕЛЬДІ ОҚЫТУ
X = df[['BJB_TJB', 'Attendance', 'Homework']][cite: 1, 2]
y = df['Final_Grade'][cite: 2]

model = LinearRegression()[cite: 1, 2]
model.fit(X, y)[cite: 2]

print("=== ОҚУШЫ АЛДЫН АЛА БОЛЖАУ ЖҮЙЕСІ ===")

# 3. ҚОЛДАНУШЫДАН МӘЛІМЕТТЕРДІ ЕНГІЗУ
try:
    bjb = float(input("БЖБ/ТЖБ орташа балын енгізіңіз (0-100): "))
    attendance = float(input("Сабаққа қатысу пайызын енгізіңіз (0-100%): "))
    homework = float(input("Үй тапсырмасының орындалу пайызын енгізіңіз (0-100%): "))

    # 4. БОЛЖАМ ЕСЕПТЕУ
    new_student = [[bjb, attendance, homework]][cite: 2]
    predicted_grade = model.predict(new_student)[0][cite: 2]

    # 5. НӘТИЖЕНІ ШЫҒАРУ
    print("\n--- БОЛЖАМ САТЫСЫ ---")
    print(f"Болжамды тоқсандық балл: {predicted_grade:.1f} балл")[cite: 2]

    if predicted_grade < 60:[cite: 1, 2]
        print("Статус: ⚠️ Тәуекел тобында! Қосымша сабақтар қажет.")[cite: 1, 2]
    else:
        print("Статус: ✅ Үлгерім деңгейі жеткілікті.")[cite: 2]

except ValueError:
    print("Қате: Тек сандарды енгізіңіз!")