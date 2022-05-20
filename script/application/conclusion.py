import os

if __name__ == "__main__":
    file = open("./record/result/all.csv", "r")
    title = file.readline()
    scheduler_time = 0
    sequential_time = 0
    random_time = 0
    list_scheduler = []
    list_sequential = []
    list_random = []

    group_num = 10
    group_size = 100
    for group in range(group_num):
        for id in range(group_size):
            line = file.readline()
            data = line.split(",")
            scheduler_time += float(data[0])
            sequential_time += float(data[1])
            random_time += float(data[2])
        average_scheduler_time = scheduler_time / ((group + 1) * group_size)
        average_sequential_time = sequential_time / ((group + 1) * group_size)
        average_random_time = random_time / ((group + 1) * group_size)
        list_scheduler.append(average_scheduler_time)
        list_sequential.append(average_sequential_time)
        list_random.append(average_random_time)
    print(list_scheduler)
    print(list_sequential)
    print(list_random)

        