##### SymCC 


```bash
$ git clone https://github.com/eurecom-s3/symcc
$ cd symcc
$ git submodule init
$ git submodule update
$ docker build -t symcc .
$ docker run -it --rm symcc

$ apt-get update
$ apt-get install bsdmainutils less vim -y
$ nano sample.cpp
$ which sym++
$ sym++ sample.cpp -o sample

$ echo test | ./sample
$ ls -la /tmp/output
$ find /tmp/output -type f -print -exec hexdump -C {} \; | less

$ sym++ sample_2.cpp -o sample_2
$ echo "ALLLLLLLLLLLLLLLLLLLLLLLLLLLLL" | ./sample_2


$ mkdir in && mkdir out
$ /symcc_build/pure_concolic_execution.sh -i in	-o out ./sample
$ ls -la | wc -l
$ grep -rn "AB" ./out/


```