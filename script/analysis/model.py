import time
import joblib
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsRegressor, KNeighborsTransformer
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

from argument import args, functions

import re

model_basic_path = "./record/model/"
figure_basic_path = "./record/figure/3D/"
masks_1 = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
masks_2 = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]


if __name__ == "__main__":
    # read training data
    length = len(masks_1)
    sc = StandardScaler()

    for i in range(length):
        if masks_1[i]:
            continue
        for j in range(i, length):
            if masks_2[j]:
                continue

            print("task: " + functions[i] + " " + functions[j])

            df = pd.read_csv("./record/data/%d_%d.csv" % (i, j))
            cols = list(df.columns)
            rows = df.shape[0]

            # reshape: change string type to int type
            x = df.loc[:, cols[:-1]]
            regex = re.compile(r'\d+')
            for col_name in cols[:-1]:
                print(type(x[col_name].iloc[0])) # loc: only string type can be used, iloc: only integer type can be used
                if type(x[col_name].iloc[0]) != np.int64:
                    # tmp = np.zeros(rows)
                    tmp = [0 for i in range(rows)]
                    for row in range(rows):
                        # print(regex.findall(str(x[col_name].iloc[i]))[0])
                        tmp[row] = int(regex.findall(str(x[col_name].iloc[row]))[0])
                    x[col_name] = tmp
            # print(x)

            sc.fit(x)
            x_std = sc.transform(x)
            y = df[cols[-1]]

            model = LinearRegression()
            # model = DecisionTreeRegressor()
            # model = KNeighborsRegressor(n_neighbors=3)
            model.fit(x_std, y)
            model_file_path = model_basic_path + "%d_%d.pk" % (i, j)
            joblib.dump(model, model_file_path)

            # test = pd.DataFrame(x_y,columns=list(['f1_num_of_row_col','f2_num_of_row_col']))
            # test = sc.transform(test)
            # Z = model.predict(test)
            # Z = np.array(Z).reshape(len(xx),len(yy))
