import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from tensorflow import keras
import tensorflow_addons as tfa
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt

learning_rate = 0.005

# Read the data
file_name = '../Dataset/WineQualityNew_R.csv'
dataFrame = pd.read_csv(file_name)

df = dataFrame[['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
                'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
                'pH', 'sulphates', 'alcohol', 'type_red', 'type_white', 'quality']]

# Split the data into training and testing data with using the independent variables(y) and dependent variable(x)
X_train, X_test, Y_train, Y_test = train_test_split(
    df.iloc[:, 0:13].values, df.loc[:, "quality"].values, test_size=0.25, random_state=147)

scaler = MinMaxScaler(feature_range=(0, 1))
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

models = []
models.append(MLPRegressor(random_state=1, max_iter=500))

# slp = keras.models.Sequential()
# slp.add(keras.layers.Dense(units=3, input_dim=13, activation='sigmoid'))
# slp_opt = tfa.optimizers.AdamW(
#     learning_rate=learning_rate, weight_decay=0.0001,
# )
# slp.compile(optimizer=slp_opt, loss='mape', metrics=['accuracy'])
# models.append(slp)

# mlp = keras.models.Sequential()
# mlp.add(keras.layers.Dense(units=4, input_dim=13, activation='relu'))
# mlp.add(keras.layers.Dense(units=3, activation='sigmoid'))
# mlp_opt = tfa.optimizers.AdamW(
#     learning_rate=learning_rate, weight_decay=0.0001,
# )
# mlp.compile(optimizer=mlp_opt, loss='mape', metrics=['accuracy'])
# models.append(mlp)

for model in models:
    model.fit(X_train_scaled, Y_train)
    #model.fit(X_train_scaled, Y_train, epochs=300, batch_size=256)
    #model.evaluate(X_test_scaled, Y_test)

# mlps = []
# for index in range(len(x_train_scaled)):
#     model = models[index].fit(x_train_scaled[index],
#                               y_train[index], epochs=200, batch_size=256)
#     mlps.append(model)

prediction = []
for index in range(len(models)):
    prediction.append(models[index].predict(X_test_scaled))

accuracy = []
for index in range(len(models)):
    accuracy.append(models[index].score(
        X_test_scaled, Y_test))

# Printing the each score of the models
for index, value in enumerate(accuracy):
    print(f'accuracy {index+1}: {value}')


def calculate_error_rate(models, y_test, prediction):
    # Calculate the mean squared error
    mse = []
    for index in range(len(models)):
        mse.append(mean_squared_error(y_test, prediction[index]))

    # Calculate the mean absolute error
    mae = []
    for index in range(len(models)):
        mae.append(mean_absolute_error(y_test, prediction[index]))

    return mse, mae


# Printing the each error metrics of the model
mse, mae = calculate_error_rate(models, Y_test, prediction)
for index, value in enumerate(mse):
    print(f'MSE{index+1}: {value}')
for index, value in enumerate(mae):
    print(f'MAE{index+1}: {value}')


def visulize_error_rate(x_label, y_label, models, error_rate):
    # Visulize the error rate
    plt.xlabel(x_label, fontweight="bold", style="italic")
    plt.ylabel(y_label, fontweight="bold", style="italic")
    plt.scatter(models, error_rate, s=75, marker='o', color='b')
    plt.show()


visulize_error_rate('Models', 'Mean Squared Error', [
                    "M{}".format(index+1) for index in range(4)], mse)
visulize_error_rate('Models', 'Mean Absolute Error', [
                    "M{}".format(index+1) for index in range(4)], mae)
