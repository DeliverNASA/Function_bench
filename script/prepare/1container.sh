docker run -itd -v "$(pwd):/usr/local/" -v "/usr/local/lib/python3.8/dist-packages:/usr/local/lib/python3.8/dist-packages" \
    --cpuset-cpus 0 --cpu-period 1000000 --cpu-quota 1000000 \
    --name container1 blueddocker/ubuntu