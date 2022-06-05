# 项目介绍

## 冲突检测

### 本地场景

1. docker启动容器，在此配备cpu-quota/cpu-period为0.2，1等

   ``` shell
   docker run -itd -v "$(pwd):/usr/local/" -v "/usr/local/lib/python3.8/dist-packages:/usr/local/lib/python3.8/dist-packages" \
       --cpuset-cpus 0 --cpu-period 1000000 --cpu-quota 200000 \
       --name container1 blueddocker/ubuntu
   
   docker run -itd -v "$(pwd):/usr/local/" -v "/usr/local/lib/python3.8/dist-packages:/usr/local/lib/python3.8/dist-packages" \
       --cpuset-cpus 0 --cpu-period 1000000 --cpu-quota 1000000 \
       --name container2 blueddocker/ubuntu
   ```

2. docker运行混合部署测试

   ``` shell
   # 根据要跑的测试选择脚本，记录下函数执行完毕的延迟
   docker exec -d container1 python3 ./aws/cpu-memory/chameleon/lambda_function.py
   docker exec -d container2 python3 ./aws/cpu-memory/chameleon/lambda_function.py
   # 如果进行总体测试，执行test_all.py
   docker exec -d container1 ./script/test/test_all.py
   docker exec -d container2 ./script/test/test_all.py
   ```

3. 使用perf监测容器1的系统性能指标

   ``` shell
   # 指定进程、CPU
   perf stat -p pid(container1) -C 0
   ```

### OpenFaaS

1. 在k8s集群上搭建OpenFaaS环境

   ``` shell
   # 切换到faas-netes目录下
   # 部署的时候要把代理关闭，否则会出现请求被拒绝的情况
   # 都使用root用户执行
   kind create cluster
   kubectl apply -f namespaces.yml
   kubectl -n openfaas create secret generic basic-auth \
       --from-literal=basic-auth-user=admin \
       --from-literal=basic-auth-password=admin
   // 在apply的时候将faas-netes下面的dep文件imagePullPolicy都改为IfNotPresent，否则会被代理折磨
   kubectl apply -f ./yaml
   kubectl get pods -n openfaas
   kubectl get service -n openfaas
   
   # 使用kinD时需要手动映射端口才能访问127.0.0.1:31112
   kubectl port-forward svc/gateway -n openfaas 31112:8080 &
   ```

2. 新建函数示例（以add为例）

   ``` shell
   faas-cli template pull
   faas-cli new add --lang python3-debian -p blueddocker
   # 在函数编写完成后
   faas-cli build -f ./add.yml
   ```

   此时build会自动生成Dockerfile并开始docker build，由于防火墙的原因，需要中断此过程并手动在Dockerfile中添加镜像源：

   在apt-get之前：

   ``` dockerfile
   RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && \
      echo "deb http://mirrors.aliyun.com/debian/ buster main non-free contrib" >/etc/apt/sources.list && \
      echo "deb-src http://mirrors.aliyun.com/debian/ buster main non-free contrib" >>/etc/apt/sources.list && \
      echo "deb http://mirrors.aliyun.com/debian-security buster/updates main" >>/etc/apt/sources.list && \
      echo "deb-src http://mirrors.aliyun.com/debian-security buster/updates main" >>/etc/apt/sources.list && \
      echo "deb http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib" >>/etc/apt/sources.list && \
      echo "deb-src http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib" >>/etc/apt/sources.list && \
      echo "deb http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib" >>/etc/apt/sources.list && \
      echo "deb-src http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib" >>/etc/apt/sources.list
   ```

   在pip之后：

   ``` shell
   pip install *** -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

   再重新进行docker build，并推送到远程仓库中并部署，至此已经完成在OpenFaaS上的函数部署

   ``` 
   docker build -t blueddocker/add --cpuset-cpus 0 --cpu-period 1000000 --cpu-quota 200000 . # blueddocker是dockerhub的用户名
   faas-cli push -f ./add.yml  # 推送到远程仓库，部署的时候才能拉区镜像
   faas-cli deploy -f add.yml  # 部署到OpenFaaS上
   ```

3. 函数调用测试

   ```shell
   # 几种调用函数的方式（以nodejs-echo为例）
   faas invoke nodejs-echo # 适用于手动输入参数调用
   curl -d '{"hello": "world"}' http://127.0.0.1:8080/function/nodejs-echo # 直接传text或json参数
   curl --data-binary @README.md http://127.0.0.1:8080/function/nodejs-echo # 传二进制参数
   uname -a | curl http://127.0.0.1:8080/function/nodejs-echo--data-binary @- # 标准输入传参
   
   # 以chameleon和float-operation为例
   curl -d '600' http://127.0.0.1:31112/function/chameleon
   curl -d '2000000' http://127.0.0.1:31112/function/float-operation
   ```

## 冲突消解

1. 数据收集

   主要代码在/script/generate目录下，其中：

   * cmd_parser：解析指令
   * generator：混部用例测试

   ``` shell
   # 测试1：双容器不同资源分配的IPC
   python3 ./script/prepare/generator.py
   
   # 测试2：不同混合部署组合的IPC
   # 如果当前无容器，需要启动两个容器
   docker run -itd -v "$(pwd):/usr/local/" -v "/usr/local/lib/python3.8/dist-packages:/usr/local/lib/python3.8/dist-packages" \
       --cpuset-cpus 0 --cpu-period 1000000 --cpu-quota 300000 \
       --name container1 blueddocker/ubuntu
   
   docker run -itd -v "$(pwd):/usr/local/" -v "/usr/local/lib/python3.8/dist-packages:/usr/local/lib/python3.8/dist-packages" \
       --cpuset-cpus 0 --cpu-period 1000000 --cpu-quota 700000 \
       --name container2 blueddocker/ubuntu
   python3 ./script/generate/generator.py
   ```

2. IPC预测器

   主要代码在/script/analysis目录下，其中：

   * argument：存储参数
   * model：训练机器学习模型
   * plot、plot_container：绘制IPC等高线图，数据可视化

   ```shell
   # 绘图
   python3 ./script/analysis/plot.py
   python3 ./script/analysis/plot.py
   # 训练模型
   python3 ./script/analysis/model.py
   ```

3. 调度器

   主要代码在/script/application/schedulers目录下，其中：

   * utils：存储task、CPU监测器等数据结构
   * scheduler：三种不同的调度器
     * 顺序调度算法：按照任务到达顺序进行调度
     * 优先调度算法：按照任务优先级进行调度
     * 智能调度算法：按照IPC调度器的预测结果进行调度

   测试示例：

   ``` shell
   # CPU监视器
   python3 ./script/application/schedulers/utils.py
   # 调度器
   python3 ./script/application/schedulers/scheduler.py
   ```

4. 动态分配

   主要代码在/script/application/allocators目录下，其中：

   * allocator：动态分配器，基于对cgroup文件的读写实现

   启动动态分配器示例：

   ```shell
   # 在开启CPU监测器的前提下才有效
   python3 ./script/application/allocators/allocator.py
   ```

5. 仿真

   主要代码在/script/application/simulation目录下，其中：

   * task_generator：任务生成器
   * simulator：仿真器
     * 选择容器数目：{1，2}
     * 选择任务规模：{20，50，100}
     * 选择调度器：{顺序调度，优先调度，智能调度}
     * 选择资源分配方式：{无动态分配，动态分配}

   启动仿真示例：

   ``` shell
   # 在开启CPU监测器的前提下才有效，且需要提前关闭动态分配器（避免重复启动）
   python3 ./script/application/simulation/simulator.py
   ```

   结果储存位置：

   ``` 
   latency_record = "./script/application/log/latency.txt"
   time_record = "./script/application/log/time_finish.txt"
   ```
