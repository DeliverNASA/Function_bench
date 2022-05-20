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

figure_path = "./record/container/"
num = 10

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签

    # read training data
    df = pd.read_csv("./record/container/ans.csv")
    cols = list(df.columns)

    # file the value of Z
    Z = [[0 for j in range(num)] for i in range(num)]
    data_y = list(df[cols[-1]])
    counter = 0
    for id_x in range(0, num):
        for id_y in range(id_x, num):
            Z[id_x][id_y] = Z[id_y][id_x] = data_y[counter]
            counter += 1
    Z = np.array(Z)
    print(Z)

    # let X be a higher dimension, otherwise the point will not be matched
    xx = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    # xx = [i for i in range(1, 11)]
    yy = xx[:]
    X, Y = np.meshgrid(yy, xx)  # not X, Y = np.meshgrid(xx, yy)

    # plot 2D figures
    fig = plt.figure()
    ctf = plt.contourf(X, Y, Z, 10, cmap="Blues")   # fill color
    ct = plt.contour(X, Y, Z, 10, linewidths=1, colors="k")    # draw contour lines
    plt.clabel(ct, fontsize=8, inline=True)       # display the value
    # plt.colorbar(ctf)  # 添加cbar
    plt.xlabel("容器1")
    plt.ylabel("容器2")
    # plt.xticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    # plt.yticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    # plt.title(functions[i] + " & " + functions[j])
    plt.savefig(figure_path + "container.jpg")
    plt.show()

    # plot 3D figures
    # fig = plt.figure()
    # ax = Axes3D(fig)
    # ax.plot_surface(X, Y, Z, rstride=1, cmap='rainbow')
    # ax.set_xlabel("container1")
    # ax.set_ylabel("container2")
    # ax.set_zlabel("IPC")
    # plt.savefig(figure_path + "container_3D.jpg")
    # plt.show()


