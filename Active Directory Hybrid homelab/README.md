# Hybrid Active Directory Lab

A multi-OS enterprise infrastructure lab integrating **Windows Server, Windows 11 Enterprise, and Ubuntu Linux** into a centralized Active Directory environment.

The project demonstrates cross-platform identity integration, DNS, Kerberos authentication, Samba/Winbind, PAM, Windows domain joining, and centralized Active Directory administration.

---

## Project Overview

The goal of this project was to build a functional enterprise-style Active Directory environment and integrate both Windows and Linux endpoints into the same domain.

The lab demonstrates the workflow of a mixed-OS environment:

```text
Windows Server Domain Controller
              │
              │ Active Directory
              │ DNS / Kerberos / LDAP
              │
       ┌──────┴──────┐
       │             │
   Windows 11     Ubuntu Linux
      Client         Client
       │             │
 Native AD Join   Samba / Winbind
                  + PAM
```

The project also provided hands-on experience troubleshooting the differences between native Windows domain integration and Linux-based Active Directory authentication.

---

# Environment

| Component             | Purpose                                              |
| --------------------- | ---------------------------------------------------- |
| Windows Server        | Active Directory Domain Controller                   |
| Windows 11 Enterprise | Native Active Directory client                       |
| Ubuntu Linux          | Cross-platform Active Directory client               |
| Samba                 | Active Directory integration                         |
| Winbind               | AD identity and authentication integration           |
| PAM                   | Linux authentication and home-directory provisioning |
| DNS                   | Active Directory name resolution                     |
| PowerShell            | Windows administration                               |
| Bash                  | Linux administration                                 |

### Active Directory

**Domain:**

```text
RNORRIS-LAB.LOCAL
```

**NetBIOS Domain:**

```text
LAB
```

**Domain Controller:**

```text
CWM3382
```

**IP Address:**

```text
104.225.141.208
```

### Windows Client

```text
WIN-CLIENT01
Windows 11 Enterprise
```

### Linux Client

```text
rnorris-ubuntu
Ubuntu Linux
```

---

# Architecture

```text
                         Active Directory
                         RNORRIS-LAB.LOCAL
                                │
                                │
                         ┌──────▼──────┐
                         │    CWM3382   │
                         │ Windows      │
                         │ Server       │
                         │ Domain       │
                         │ Controller   │
                         └──────┬───────┘
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
          ┌───────▼────────┐         ┌────────▼────────┐
          │  WIN-CLIENT01  │         │  rnorris-ubuntu │
          │ Windows 11     │         │ Ubuntu Linux    │
          │ Enterprise     │         │                 │
          │ Native AD Join │         │ Samba/Winbind   │
          └────────────────┘         │ PAM             │
                                     └─────────────────┘
```

---

# Key Technical Components

## Windows Active Directory

The Windows Server Domain Controller provides centralized identity and authentication for the environment.

Active Directory was used for:

* User authentication
* Computer authentication
* DNS integration
* Kerberos authentication
* LDAP directory services
* Security groups
* Centralized identity management

The Windows 11 client was joined directly using the native Windows domain-join workflow.

---

# Ubuntu Active Directory Integration

Integrating Ubuntu Linux into Active Directory required several additional components because Linux does not natively participate in Windows domain authentication in the same manner as a Windows client.

The Linux endpoint was integrated using:

* Samba
* Winbind
* Kerberos
* PAM
* DNS
* RID-based identity mapping

---

## 1. DNS Resolution & `systemd-resolved`

### Challenge

Ubuntu's local resolver (`127.0.0.53`) initially failed to correctly resolve the internal Active Directory DNS records required for domain discovery.

This prevented the Linux client from reliably locating the Domain Controller through Active Directory SRV records and resulted in authentication errors such as:

```text
No logon servers are currently available
```

### Solution

The network interface was explicitly configured to use the Active Directory Domain Controller as its DNS server and to route queries for the internal domain appropriately.

```bash
sudo resolvectl dns <INTERFACE_NAME> 104.225.141.208
sudo resolvectl domain <INTERFACE_NAME> ~rnorris-lab.local
```

This allowed the Linux client to correctly locate Active Directory services.

---

## 2. Samba & Winbind Identity Mapping

### Challenge

Initial Winbind configuration did not correctly translate Active Directory Security Identifiers (SIDs) into Linux UIDs/GIDs.

This prevented Linux from properly resolving domain accounts.

### Solution

An explicit RID-based identity mapping configuration was implemented in `/etc/samba/smb.conf`.

```ini
[global]
security = ads
workgroup = LAB
realm = RNORRIS-LAB.LOCAL

idmap config * : backend = tdb
idmap config * : range = 3000-7999

idmap config LAB : backend = rid
idmap config LAB : range = 10000-999999

winbind use default domain = yes
winbind enum users = yes
winbind enum groups = yes

template shell = /bin/bash
template homedir = /home/%D/%U
```

This allowed Active Directory identities to be represented as valid Linux users and groups.

---

## 3. PAM Home Directory Provisioning

### Challenge

Domain authentication succeeded, but newly authenticated users did not automatically receive a local home directory.

### Solution

PAM was configured to create user home directories during the first successful login.

```bash
sudo pam-auth-update
```

The **Create home directory on login** option was enabled.

This allowed domain users to authenticate and receive a usable Linux session without requiring manual home-directory creation.

---

# Windows 11 Enterprise Integration

The Windows client used the native Windows Active Directory workflow.

### Domain Join

The Windows 11 Enterprise endpoint was joined directly to:

```text
RNORRIS-LAB.LOCAL
```

### DNS Configuration

The client was configured to use the Domain Controller for Active Directory DNS resolution.

### Authentication Verification

Successful domain authentication was verified after joining the client to the domain.

The Windows endpoint could then authenticate against the centralized Active Directory environment.

---

# Verification & Testing

The environment was validated through multiple independent tests.

## 1. Active Directory Join — Ubuntu

```bash
sudo net ads testjoin
```

Expected result:

```text
Join is OK
```

---

## 2. Domain Controller Connectivity

```bash
wbinfo --ping-dc
```

Expected result:

```text
checking the NETLOGON for domain[LAB] dc connection to "CWM3382.rnorris-lab.local" succeeded
```

This verified that Winbind could communicate with the Domain Controller.

---

## 3. Active Directory User Resolution

```bash
id administrator
```

Expected output included the mapped Linux UID/GID and Active Directory group memberships:

```text
uid=10500(administrator)
gid=10513(domain users)
groups=10513(domain users),10500(administrator),...
```

This confirmed that Active Directory identities were successfully being resolved by the Linux client.

---

## 4. Fleet Inventory

The Domain Controller was used to enumerate domain computers and their operating-system information.

```powershell
Get-ADComputer -Filter * -Properties OperatingSystem, LastLogonDate |
    Select-Object Name, OperatingSystem, LastLogonDate
```

Example output:

```text
Name            OperatingSystem        LastLogonDate
----            ----------------       -------------
CWM3382         Windows Server...      ...
ROBERT-WIN11    Windows 11 Enterprise  ...
robert-ubuntu   Ubuntu                 ...
```

This provided centralized visibility into the systems participating in the domain.

---

# Troubleshooting Methodology

A major part of this project was troubleshooting the interaction between different operating systems rather than simply following an installation guide.

The troubleshooting process followed a consistent methodology:

```text
1. Identify the failure
        ↓
2. Determine which component is failing
        ↓
3. Gather diagnostic information
        ↓
4. Test DNS / connectivity / authentication
        ↓
5. Isolate the cause
        ↓
6. Apply a targeted configuration change
        ↓
7. Re-test
        ↓
8. Verify domain functionality
```

This was particularly important when troubleshooting DNS, Winbind identity mapping, and PAM authentication.

---

# Skills Demonstrated

## Systems Administration

* Windows Server administration
* Active Directory Domain Services
* Windows 11 administration
* Ubuntu Server/Linux administration
* User and computer management
* PowerShell
* Bash

## Identity & Authentication

* Active Directory
* Kerberos
* LDAP
* Samba
* Winbind
* PAM
* SID-to-UID/GID mapping
* Domain authentication

## Networking

* IPv4 configuration
* DNS
* Active Directory SRV records
* `systemd-resolved`
* Network troubleshooting
* Client-to-domain-controller connectivity

## Cross-Platform Administration

* Windows/Linux domain integration
* Samba configuration
* Winbind configuration
* Linux authentication against Active Directory
* Centralized identity across multiple operating systems

---

# Repository Structure

```text
├── assets/
│   └── Infrastructure screenshots and configuration examples
│
├── documentation/
│   └── Architecture diagrams, workflows, and project screenshots
│
└── README.md
```

The `assets/` directory contains supporting configuration files and infrastructure artifacts.

The `documentation/` directory contains project documentation, architectural diagrams, workflow documentation, and screenshots demonstrating the completed environment.

---

# Future Enhancements

Potential future additions include:

* Implementing Group Policy Objects to restrict SSH access on Linux clients to specific Active Directory security groups.
* Integrating centralized logging and auditing.
* Adding a SIEM platform such as Wazuh.
* Expanding endpoint security monitoring.
* Adding additional Windows and Linux clients to simulate a larger enterprise environment.

---

# Project Outcome

The completed lab successfully demonstrated a mixed Windows/Linux enterprise environment using centralized Active Directory identity management.

```text
                 Active Directory
                       │
          ┌────────────┴────────────┐
          │                         │
      Windows 11                Ubuntu Linux
          │                         │
      Native AD                 Samba/Winbind
        Join                       + PAM
          │                         │
          └────────────┬────────────┘
                       │
                Centralized Identity
```

The project provided practical experience with **Active Directory, DNS, Kerberos, LDAP, Windows administration, Linux administration, Samba, Winbind, PAM, PowerShell, and cross-platform authentication troubleshooting**.

---

## Return Page

[Return to Repository Hub](https://github.com/RobNor12/IT-Automation-Engineering/blob/main/README.md)
