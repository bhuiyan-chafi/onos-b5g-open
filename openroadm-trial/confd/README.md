# How install `confd`

There are a couple of steps that you have to perform before installing `confd`. Let's start with downloading the `confd` package from cisco:

- it requires your own cisco account to download the zip file.
- unzip the file
- then run this: which will verify and bring the installer for you

```bash
./confd-basic-8.0.19.linux.x86_64.signed.bin
```

- now you have to download and install `libssl1.1` as dependency:

```bash
cd ~/Downloads
wget https://www.openssl.org/source/openssl-1.1.1b.tar.gz
cd
sudo mkdir /opt/openssl
sudo tar xfvz ~/Downloads/openssl-1.1.1b.tar.gz --directory /opt/openssl
perl --version
export LD_LIBRARY_PATH=/opt/openssl/lib
echo $LD_LIBRARY_PATH
cd /opt/openssl/openssl-1.1.1b
sudo ./config --prefix=/opt/openssl --openssldir=/opt/openssl/ssl
sudo make
sudo make test
sudo make install #even if some tests fail
sudo apt install plocate
locate openssl | grep /opt/openssl/bin
cd /usr/bin
ls -l openssl #out existing openssl version installed which will cause trouble
sudo mv openssl openssl.old
sudo touch /etc/profile.d/openssl.sh
sudo nano /etc/profile.d/openssl.sh
#add the following lines and then save > exit:
#!/bin/sh
export PATH=/opt/openssl/bin:${PATH}
export LD_LIBRARY_PATH=/opt/openssl/lib:${LD_LIBRARY_PATH}
sudo chmod +x /etc/profile.d/openssl.sh
sudo nano ~/.bashrc
#add this line
source /etc/profile.d/openssl.sh
echo $PATH
which openssl
openssl
> version
> exit
```

- now we will proceed with the `confd` installation

```bash
./confd-basic-8.0.19.linux.x86_64.installer.bin ~/confd-bin/
source confd-bin/confdrc
man confd
confd --version #must show the version installed
```
