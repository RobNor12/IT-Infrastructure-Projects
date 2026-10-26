# Azure Hybrid Active Directory & Domain Controller Redundancy Lab

A hybrid Active Directory infrastructure lab demonstrating **Windows Server administration, Active Directory Domain Services, DNS, Azure networking, VPN connectivity, domain-controller redundancy, and cross-platform client discovery**.

The environment consists of two writable domain controllers located in separate hosting environments. The primary lab infrastructure is hosted in Microsoft Azure, while a second domain controller is hosted externally through Kamatera and connected to Azure through an IKEv2 Point-to-Site VPN.

Windows and Linux clients are joined to the same Active Directory domain and can discover available domain controllers through Active Directory DNS and DC Locator.

---

# Project Overview

The goal of this project was to expand a single-domain-controller Active Directory environment into a geographically separated, redundant infrastructure.

The completed environment demonstrates:

```text
                         Active Directory
                         ad.hybridlab.test
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
          ┌──────▼──────┐               ┌──────▼──────┐
          │    DC02     │◄── Replication ─►│    DC03     │
          │   Azure     │      VPN          │  Kamatera  │
          │ AD / DNS / GC│                  │ AD / DNS / GC│
          └──────┬──────┘               └──────┬──────┘
                 │                             │
                 └──────────────┬──────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
              Windows Client           Linux Client
```

This project focuses on the relationship between **Active Directory, DNS, replication, network connectivity, and domain-controller discovery**.

---

# Objectives

* Deploy and administer Active Directory Domain Services in Microsoft Azure.
* Configure DNS for an Active Directory environment.
* Configure Azure virtual networking and Network Security Groups.
* Establish secure connectivity between Azure and an external network.
* Configure an IKEv2 Point-to-Site VPN.
* Deploy a second writable domain controller outside Azure.
* Configure and verify Active Directory replication.
* Configure both domain controllers as Global Catalog servers.
* Validate domain-controller discovery from Windows and Linux clients.
* Troubleshoot DNS and Active Directory replication failures.

---

# Environment

| Component      | Platform                         | Role                                   |
| -------------- | -------------------------------- | -------------------------------------- |
| DC02           | Microsoft Azure / Windows Server | Domain Controller, DNS, Global Catalog |
| DC03           | Kamatera / Windows Server 2022   | Domain Controller, DNS, Global Catalog |
| Windows Client | Microsoft Azure                  | Domain-joined Windows endpoint         |
| Linux Client   | Microsoft Azure / Ubuntu         | Domain-joined Linux endpoint           |

### Active Directory

**Domain:**

```text id="7jgjqa"
ad.hybridlab.test
```

### Domain Controllers

**DC02**

```text id="8unqhc"
Location: Microsoft Azure
Role: Active Directory / DNS / Global Catalog
IP: 10.10.10.4
```

**DC03**

```text id="7v15x5"
Location: Kamatera
Role: Active Directory / DNS / Global Catalog
```

---

# Architecture

![Hybrid Active Directory Architecture](./assets/azure/architecture.png)

The environment uses an Azure Point-to-Site VPN to provide connectivity between the Azure virtual network and the externally hosted DC03 server.

The two environments operate as part of the same Active Directory domain.

### Domain Controller Roles

**DC02**

* Active Directory Domain Services
* DNS
* Global Catalog
* Azure-hosted infrastructure
* Primary infrastructure endpoint for the Azure environment

**DC03**

* Active Directory Domain Services
* DNS
* Global Catalog
* External domain-controller redundancy
* Active Directory replication partner

### Client Discovery

Windows and Linux clients use Active Directory DNS and DC Locator to discover available domain controllers.

This allows clients to locate domain services without relying on a single hard-coded domain controller.

---

# Implementation

## Azure Domain Controller

The initial Active Directory environment was deployed in Microsoft Azure using Windows Server.

The server was configured with:

* Active Directory Domain Services
* DNS
* Global Catalog
* Azure Virtual Network
* Network Security Group
* PowerShell-based administration

DC02 operates as a writable domain controller for the `ad.hybridlab.test` domain.

---

# External Domain Controller

A separate Windows Server 2022 system was deployed through Kamatera and integrated into the existing Active Directory domain.

DC03 was promoted to a writable domain controller and configured as a Global Catalog server.

![DC03 Domain Controller](./assets/dc03/dc03.png)

This provided a second domain controller outside the Azure environment.

The separation between Azure and the external hosting environment allows the lab to demonstrate domain-controller redundancy across independent networks.

---

# Azure Point-to-Site VPN

An IKEv2 Point-to-Site VPN was configured to provide connectivity between the Azure environment and the external DC03 server.

DC03 received the VPN address:

```text id="3ndmgl"
172.16.100.2
```

The VPN provided connectivity between DC03 and the Azure domain controller:

```text id="cr9hmm"
DC02
10.10.10.4
```

![Azure P2S VPN Session](./assets/azure/azure_vpn.png)

The VPN connection allowed Active Directory replication and other domain-controller communication to occur between the separate hosting environments.

---

# Active Directory Replication

Replication between DC02 and DC03 was verified using `repadmin`.

Final replication status:

```text id="xw3hs0"
Source DSA          fails/total
DC02                0 / 5
DC03                0 / 5
```

![AD Replication Status](./assets/dc03/dc03_rs.png)

The successful replication status confirmed that Active Directory directory data could be synchronized between the Azure and external domain controllers.

---

# Domain Controller Health

DC03 was validated using `dcdiag` for DNS, NetLogons, and domain-controller advertising.

Final health checks included:

```text id="6nuxg4"
DC03 passed test Advertising
DC03 passed test NetLogons
DC03 passed test DNS

ad.hybridlab.test passed test DNS
```

![DC03 Health Checks](./assets/dc03/dc03_dctest.png)

These tests provided additional verification that DC03 was correctly functioning as an Active Directory domain controller.

---

# Client Domain-Controller Discovery

The Windows and Linux clients were joined to:

```text id="1j13d5"
ad.hybridlab.test
```

Both clients were tested to verify that they could discover available domain controllers through Active Directory DNS and DC Locator.

---

## Windows Client

The Windows client was tested using:

```powershell id="c0ojy0"
nltest /dsgetdc:ad.hybridlab.test
```

The client successfully discovered an available domain controller.

![Windows Domain Controller Discovery](./assets/win01/win01_ntest.png)

---

## Linux Client

The Linux client was tested using an Active Directory DNS SRV query:

```bash id="e4ijhz"
nslookup -type=SRV _ldap._tcp.ad.hybridlab.test
```

The returned records included both DC02 and DC03.

![Linux Domain Controller Discovery](./assets/lnx01/lnx-01.png)

This demonstrated that Active Directory DNS contained the required service records for locating the available domain controllers.

---

# Troubleshooting

The implementation involved several Active Directory and DNS troubleshooting scenarios.

## Active Directory Replication Error 8524

One significant issue occurred when Active Directory replication reported error `8524`, indicating a DNS lookup failure.

The issue was investigated using:

```text id="w8tsm6"
dcdiag
repadmin
nslookup
nltest
```

The investigation identified DNS registration issues affecting the new domain controller.

After correcting the DNS configuration and forcing DNS/Netlogon registration, the required Active Directory SRV and CNAME records became available.

Replication was subsequently re-tested and completed successfully with:

```text id="8y7p5x"
DC02    0 / 5 failures
DC03    0 / 5 failures
```

This troubleshooting process demonstrated the relationship between:

```text id="v8g1q2"
DNS
 ↓
Netlogon Registration
 ↓
Active Directory Service Records
 ↓
Domain Controller Discovery
 ↓
Replication
```

---

# Verification & Testing

The final environment successfully demonstrated:

* Two writable Active Directory domain controllers.
* Both domain controllers operating as Global Catalog servers.
* Successful DNS registration for DC03.
* Successful Active Directory replication between DC02 and DC03.
* Successful DNS health checks.
* Successful NetLogon health checks.
* Successful domain-controller advertising checks.
* Successful Azure-to-external connectivity through the IKEv2 VPN.
* Windows client domain-controller discovery.
* Linux client domain-controller discovery.
* Active Directory service records available through DNS.

---

# Troubleshooting Methodology

The project followed a structured infrastructure troubleshooting process:

```text id="o9rj4a"
1. Identify the failure
        ↓
2. Gather diagnostic information
        ↓
3. Determine which infrastructure component is failing
        ↓
4. Test DNS / connectivity / authentication
        ↓
5. Isolate the root cause
        ↓
6. Apply a targeted configuration change
        ↓
7. Re-test the affected service
        ↓
8. Verify the entire environment
```

The replication/DNS issue was particularly useful for demonstrating that an apparent Active Directory replication problem can originate from an underlying DNS or network-registration problem.

---

# Skills Demonstrated

## Systems Administration

* Windows Server administration
* Active Directory Domain Services
* Domain Controller deployment
* Global Catalog configuration
* PowerShell administration
* Windows client administration
* Ubuntu Linux administration

## Identity & Authentication

* Active Directory
* Kerberos
* LDAP
* DNS-based domain discovery
* Domain-controller discovery
* Active Directory replication

## Networking

* IPv4 networking
* DNS
* Azure Virtual Network
* Network Security Groups
* Point-to-Site VPN
* IKEv2
* Azure-to-external network connectivity
* Network troubleshooting

## Infrastructure Redundancy

* Multiple writable domain controllers
* Global Catalog redundancy
* Cross-network Active Directory replication
* Domain-controller discovery
* DNS service redundancy

## Troubleshooting

* `dcdiag`
* `repadmin`
* `nltest`
* `nslookup`
* DNS troubleshooting
* Active Directory replication troubleshooting
* NetLogon troubleshooting

---

# Repository Structure

```text id="d9xvab"
├── assets/
│   ├── azure/
│   │   ├── architecture.png
│   │   └── azure_vpn.png
│   │
│   ├── dc03/
│   │   ├── dc03.png
│   │   ├── dc03_rs.png
│   │   └── dc03_dctest.png
│   │
│   ├── win01/
│   │   └── win01_ntest.png
│   │
│   └── lnx01/
│       └── lnx-01.png
│
├── documentation/
│   └── Additional project documentation
│
└── README.md
```

The `assets/` directory contains screenshots and infrastructure evidence collected during implementation and verification.

The `documentation/` directory contains supporting project documentation and diagrams.

---

# Future Enhancements

Potential future additions include:

* Adding additional domain-joined Windows and Linux clients.
* Implementing more granular Group Policy controls.
* Adding centralized Active Directory auditing.
* Integrating Windows and Linux event collection.
* Deploying a SIEM platform such as Wazuh.
* Expanding the environment into a larger multi-site Active Directory topology.
* Testing domain availability during simulated domain-controller outages.

---

# Project Outcome

The completed environment successfully demonstrated a geographically separated Active Directory infrastructure with redundant domain controllers.

```text id="v2m6af"
                    ad.hybridlab.test
                           │
             ┌─────────────┴─────────────┐
             │                           │
        ┌────▼─────┐                 ┌────▼─────┐
        │   DC02   │◄─── Replication ─►│   DC03   │
        │  Azure   │      via VPN      │ Kamatera │
        │ AD/DNS/GC│                   │ AD/DNS/GC│
        └────┬─────┘                   └────┬─────┘
             │                              │
             └──────────────┬───────────────┘
                            │
                  Domain Controller
                       Discovery
                            │
                    ┌───────┴───────┐
                    │               │
                Windows           Linux
                 Client           Client
```

The project provided hands-on experience with **Active Directory, DNS, domain-controller redundancy, Global Catalogs, Active Directory replication, Azure networking, VPN connectivity, Windows administration, Linux administration, and infrastructure troubleshooting**.

---

## Return Page

[Return to Repository Hub](https://github.com/RobNor12/IT-Automation-Engineering/blob/main/README.md)
