# Running ONOS from Docker Hub

This tutorial explains how to pull the official ONOS Docker image from Docker Hub and run it inside a dedicated Docker network. This guide assumes Docker is already installed and properly running on your system.

## 1. Create an Isolated Docker Network

As an SDN controller, running ONOS in an isolated Docker network provides clean separation for network simulations, predictable IP assignments, and multi-node topologies.

Create a custom Docker bridge network:

```bash
docker network create --subnet "172.28.0.0/16" "labnet"
```

## 2. Run the ONOS Container

Launch the ONOS container in detached mode (`-d`) attached to the `labnet` network:

```bash
docker run -d \
  --name "onos-docker" \
  --network "labnet" \
  --ip "172.28.0.11" \
  -p 8181:8181 \
  -p 6653:6653 \
  -p 8101:8101 \
  onosproject/onos:latest
```

### Port Mappings

- **`8181`**: ONOS Web GUI and REST API.
- **`6653`**: OpenFlow protocol port for connecting SDN switches.
- **`8101`**: Apache Karaf SSH CLI.

## 3. Verify Container Status and Logs

Check that the container is active and running:

```bash
docker ps -f name=onos-docker
```

View the ONOS startup logs:

```bash
docker logs -f onos-docker
```

## 4. Access the Web GUI

Open your browser and navigate to:

- **URL**: [http://localhost:8181/onos/ui](http://localhost:8181/onos/ui)
- **Username**: `onos` or `karaf`
- **Password**: `rocks` or `karaf`

## 5. Access the ONOS CLI

Connect to the ONOS CLI directly over SSH:

```bash
ssh -p 8101 onos@localhost
```

When prompted for the password, enter **`rocks`**.

## 6. Stop and Clean Up

When you are done testing, stop and remove the container and network:

```bash
# Stop and remove the ONOS container
docker stop onos-docker && docker rm onos-docker

# Remove the test network
docker network rm labnet
```
