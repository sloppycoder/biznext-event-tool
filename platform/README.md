# workaround for no binary wheel for confluent-kafka (1.9.2) on debian bulleye aarch64

The files in ```debian-aarch64/librdkafka``` was built manually on an AWS Graivton instance using the steps below

```
apt update && apt install -y build-essential libghc-curl-dev libghc-zlib-dev libssl-dev libsasl2-dev libzstd-dev

git clone --branch v1.9.2 --depth 1 https://github.com/confluentinc/librdkafka

cd librdkafka
./configure
make
sudo make install

# the files will be installed in /usr/local. only the h and so files are needed.

```
