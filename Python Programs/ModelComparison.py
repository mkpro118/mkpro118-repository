from LearningNeuralNetworksMultiClassClassificationVersion import NeuralNetworkMultiClassifier as NNMC
from NeuralNet import NeuralNet as NN
# from Test import NeuralNetworkMultiClassifier as NNMC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from time import perf_counter as pc
import pandas as pd
# import numpy as np
# from matplotlib import pyplot as plt

print('Time taken to create the training and test datasets...', end=' ')
t1 = pc()

# # A Good Dataset
# # From a file of randomly generated numbers
df = pd.read_csv('Data/MLData.csv', index_col='ID')
X = df[['Attribute 1', 'Attribute 2', 'Attribute 3', 'Attribute 4']].values
y = df['Answers'].values

# Cluster Dataset
# df = pd.read_csv('Data/Cluster Dataset.csv')
# X = df[['x', 'y']].values
# y = df['color'].values

# # Linear Dataset
# df = pd.read_csv('Data/Linear Dataset.csv')
# X = df[['x', 'y']].values
# y = df['color'].values

# # Quadratic Dataset
# df = pd.read_csv('Data/Quadratic Dataset.csv')
# X = df[['x', 'y']].values
# y = df['color'].values

# A Horrible Dataset
# From https://cs231n.github.io/neural-networks-case-study/
# N = 100  # number of points per class
# D = 2  # dimensionality
# K = 4  # number of classes
# X = np.zeros((N * K, D))  # data matrix (each row = single example)
# y = np.zeros(N * K, dtype='uint8')  # class labels
# for j in range(K):
#     ix = range(N * j, N * (j + 1))
#     r = np.linspace(0.0, 1, N)  # radius
#     t = np.linspace(j * 4, (j + 1) * 4, N) + np.random.randn(N) * 0.2  # theta
#     X[ix] = np.c_[r * np.sin(t), r * np.cos(t)]
#     y[ix] = j

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=118)
print(round(pc() - t1, 4), 'seconds', end='\n\n')

models = [NNMC(output_answers=4),
          LogisticRegression(solver='liblinear'),
          DecisionTreeClassifier(),
          RandomForestClassifier(),
          MLPClassifier(),
          # NN(classes=4, activation_function='relu'),]
          NN()]


def compare(model):
    t1 = pc()
    name = model.__class__.__name__
    model.fit(X_train, y_train)
    accuracy = round(model.score(X_test, y_test) * 100, 4)
    time = round(pc() - t1, 3)
    return name, accuracy, time


def main():
    df = pd.DataFrame({'Model name': [], 'Accuracy (%)': [], 'Time (s)': [], 'ID': []})
    df.set_index('ID', inplace=True)
    count = 1
    for model in models:
        name, accuracy, time = compare(model)
        vals = {'Model name': name, 'Accuracy (%)': accuracy, 'Time (s)': time}
        df.loc[count] = vals
        count += 1

    df.sort_values(by=['Accuracy (%)', 'Time (s)'], ascending=[False, True], inplace=True)
    print(df.head(6))


if __name__ == '__main__':
    main()
