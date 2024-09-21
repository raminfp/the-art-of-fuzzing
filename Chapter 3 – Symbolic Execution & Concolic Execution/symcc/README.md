### SymCC 


```bash
$ git clone https://github.com/eurecom-s3/symcc
$ git submodule init
$ git submodule update
$ docker build -t symcc .
$ docker run -it --rm symcc
docker $ apt-get update
docker $ apt-get install bsdmainutils less vim nano
docker $ sym++ sample.cpp -o sample
docker $ ls /tmp/output
docker $ find /tmp/output type f -print -exec hexdump -C {} \; | less
docker $ grep -r "ABC" /tmp/output
docker $ mkdir in && mkdir out && echo AAAAAAAAAAAAAAAAa >> in/seed
docker $ ./symcc_build/pure_concolic_execution.sh -i ./in -o out ./sample

```
