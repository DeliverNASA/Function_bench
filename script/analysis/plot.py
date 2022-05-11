import time
import joblib
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from scipy.interpolate import Rbf

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

from argument import args, functions

model_basic_path = "./record/model/"
figure3D_basic_path = "./record/figure/3D/"
figure2D_basic_path = "./record/figure/2D/"

masks_1 = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
# masks_1 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

masks_2 = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
# masks_2 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


if __name__ == "__main__":
    # read training data
    length = len(masks_1)

    for i in range(length):
        if masks_1[i]:
            continue
        for j in range(i, length):
            if masks_2[j]:
                continue

            print("task: " + functions[i] + " " + functions[j])

            df = pd.read_csv("./record/data/%d_%d.csv" % (i, j))
            cols = list(df.columns)

            # plot: only plot function with two variables
            if len(cols) > 3:
                continue

            xx = args[i]
            yy = args[j]
            x_len = len(xx)
            y_len = len(yy)

            # file the value of Z
            # attention: X: f1_args, Y:f2_args
            if i != j:
                Z = np.array(df[cols[-1]]).reshape(x_len, y_len)
                # print(Z)
            else:
                Z = [[0 for j in range(y_len)] for i in range(x_len)]
                data_y = list(df[cols[-1]])
                counter = 0
                for id_x in range(0, y_len):
                    for id_y in range(id_x, y_len):
                        Z[id_x][id_y] = Z[id_y][id_x] = data_y[counter]
                        counter += 1
                Z = np.array(Z)

            # let X be a higher dimension, otherwise the point will not be matched
            X, Y = np.meshgrid(yy, xx)  # not X, Y = np.meshgrid(xx, yy)

            # plot 2D figures
            # if x_len == 1 or y_len == 1:  # only matrix larger than (2, 2) will be plotted
            #     continue
            # fig = plt.figure()
            # ctf = plt.contourf(X, Y, Z, 10, cmap="Blues")   # fill color
            # ct = plt.contour(X, Y, Z, 10, linewidths=1, colors="k")    # draw contour lines
            # plt.clabel(ct, fontsize=7, inline=True)       # display the value
            # # plt.colorbar(ctf)  # 添加cbar
            # plt.xlabel(cols[1])
            # plt.ylabel(cols[0])
            # plt.title(functions[i] + " & " + functions[j])
            # plt.savefig(figure2D_basic_path + "%d_%d.jpg" % (i, j))

            # plot 3D figures
            fig = plt.figure()
            ax = Axes3D(fig)
            ax.plot_surface(X, Y, Z, rstride=1, cmap='rainbow')
            ax.set_xlabel(cols[1])
            ax.set_ylabel(cols[0])
            ax.set_zlabel("IPC")
            ax.set_title(functions[i] + " & " + functions[j])
            plt.savefig(figure3D_basic_path + "%d_%d.jpg" % (i, j))
            # plt.show()


