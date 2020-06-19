from __future__ import absolute_import, division, print_function, unicode_literals
import pandas as pd
# noinspection PyUnresolvedReferences
import tensorflow.compat.v2.feature_column as fc
import tensorflow as tf

dftrain = pd.read_csv("dataset1.csv")
y_train = dftrain.pop("death")
dfeval = pd.read_csv("dataset2.csv")
print(dfeval)
y_eval = dfeval.pop("death")
CATEGORICAL_COLUMNS = ["gender", "country"]

feature_columns = []

for feature_name in CATEGORICAL_COLUMNS:
    vocabulary = dftrain[feature_name].unique()  # gets a list of all unique values from given feature column
    feature_columns.append(tf.feature_column.categorical_column_with_vocabulary_list(feature_name, vocabulary))

feature_columns.append(tf.feature_column.numeric_column("age", dtype=tf.float32))


def make_input_fn(data_df, label_df, num_epochs=30, shuffle=True, batch_size=100):
    def input_function():  # inner function, this will be returned
        ds = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))
        # create tf.data.Dataset object with data and its label
        if shuffle:
            ds = ds.shuffle(1000)  # randomize order of data
        ds = ds.batch(batch_size).repeat(num_epochs)
        # split dataset into batches of 100 and repeat process for number of epochs
        return ds  # return a batch of the dataset
    return input_function  # return a function object for use


train_input_fn = make_input_fn(dftrain, y_train)
# here we will call the input_function that was returned to us to get a dataset object we can feed to the model
eval_input_fn = make_input_fn(dfeval, y_eval, num_epochs=1, shuffle=False)
linear_est = tf.estimator.LinearClassifier(feature_columns=feature_columns)
linear_est.train(train_input_fn)  # train
result = linear_est.predict(eval_input_fn)  # get model metrics/stats by testing on testing data


for i in result:
    print(i) # the result variable is simply a dict of stats about our model
