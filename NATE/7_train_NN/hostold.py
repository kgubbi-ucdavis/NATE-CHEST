## loaded modules ##
import pandas as pd
from os import listdir
from os.path import join,isdir,isfile,exists
import matplotlib.pyplot as plt

from mlxtend.preprocessing import standardize
from mlxtend.preprocessing import minmax_scaling
from pandas.plotting import scatter_matrix
from sklearn.metrics import r2_score


###stacking regressor example###
from mlxtend.regressor import StackingCVRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import GradientBoostingRegressor


from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.linear_model import Lasso, Ridge, ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, cross_val_predict
from mlxtend.regressor import LinearRegression
from sklearn.model_selection import GridSearchCV, train_test_split, KFold
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA

import joblib

# Stacking
from Stacker import *

import numpy as np
RANDOM_SEED = 42

tmp = open('./config.txt', 'r')
tmp_ = tmp.read()
tmp.close()
eval(tmp_)



SEED = 42
np.random.seed(SEED)

df = pd.read_csv(root_path+in_file, index_col='index')

mlp = MLPRegressor(learning_rate='adaptive',
                   hidden_layer_sizes=(23),
                   solver='adam',
                   random_state=1,
                   activation='tanh',
                   max_iter=10000, )

lasso = Lasso(max_iter=5000, alpha=0.001, random_state=SEED)
enet = ElasticNet(random_state=SEED, alpha=0.001)
ridge = Ridge(alpha=1, random_state=SEED)
rf = RandomForestRegressor(n_estimators=1024,
                           bootstrap=True,
                           max_features='auto',
                           min_samples_leaf=1,
                           min_samples_split=2,
                           random_state=SEED, )
xgb = GradientBoostingRegressor(random_state=SEED, n_estimators=1024, learning_rate=0.05, )
stack = StackingCVRegressor(regressors=(ridge, lasso, rf, xgb, enet, mlp),
                            meta_regressor=lasso, verbose=1,
                            n_jobs=2, use_features_in_secondary=True)

df = pd.read_csv(root_path + in_file, index_col='index')
# ageing only
# df.rename(columns = {'SPICE1':'label'}, inplace = True)
results = []
for i in range(6):
    # for i in [0]:
    if i == 0:
        data = df[(df['status'] == 'train')]
    if i == 1:
        data = df[(df['status'] == 'train') | (df['status'] == 'train_HT_10')]
    if i == 2:
        data = df[(df['status'] == 'train') | (df['status'] == 'train_HT_10') |
                  (df['status'] == 'train_HT_20')]
    if i == 3:
        data = df[(df['status'] == 'train') | (df['status'] == 'train_HT_10') |
                  (df['status'] == 'train_HT_20') | (df['status'] == 'train_HT_30')]
    if i == 4:
        data = df[(df['status'] == 'train') | (df['status'] == 'train_HT_10') |
                  (df['status'] == 'train_HT_20') | (df['status'] == 'train_HT_30') |
                  (df['status'] == 'train_HT_40')]
    if i == 5:
        data = df[(df['status'] == 'train') | (df['status'] == 'train_HT_10') |
                  (df['status'] == 'train_HT_20') | (df['status'] == 'train_HT_30') |
                  (df['status'] == 'train_HT_40') | (df['status'] == 'train_HT_50')]

    data.drop(columns=['info', 'path_number', 'GTM', 'SPICE_nt'], axis=1, inplace=True)
    col_list = list(data.columns)
    col_list.remove('label')
    col_list.remove('status')
    zero_idx = np.isclose(data[col_list].sum(axis=0), 0)
    data.drop(columns=list(data[col_list].columns[zero_idx]), axis=1, inplace=True)

    col_list = list(data.columns)
    col_list.remove('label')
    col_list.remove('status')
    data[col_list] = data[col_list].apply(lambda x: (x - x.mean()) / (x.std()))

    train, test = train_test_split(data, test_size=0.2, random_state=SEED)
    y_train = train['label']
    X_train = train.drop(columns=['label', 'status'], axis=1)

    test.drop(test[test['status'] != 'train'].index, axis=0, inplace=True)
    y_test = test['label']
    X_test = test.drop(columns=['label', 'status'], axis=1)

    ## runing the neural models
    result = {}
    # for clf, label in zip([stack], ['StackingClassifier']):
        # print('-' * 20)
        # print('{}:{}'.format(i, label))
        # clf.fit(X_train, y_train)
        # pred_train = clf.predict(X_train)
        # pred_test = clf.predict(X_test)

        # mean_test = np.mean(pred_test - y_test)
        # std_test = np.std(pred_test - y_test)
        # mean_train = np.mean(pred_train - y_train)
        # std_train = np.std(pred_train - y_train)

        # result['trj_n'] = i * 10
        # result['mean_test'] = mean_test
        # result['mean_train'] = mean_train
        # result['std_test'] = std_test
        # result['std_train'] = std_train
        # result['clf'] = label

        # results.append(result.copy())

    for clf, label in zip([mlp, stack], ['mlp', 'StackingClassifier']):
        print('-'*20)
        print('{}:{}'.format(i, label))
        clf.fit(X_train, y_train)
        pred_train = clf.predict(X_train)
        pred_test = clf.predict(X_test)

        mean_test = np.mean(pred_test-y_test)
        std_test = np.std(pred_test-y_test)
        mean_train = np.mean(pred_train-y_train)
        std_train = np.std(pred_train-y_train)

        result['trj_n'] = i*10
        result['mean_test'] = mean_test
        result['mean_train'] = mean_train
        result['std_test'] = std_test
        result['std_train'] = std_train
        result['clf'] = label

        results.append(result.copy())

    joblib.dump(stack, root_path + 'stack_{}.pkl'.format(i))

results_pd = pd.DataFrame(results)
results_pd.to_csv(root_path + res_file)