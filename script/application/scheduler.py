import joblib
import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import StandardScaler
from task_generator import functions

combinations = []
model_basic_path = "./record/model/"

def dfs(L, ans):
    if len(L) == 0:
        combinations.append(ans)
        return 

    # choose the first element
    ans.append(L[0])
    L.remove(L[0])
    for data in L:
        ans.append(data)
        tmp = L.copy()
        tmp.remove(data)
        dfs(tmp, ans.copy())
        ans.remove(data)

def scheduler(task_list):
    task_num = len(task_list)
    dfs([i for i in range(task_num)], [])
    max_ipc = -1
    best_comb = [i for i in range(task_num)]
    # print(combinations)
    for combination in combinations:
        # print("combination: " + str(combination))
        total_ipc = 0
        for i in range(int(task_num / 2)):
            # just for test
            # if i != 0 or combinations.index(combination) != 0:
            #     continue

            func1 = task_list[combination[2*i]]
            func2 = task_list[combination[2*i+1]]
            # let function1's id smaller than function2's id 
            if func1[0] > func2[0]:
                tmp = func1.copy()
                func1 = func2.copy()
                func2 = tmp

            # print("func1: " + str(func1) + "  func2: " + str(func2))

            train_dataset = pd.read_csv("./record/data/%d_%d.csv" % (func1[0], func2[0]))
            cols = list(train_dataset.columns)
            rows = train_dataset.shape[0]

            # reshape: change string type to int type
            train = train_dataset.loc[:, cols[:-1]]     # use loc to copy a dataframe, instead of train_dataset[cols[:-1]]
            regex = re.compile(r'\d+')
            for col_name in cols[:-1]:
                # print(type(train[col_name].iloc[0])) # loc: only string type can be used, iloc: only integer type can be used
                if type(train[col_name].iloc[0]) != np.int64:
                    # tmp = np.zeros(rows)
                    # tmp2 = [0 for i in range(rows)]
                    tmp2 = np.zeros(train.shape[0])
                    for row in range(rows):
                        # print(regex.findall(str(x[col_name].iloc[i]))[0])
                        tmp2[row] = int(regex.findall(str(train[col_name].iloc[row]))[0])
                    # train[col_name] = tmp2
                    train.loc[:, (col_name)] = tmp2

            # print(train)
            # use training data to standardize
            sc = StandardScaler()
            sc.fit(train)
            # print(train)
            test = pd.DataFrame([func1[1:]+func2[1:]], columns=train.columns)
            # print(test)
            test_std = sc.transform(test)
            # print(test_std)

            model = joblib.load(model_basic_path + "%d_%d.pk" % (func1[0], func2[0]))
            test_ipc = model.predict(test_std)
            total_ipc += test_ipc
            # print("test_ipc: " + str(test_ipc))

        if total_ipc > max_ipc:
            max_ipc = total_ipc
            best_comb = combination

    # print("max_ipc: " + str(max_ipc))
    # print("best_comb: " + str(best_comb))

    return best_comb



if __name__ == "__main__":
    comb = scheduler(6)