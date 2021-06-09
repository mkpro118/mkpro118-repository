import pandas as pd
from matplotlib import pyplot as plt
from itertools import combinations

df = pd.read_csv('Data/MLData.csv', index_col='ID')
# print(df)

attrs = {}

for i in range(1, 5):
    attrs[f'atr{i}'] = [df[f'Attribute {i}'].values, f'Attribute {i}']

k = combinations(attrs.keys(), r=2)

# for i, j in k:
#     print(attrs[i][0].shape)
#     print(attrs[j][0].shape)
#     print()

attrs['answers'] = df['Answers'].values
# print(attrs['answers'])

plt.style.use('dark_background')
fig, ax = plt.subplots(2, 3)
for row in ax:
    for col in row:
        x, y = next(k)
        col.scatter(attrs[x][0], attrs[y][0], c=attrs['answers'], cmap='winter', alpha=0.75, edgecolor='white')
        col.set_xlabel(attrs[x][1])
        col.set_ylabel(attrs[y][1])

plt.tight_layout()
plt.show()
