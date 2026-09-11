# How to prepare a `openROADM` device

I am trying to build my own `ROADM` device using the `openroadm` driver. There are couple of dependencies that needs to be installed first. Let's being:

- first we have to configure `confd` for which I have followed this [procedure](./confd/README.md).
- for the `ROADM` configuration I have followed this [procedure](./yang/README.md).
- next we have to build the `device`:

```bash
#from the root directory
for f in yang/*.yang; do
  if grep -q 'submodule' "$f"; then
    echo "Skipping submodule: $f"
    continue
  fi
  name=$(basename "$f" .yang)
  echo "Compiling: $name.yang"
  confdc -c --yangpath yang -o "confd/$name.fxs" "$f"
done
#some error will show up due to missing dependency, just ignore them
```

- prepared the `confd.conf` [file](./confd/confd.conf) and `users.xml` [file](./data/aaa_init/users.xml)
- prepare the directories and user:

```bash
mkdir -p data/state data/cdb data/ssh
mkdir -p "$PWD/data/ssh"
ssh-keygen -t ed25519 -N '' -f "$PWD/data/ssh/ssh_host_ed25519_key"
ssh-keygen -t rsa     -b 2048 -N '' -f "$PWD/data/ssh/ssh_host_rsa_key"
confd --foreground --conf confd.conf
```

Finally I couldn't build the `openroadm` device but I got a clear idea how `confd` builds the `openroadm` device and how `yang` files are working. Maybe I will use the knowledge later.
