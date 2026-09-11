from ncclient import manager
from ncclient.operations import RPCError
from lxml import etree  # ncclient uses lxml under the hood

HOST, PORT, USER, PASSWORD = "127.0.0.1", 830, "netconf", "netconf"

CFG = """
<nc:config
    xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"
    xmlns:if="urn:ietf:params:xml:ns:yang:ietf-interfaces"
    xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
  <if:interfaces>
    <if:interface>
      <if:name>loopback-test0</if:name>
      <if:type>ianaift:softwareLoopback</if:type>
      <if:enabled>true</if:enabled>
    </if:interface>
  </if:interfaces>
</nc:config>
"""

FLT = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" type="subtree">
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
</filter>
"""

def show_rpc_error(e: RPCError):
    try:
        # e._raw is an lxml Element; pretty-print it
        print(etree.tostring(e._raw, pretty_print=True).decode())
    except Exception:
        print(str(e))

with manager.connect(host=HOST, port=PORT, username=USER, password=PASSWORD,
                     hostkey_verify=False, allow_agent=False, look_for_keys=False, timeout=20) as m:
    print("Lock candidate…")
    m.lock(target="candidate")
    try:
        print("Edit candidate…")
        r = m.edit_config(target="candidate", config=CFG, default_operation="merge")
        print("Validate…")
        m.validate()
        print("Commit…")
        m.commit()
    except RPCError as e:
        print("RPCError from server:")
        show_rpc_error(e)
        raise
    finally:
        try: m.unlock(target="candidate")
        except: pass

    print("Read back from running…")
    rb = m.get_config(source="running", filter=FLT)
    print(etree.tostring(etree.fromstring(rb.xml.encode()), pretty_print=True).decode())
    print("\n")
    print(etree.tostring(etree.fromstring(rb.data_xml.encode()), pretty_print=True).decode())