# ONOS: Open Network Operating System

## What is ONOS?

ONOS is the only SDN controller platform that supports the transition from legacy “brown field” networks to SDN “green field” networks. This enables exciting new capabilities, and disruptive deployment and operational cost points for network operators.

## Top-Level Features

- High availability through clustering and distributed state management.
- Scalability through clustering and sharding of network device control.
- Performance that is good for a first release, and which has an architecture that will continue to support improvements.
- Northbound abstractions for a global network view, network graph, and application intents.
- Pluggable southbound for support of OpenFlow, P4Runtime, and new or legacy protocols.
- Graphical user interface to view multi-layer topologies and inspect elements of the topology.
- REST API for access to Northbound abstractions as well as CLI commands.
- CLI for debugging.
- Support for both proactive and reactive flow setup.
- SDN-IP application to support interworking with traditional IP networks controlled by distributed routing protocols such as BGP.
- IP-Optical use case demonstration.

For the final official version please switch to `master` branch.

---

## About This Fork

This repository is a fork of the original **Open Network Operating System (ONOS)** controller originally developed and maintained by the **Open Networking Foundation (ONF)**.

### Upstream Repository Status

The original official upstream repository previously cloned via:

```bash
git clone https://gerrit.onosproject.org/onos
```

is no longer available or actively maintained.

### Motivation and Maintenance

This fork is maintained for **educational and research purposes** by [Alessio Giorgetti](https://github.com/alessiocnit), an active contributor to the official upstream ONOS repository (with contributions including optical network extensions and ODTN drivers). The goal of this project is to keep ONOS accessible, buildable on modern environments, and ready for use in SDN labs, experiments, and research.

### References

- **Open Networking Foundation (ONF)**: [https://opennetworking.org/](https://opennetworking.org/)
- **Upstream GitHub Mirror (Archive)**: [https://github.com/opennetworkinglab/onos](https://github.com/opennetworkinglab/onos)
- **ONOS Architecture Whitepaper**: [ONOS Architecture (PDF)](https://stordis.com/wp-content/uploads/2019/05/Whitepaper-ONOS.pdf)

---

## Documentation

An archived and searchable version of the official ONOS Classic documentation and wiki is maintained at:

- **ONOS Classic Wiki**: [https://andrea-campanella.github.io/onos-classic-wiki/](https://andrea-campanella.github.io/onos-classic-wiki/)

---

## Getting Started: Installing ONOS

Choose one of the following installation methods to get started:

- **Build from source**: follow the [From Source Guide](./docs/FROM_SOURCE.md).
- **Run with Docker Hub**: follow the [Docker Hub Guide](./docs/FROM_DOCKER_HUB.md).
- **Run with Kathará**: follow the [Kathará + ONOS Guide](./docs/katharaXonos/FROM_KATHARA_CORE.md).

---

## Maintainer

- **Alessio Giorgetti**
  - Role: Associate Professor
  - Affiliation: Department of Information Engineering (Dipartimento di Ingegneria dell'Informazione), University of Pisa, Pisa, Italy
  - GitHub: [@alessiocnit](https://github.com/alessiocnit)

### Lab Activities

- **ASM CHAFIULLAH BHUIYAN**
  - Role: Research Fellow
  - Affiliation: University of Pisa, Pisa, Italy

---

## Official License

ONOS (Open Network Operating System) is published under the [Apache License 2.0](LICENSE.txt).

## Official Acknowledgements

YourKit supports open source projects with innovative and intelligent tools for monitoring and profiling Java and .NET applications.
YourKit is the creator of [YourKit Java Profiler](https://www.yourkit.com/java/profiler/), [YourKit .NET Profiler](https://www.yourkit.com/.net/profiler/) and [YourKit YouMonitor](https://www.yourkit.com/youmonitor/).

![YourKit](https://www.yourkit.com/images/yklogo.png)
