from ncclient import manager
from lxml import etree
import xml.etree.ElementTree as ET

NS_DEV = "http://org/openroadm/device"
FILTER_OPENROADM_DEVICE = f"""
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" type="subtree">
  <org-openroadm-device xmlns="{NS_DEV}">
    <circuit-packs/>
  </org-openroadm-device>
</filter>
"""


def t(e):
    return e.text.strip() if e is not None and e.text else ""


with manager.connect(host="10.100.101.11", port=2022, username="admin", password="admin", hostkey_verify=False, allow_agent=False, look_for_keys=False, timeout=15) as m:
    # operational (config + state)

    reply = m.get(filter=FILTER_OPENROADM_DEVICE)
    root = ET.fromstring(reply.data_xml)

    # find all port nodes under circuit-packs
    ports = root.findall(f".//{{{NS_DEV}}}ports")

    print(f"{'PORT-NAME':20} {'DIRECTION':10} {'QUAL':16} {'LOGICAL-CP'}")
    print("-"*70)
    for p in ports:
        name = t(p.find(f"{{{NS_DEV}}}port-name"))
        direc = t(p.find(f"{{{NS_DEV}}}port-direction"))
        qual = t(p.find(f"{{{NS_DEV}}}port-qual"))
        lcp = t(p.find(f"{{{NS_DEV}}}logical-connection-point"))
        print(f"{name:20} {direc:10} {qual:16} {lcp}")

    print(f"\nTotal ports: {len(ports)}")
