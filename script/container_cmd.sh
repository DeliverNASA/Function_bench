docker run -itd -v "$(pwd):/usr/local/test_scripts" -v "/usr/local/lib/python3.8/dist-packages:/usr/local/lib/python3.8/dist-packages" \
    --cpuset-cpus 0 --cpu-period 1000000 --cpu-quota 500000 \
    --name container1 dolphin/ubuntu

docker run -itd -v "$(pwd):/usr/local/test_scripts" -v "/usr/local/lib/python3.8/dist-packages:/usr/local/lib/python3.8/dist-packages" \
    --cpuset-cpus 0 --cpu-period 1000000 --cpu-quota 500000 \
    --name container2 dolphin/ubuntu