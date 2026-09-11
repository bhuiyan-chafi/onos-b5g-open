# Creating a NETCONF server

## create docker container

```bash
docker run -it --name sysrepo -p 830:830 --rm sysrepo/sysrepo-netopeer2:latest
````

## access the container

```bash
ssh netconf@localhost -p 830 -s netconf #password:netconf
find / -name 'iana-if-type@*.yang' 2>/dev/null
# /opt/dev/libyang/tests/modules/yang/iana-if-type@2014-05-08.yang
sysrepoctl -i /opt/dev/libyang/tests/modules/yang/iana-if-type@2014-05-08.yang
```

The container exits after sometime due to inactivity.

## install python client

```bash
python3 -m pip install ncclient #make sure you have pip installed
```

## python script to read data

Check out this [python file](./NetconfGetHello.py) and run it:

```bash
python3 NetconfGetHello.py
```

To push a configuration checkout [this file](./NetconfWrite.py).

## For the existing ROADM we have

Execute or have a look at [this file](./ReadRoadmPorts.py)
