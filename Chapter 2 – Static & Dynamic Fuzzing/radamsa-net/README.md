#### To install radamsa, first we have to clone the repository from gitlab:
```bash

git clone https://gitlab.com/akihe/radamsa.git

cd radamsa

make

sudo make install

```

Now we are ready to use it.

One simple trick would be using netcat to pipe the output to the target service. In this case host 192.168.1.12 on port 8080:

```bash
One simple trick would be using netcat to pipe the output to the target service. In this case host 192.168.1.12 on port 8080:

	echo "some random string 123456789" | radamsa | nc 192.168.1.12 8080

we can send data simpler and directly using radamsa network support:

	echo "some random string 123456789" | radamsa -o 192.168.1.12:8080

we want to send the data to some UDP service:

	echo "some random string 123456789" | radamsa -o 192.168.1.1:123/udp

```