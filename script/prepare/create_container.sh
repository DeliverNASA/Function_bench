docker run -itd -v "$(pwd):/usr/local/" -v "/usr/local/lib/python3.8/dist-packages:/usr/local/lib/python3.8/dist-packages" \
    --cpuset-cpus 0 --cpu-period 1000000 --cpu-quota 1000000 \
    --name container1 blueddocker/ubuntu

docker run -itd -v "$(pwd):/usr/local/" -v "/usr/local/lib/python3.8/dist-packages:/usr/local/lib/python3.8/dist-packages" \
    --cpuset-cpus 0 --cpu-period 1000000 --cpu-quota 1000000 \
    --name container2 blueddocker/ubuntu


# docker exec container1 apt-get update
# docker exec container1 apt install -y libjpeg8 libimagequant0 libtiff5 libgl1 libglib2.0-dev

# docker exec container2 apt-get update
# docker exec container2 apt install -y libjpeg8 libimagequant0 libtiff5 libgl1 libglib2.0-dev

# docker rm -f $(docker ps -aq)