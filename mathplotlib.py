import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ggplot')

#Генерация данных

tableTask3 = pd.read_csv(filepath_or_buffer = "Task3.csv", sep = ',', nrows = 20)
ydata = tableTask3['hindfoot_length']
xdata = tableTask3['record_id']

unique, counts = np.unique(tableTask3['species_id'], return_counts=True)

#Параметры отображения графика и вывод данных

plt.figure(figsize=(10, 5))

plt.scatter(xdata, ydata, label='hindfoot lenght')

plt.legend(loc='best')

plt.figure(figsize=(10, 5))
plt.scatter(unique, counts, label='species id')

women = tableTask3['species_id'][tableTask3['gender'] == 'F'].unique()
print("Species ID for women: ", women)

print("Difference between max and min haidfoot lenght: ", ydata.max() - ydata.min())

plt.show()

