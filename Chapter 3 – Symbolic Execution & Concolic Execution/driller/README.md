#### Install driller

```bash
kali@kali$ cd qemu_mode
kali@kali$ wget -O patches/memfd.diff https://salsa.debian.org/qemu-team/qemu/raw/ubuntu-bionic-2.11/debian/patches/ubuntu/lp1753826-memfd-fix-configure-test.patch
kali@kali$ ./build_qemu_support.sh

kali@kali$ sudo apt-get install python-dev libffi-dev build-essential virtualenvwrapper debootstrap debian-archive-keyring

kali@kali$ mkdir ~/.environments

kali@kali$ export WORKON_HOME=~/.environments

kali@kali$ source /usr/share/virtualenvwrapper/virtualenvwrapper.sh

kali@kali$ mkvirtualenv driller

kali@kali$ git clone https://github.com/shellphish/driller.git

kali@kali$ python3.9 install -r requirements.txt

kali@kali$ python3.9 
>>> import driller
>>>
```