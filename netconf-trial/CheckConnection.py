# save as hello.py
from ncclient import manager
m = manager.connect(host="10.100.101.11", port=2022, username="admin", password="admin",
                    hostkey_verify=False, allow_agent=False, look_for_keys=False, timeout=10)
print("Connected. Capabilities:", len(list(m.server_capabilities)))
for c in m.server_capabilities:
    print(" -", c)
