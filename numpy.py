import numpy as np

print("Задание 1")
dice = np.random.randint(1, 7, (10, 10))
print("Dice: ", dice)
xaxis_dispersion = np.var(dice, axis = 0)
yaxis_dispersion = np.var(dice, axis = 1)
print("X-axis dispersion: ", xaxis_dispersion)
print("X-axis dispersion: ", yaxis_dispersion)

print("Задание 2")
list_of_columns = np.zeros((10, 10), dtype=np.int8)
for i in range(0, 10):
    list_of_columns[i] = dice[:, i]
print("List of columns: ", list_of_columns)

first_list_dispersion = np.var(dice)
second_list_dispersion = np.var(list_of_columns)
print(first_list_dispersion, " - ", second_list_dispersion,
      " = ", first_list_dispersion - second_list_dispersion)
