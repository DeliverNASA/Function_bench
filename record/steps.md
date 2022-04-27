后续实验步骤

1. 混部数据收集

   编写脚本：在两个容器中运行不同的函数，然后使用perf监视得到ips数据，这个过程还要实现输入可控，也就是说函数A的输入范围和函数B的输入范围的不同组合

   使用的函数

   * chameleon
   * feature_extractor
   * float_operation
   * image_processing
   * linpack
   * matmul
   * model_serving：ml_lr_prediction
   * model_training
   * pyaes
   * video_processing

   容器外部检测：perf stat

   * 外部周期性运行。例如每5秒输出一个ips写入，这样的话在容器内部检测中就需要每5秒完成一个实例的测试。优点是比较便捷，只用在终端运行一次即可；缺点是取得的数据不够精确，因为不知道函数执行周期是多久，所测的结果也不一定就是混部时候的ips。
   * 在容器内部运行的时候启动。在每启动一个函数部署实例的时候启动一个perf监测程序，在运行结束时候收回，优点是取得的数据比较精确，缺点是很难控制perf收集的时间周期。

   容器内部检测：python指定运行脚本

   首先要生成不同输入参数的python执行命令，然后在实现混合部署抽取执行，例如对于函数A，先生成一个sh文件A_cmd，内容为执行函数A的不同参数输入，对函数B同理，得到B_cmd。然后一次混合部署中从A_cmd和B_cmd中抽取一条指令，然后混部运行，将perf结果和参数都写入一个记录文件中

   

2. 

