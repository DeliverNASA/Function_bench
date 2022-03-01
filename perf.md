# 使用perf进行性能分析

## Perf学习

1. Perf

   Perf是内置于Linux内核源码树中的性能剖析(profiling)工具。

   它基于事件采样原理，以性能事件为基础，支持针对处理器相关性能指标与操作系统相关性能指标的性能剖析。

   常用于性能瓶颈的查找与热点代码的定位。

   CPU周期(cpu-cycles)是默认的性能事件，所谓的CPU周期是指CPU所能识别的最小时间单元，通常为亿分之几秒，

   是CPU执行最简单的指令时所需要的时间，例如读取寄存器中的内容，也叫做clock tick。

2. perf list

   用来查看perf所支持的性能事件，有软件的也有硬件的。

   性能事件的分布：

   * hw：Hardware event
   * sw：Software event
   * cache：Hardware cache event
   * tracepoint：Tracepoint event

3. perf top

   对于一个指定的性能事件（默认是CPU周期），显示消耗最多的函数或指令。

   perf top主要用于实时分析各个函数在某个性能事件上的热度，能够快速的定位热点函数，包括应用程序函数、

   模块函数与内核函数，甚至能够定位到热点指令。默认的性能事件为cpu cycles。

   结果格式为：

   | 性能事件的比例 | 所在的DSO | DSO类型 | 符号名 |
   | -------------- | --------- | ------- | ------ |

   常用的命令行参数：

   -e <event>：指明要分析的性能事件。

   -p <pid>：仅分析目标进程及其创建的线程。

   -K：不显示属于内核或模块的符号。

   -U：不显示属于用户态程序的符号。

   -G：得到函数的调用关系图。

4. perf stat

   用于分析指定程序（进程）的性能状况。可将结果写入文件中。

   默认输出10个性能事件的统计：

   常用的命令行参数：

   -p：仅分析目标进程及其创建的线程。

   -a：从所有CPU上收集性能数据。

   -C：从指定CPU上收集性能数据。

   -r：重复执行命令求平均。

   -v：显示更多性能数据。

5. perf record

   收集采样信息，并将其结果记录在数据文件中，随后可以通过其它工具(perf-report)对数据文件进行分析，结果类似于perf-top的。

   常用的命令行参数：

   -e：Select the PMU event.

   -a：System-wide collection from all CPUs.

   -p：Record events on existing process ID (comma separated list).

   -A：Append to the output file to do incremental profiling.

    -f：Overwrite existing data file.

   -o：Output file name.

   -g：Do call-graph (stack chain/backtrace) recording.

   -C：Collect samples only on the list of CPUs provided.

6. perf record

   读取perf record创建的文件，并给出热点分析结果。

   

## 实验分析

1. 实验设计

   首先设定一个固定的容器container1，其设置为只占用单核CPU，并且在时间片为1s的情况下占用0.2s资源。

   然后设定一个变化的容器container2，用于模拟混合部署的环境，其参数设定为时间片为1s的情况下占用0.2s、0.4s、0.6s、0.8s、1s，表示竞争程度的逐步增加。

2. 实验结果

   | 配置 \ 指标 | task-clock | context-switches(K/sec) | cpu-migrations(K/sec) | page-faults(K/sec) | cycles(GHz) | instructions(per cycle) | branches(M/sec) | branch-misses(%) |
   | ----------- | ---------- | ----------------------- | --------------------- | ------------------ | ----------- | ----------------------- | --------------- | ---------------- |
   | 0.2         | 52.30      | 14.781                  | 0.688                 | 1.109              | 0.861       | 0.92                    | 174.602         | 2.83             |
   | 0.2+0.2     | 55.10      | 19.220                  | 0.889                 | 0.617              | 1.144       | 0.96                    | 242.351         | 2.77             |
   | 0.2+0.4     | 48.16      | 24.479                  | 1.080                 | 1.453              | 1.033       | 0.90                    | 205.730         | 2.89             |
   | 0.2+0.6     | 28.24      | 54.567                  | 2.160                 | 2.727              | 2.602       | 0.89                    | 512.000         | 2.86             |
   | 0.2+0.8     | 31.34      | 57.299                  | 2.265                 | 1.531              | 2.456       | 0.87                    | 474.590         | 2.92             |
   | 0.2+1       | 24.90      | 69.878                  | 3.534                 | 2.128              | 2.415       | 0.83                    | 442.626         | 2.83             |

3. 结果分析

   * 首先发现，在container2设置为0.4和0.6之间时出现一个显著的突变，与之前实验中的时间突变有着极大的相似性，推测之前的突变是由该因素引起的。
   * 根据实验的结果，首先变化最明显、且呈现显然递增规律的是上下文切换（context-switches）、CPU迁移次数（cpu-migrations）和CPU频率（cycles），随着混合部署的程度上升而上升，并且在容器2参数为0.4到0.6之间存在一个突变，这和之前的实验中展现出的结果现象相同，推测可能是由于这些原因造成了运行时间的突变。
   * 在单周期指令数、分支预测错误率等指标上保持不变，基本排除这些因素对于结果的干扰。

