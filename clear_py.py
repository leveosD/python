print("Задание 1")
print("1: ")
x = int(input("Введите число: "))
y = int(input("Введите число: "))
if x > y:
    print(x, "больше", y)
else:
    print(y, "больше", x)

print("2: ")
age = int(input("Введите свой возраст: "))
if 25 <= age <= 40:
    print("подходит")
else:
    print("не подходит")

print("3: ")
month = int(input("Введите номер месяца: "))
if 1 <= month <= 2 or month == 12:
    print("зима")
elif 3 <= month <= 5:
    print("весна")
elif 6 <= month <= 8:
    print("лето")
elif 9 <= month <= 11:
    print("осень")
else:
    print("Ошибка!")

m = 54
n = 16
while m != n:
    if m > n:
        m -= n
    elif m < n:
        n -= m
print(m)
