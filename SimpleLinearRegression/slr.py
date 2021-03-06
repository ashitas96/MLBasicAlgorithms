from random import seed
from random import randrange
from csv import reader
from math import sqrt

#load a csv file
def load_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset

# convert string column to float
def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())
        
#split a dataset into a train and test set
def train_test_split(dataset, split):
    train = list()
    train_size = split * len(dataset)
    dataset_copy = list(dataset)
    while len(train)<train_size:
        index = randrange(len(dataset_copy))
        train.append(dataset_copy.pop(index))
    return train, dataset_copy

#calculate root mean squared error (RMSE)
def rmse_metric(actual, predicted):
    sum_error = 0.0
    for i in range(len(actual)):
        prediction_error = predicted[i] - actual[i]
        sum_error += (prediction_error**2)
    mean_error = sum_error/float(len(actual))
    return sqrt(mean_error)

#evaluate regression algorithm on train/test split
def evaluate_algorithm(dataset, algorithm, split, *args):
    train, test = train_test_split(dataset, split)
    test_set = list()
    for row in test:
        row_copy = list(row)
        row_copy[-1] = None
        test_set.append(row_copy)
    predicted = algorithm(train, test_set, *args)
    actual = [row[-1] for row in test]
    rmse = rmse_metric(actual, predicted)
    return rmse

#calculate the mean value from a list of numbers
def mean(values):
    return sum(values)/float(len(values))

#calculate variance from a list of values
def variance(values, mean):
    return sum([(x-mean)**2 for x in values])

#calculate covariance between x and y
def covariance(x, mean_x, y, mean_y):
    covar = 0.0
    for i in range(len(x)):
        covar += (x[i] - mean_x) * (y[i] - mean_y)
    return covar

#calculate coefficients a and b for y = ax+b
def coefficients(dataset):
    x = [row[0] for row in dataset]
    y = [row[1] for row in dataset]
    
    x_mean, y_mean = mean(x), mean(y)
    a = covariance(x, x_mean, y, y_mean)/variance(x,x_mean)
    b = y_mean - a * x_mean
    return [b,a]

#implements the prediction equation to make predictions on a test dataset
def simple_linear_regression(train,test):
    predictions = list()
    b,a = coefficients(train)
    for row in test:
        yhat = b + a*row[0]
        predictions.append(yhat)
    return predictions

#SLR on insurance dataset
seed(1)

#load and prepare data
filename = 'insurance.csv'
dataset = load_csv(filename)

for i in range(len(dataset[0])):
    str_column_to_float(dataset, i)
    
    
#evaluate algorithm
split = 0.6
rmse = evaluate_algorithm(dataset, simple_linear_regression,split)
print('RMSE : %.3f' %(rmse))




























