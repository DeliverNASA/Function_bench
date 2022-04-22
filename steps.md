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

2. 