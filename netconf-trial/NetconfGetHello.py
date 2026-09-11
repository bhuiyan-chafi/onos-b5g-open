from xml.dom import minidom
from NetconfConnectionImpl import NetconfConnection


host: str = "127.0.0.1"
port: int = 830
username: str = "netconf"
password: str = "netconf"


def pretty(x: str) -> str:
    try:
        return minidom.parseString(x).toprettyxml()
    except:
        return x


with NetconfConnection(host, port, username, password) as netconf_connection:
    print("Connected. Capabilities:")
    for c in netconf_connection.capabilities:
        print(" -", c)
