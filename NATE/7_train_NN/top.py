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
# from Stacker import *

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
# 

clf_label_zip = [(mlp, 'mlp'), (stack, 'StackingClassifier')]
def get_statistic():
    df = pd.read_csv(root_path + in_file, index_col='index')
    results = []
    for i in range(6):
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
        # pred_result = {}
        result = {}
        # for clf, label in zip([ridge], ['Ridge']):
        for clf, label in clf_label_zip:
            print('-' * 20)
            print('{}:{}'.format(i, label))
            clf.fit(X_train, y_train)
            pred_train = clf.predict(X_train)
            pred_test = clf.predict(X_test)

            mean_test = np.mean(pred_test - y_test)
            std_test = np.std(pred_test - y_test)
            mean_train = np.mean(pred_train - y_train)
            std_train = np.std(pred_train - y_train)

            result['trj_n'] = i * 10
            result['mean_test'] = mean_test
            result['mean_train'] = mean_train
            result['std_test'] = std_test
            result['std_train'] = std_train
            result['clf'] = label

            results.append(result.copy())
            joblib.dump(clf, root_path + '{}_{}.pkl'.format(label, i))

    results_pd = pd.DataFrame(results)
    results_pd.to_csv(root_path + res_file)

def get_predictions():

    pred_results = {}
    for i in range(6):
        df = pd.read_csv(root_path + in_file, index_col='index')
        # df_temp = df[['label', 'status']]
        df_temp = df.copy()
        df.drop(columns=['label', 'info', 'status', 'path_number', 'GTM', 'SPICE_nt'], axis=1, inplace=True)
        zero_idx = np.isclose(df.sum(axis=0), 0)
        df.drop(columns=list(df.columns[zero_idx]), axis=1, inplace=True)

        # for i in [0]:
        if i == 0:
            df_ht0 = df_temp[(df_temp['status'] == 'train')]
            df = df.apply(lambda x: (x - df_ht0[x.name].mean()) / (df_ht0[x.name].std()))

        if i == 1:
            df_ht10 = df_temp[(df_temp['status'] == 'train') | (df_temp['status'] == 'train_HT_10')]
            df = df.apply(lambda x: (x - df_ht10[x.name].mean()) / (df_ht10[x.name].std()))

        if i == 2:
            df_ht20 = df_temp[(df_temp['status'] == 'train') | (df_temp['status'] == 'train_HT_10') |
                              (df_temp['status'] == 'train_HT_20')]
            df = df.apply(lambda x: (x - df_ht20[x.name].mean()) / (df_ht20[x.name].std()))

        if i == 3:
            df_ht30 = df_temp[(df_temp['status'] == 'train') | (df_temp['status'] == 'train_HT_10') |
                              (df_temp['status'] == 'train_HT_20') | (df_temp['status'] == 'train_HT_30')]
            df = df.apply(lambda x: (x - df_ht30[x.name].mean()) / (df_ht30[x.name].std()))

        if i == 4:
            df_ht40 = df_temp[(df_temp['status'] == 'train') | (df_temp['status'] == 'train_HT_10') |
                              (df_temp['status'] == 'train_HT_20') | (df_temp['status'] == 'train_HT_30') |
                              (df_temp['status'] == 'train_HT_40')]
            df = df.apply(lambda x: (x - df_ht40[x.name].mean()) / (df_ht40[x.name].std()))
        if i == 5:
            df_ht50 = df_temp[(df_temp['status'] == 'train') | (df_temp['status'] == 'train_HT_10') |
                              (df_temp['status'] == 'train_HT_20') | (df_temp['status'] == 'train_HT_30') |
                              (df_temp['status'] == 'train_HT_40') | (df_temp['status'] == 'train_HT_50')]
            df = df.apply(lambda x: (x - df_ht50[x.name].mean()) / (df_ht50[x.name].std()))

        temp = {}
        # for clf, label in zip([ridge], ['Ridge']):
        for clf, label in clf_label_zip:
            stacking = joblib.load(root_path + '{}_{}.pkl'.format(label, i))
            temp['{}_ht_{}'.format(label, i * 10)] = list(stacking.predict(df))
            pred_results.update(temp.copy())
            # print(temp)
            # break
    df = df.join(pd.DataFrame(pred_results))
    df = df.join(df_temp[['label', 'status']])
    df.to_csv(root_path + out_file)

get_statistic()
get_predictions()