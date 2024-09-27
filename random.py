import random
dice = []
counter = [0] * 6
print("Insert number of rolls: ")
n = int(input())

print("Задание 1")
average = 0
for x in range(0, n):
    dice.append(random.randint(1, 6))
    average += dice[x]
    counter[dice[x] - 1] += 1
average /= n
print("Dice is: ", dice, " Average: ", average)
for i in range(0, 6):
    print(i + 1, ": ", counter[i])
dispersion = 0
for i in range(0, n):
    dispersion += (dice[i] - average)**2
dispersion /= n
print("Dispersion: ", dispersion)

print("Задание 2")
dice[0] = 6
dice[1] = 2
dice[2] = 5
average2 = 0
for i in range(0, n):
    average2 += dice[i]
average2 /= n
print("New average: ", average2)
