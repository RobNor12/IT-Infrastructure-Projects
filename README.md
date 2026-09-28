# FreeScout Help Desk Lab

A hands-on IT help desk and systems administration lab built around **FreeScout, Microsoft Active Directory, Windows, Linux, and Microsoft Azure**.

The purpose of this project is to simulate a small organization's internal IT environment and demonstrate practical help desk workflows, including ticket intake, troubleshooting, escalation, documentation, identity management, and basic Windows administration.

---

## Project Overview

This lab combines a functional ticketing system with an Active Directory environment and Windows client machines.

The environment is hosted primarily in **Microsoft Azure**, with FreeScout running on an Ubuntu Server VM and Windows machines joined to the Active Directory domain.

The goal was not simply to install a ticketing system, but to create a realistic workflow:

```text
User experiences problem
        ↓
User submits help desk ticket
        ↓
FreeScout receives ticket
        ↓
IT technician investigates
        ↓
Troubleshooting / diagnostics
        ↓
Issue resolved OR escalated
        ↓
User receives response
        ↓
Ticket documented
```

---

## Environment

| Component                | Purpose                                    |
| ------------------------ | ------------------------------------------ |
| Microsoft Azure          | Infrastructure hosting                     |
| Ubuntu Server            | FreeScout help desk server                 |
| FreeScout                | Ticket management                          |
| Microsoft Windows Server | Active Directory / DNS                     |
| Active Directory         | Identity and authentication                |
| WIN01                    | IT technician workstation                  |
| WIN02                    | Simulated end-user workstation             |
| Gmail                    | Help desk email integration                |
| PowerShell               | Windows administration and troubleshooting |
| Group Policy             | Endpoint configuration and access control  |

### Active Directory

**Domain:**

```text
ad.hybridlab.test
```

**Domain Controller:**

```text
DC02
10.10.10.4
```

### Help Desk Server

```text
helpdesk.hybridlab.test
10.10.30.5
```

### Windows Clients

```text
WIN01 — IT technician workstation
WIN02 — simulated end-user workstation
```

---

## Architecture

```text
                         Microsoft Azure
                               │
             ┌─────────────────┴─────────────────┐
             │                                   │
        Active Directory                    Help Desk Server
             │                                   │
           DC02                              Ubuntu
       10.10.10.4                         10.10.30.5
             │                                   │
             │                              FreeScout
             │                                   │
       ┌─────┴─────┐                         Gmail
       │           │
     WIN01       WIN02
   Technician      User
       │           │
       └─────┬─────┘
             │
       Domain: ad.hybridlab.test
```

---

# FreeScout Configuration

FreeScout was installed on an Ubuntu Server VM and configured as the central help desk platform.

The help desk mailbox was configured with a dedicated Gmail account.

### Incoming Mail

```text
IMAP Server: imap.gmail.com
Port: 993
Security: SSL/TLS
```

### Outgoing Mail

```text
SMTP Server: smtp.gmail.com
Port: 587
Security: STARTTLS
```

A Gmail App Password was used for authentication.

FreeScout's scheduler was configured to automatically retrieve incoming messages.

```cron
* * * * * php /var/www/freescout/artisan schedule:run >> /dev/null 2>&1
```

This allowed the complete ticket workflow to function:

```text
User Email
    ↓
Gmail
    ↓
FreeScout
    ↓
Help Desk Ticket
    ↓
Technician Response
    ↓
Email Response
```

---

# Active Directory Integration

The Windows machines were joined to the lab's Active Directory domain:

```text
ad.hybridlab.test
```

Active Directory was used for:

* User authentication
* Computer authentication
* Security groups
* Group Policy
* Remote Desktop access
* DNS
* Centralized identity management

The lab also uses security groups to control administrative and remote-access permissions rather than manually configuring every workstation.

---

# Group Policy

A dedicated Group Policy Object was created for Remote Desktop access:

```text
Lab - Remote Desktop Access
```

The policy configures the local **Remote Desktop Users** group on domain-joined workstations.

The intended management structure is:

```text
Active Directory Security Group
            ↓
Local Remote Desktop Users
            ↓
Windows Workstation
```

This allows Remote Desktop permissions to be managed centrally through Active Directory rather than manually configuring each workstation.

The policy was tested on WIN02 using:

```powershell
gpresult /r /scope computer
```

and:

```powershell
Get-LocalGroupMember -Group "Remote Desktop Users"
```

---

# Help Desk Incident Simulations

Three incidents were created to simulate realistic internal IT support requests.

The incidents were intentionally designed to demonstrate different troubleshooting and escalation scenarios.

---

## Incident 1 — Password Reset

### User Report

The simulated user was unable to authenticate because of a password-related issue.

### Troubleshooting

The technician verified the user's account information and determined that the issue required an administrative password reset.

### Resolution

The password was reset through the appropriate administrative process.

The user was then able to authenticate successfully.

### Skills Demonstrated

* Active Directory
* User account management
* Authentication troubleshooting
* Password administration
* Help desk ticket documentation

---

# Incident 2 — DNS Resolution Failure

### User Report

The user reported that they were unable to access resources by hostname.

### Troubleshooting

The technician investigated name resolution using tools such as:

```powershell
nslookup
```

The issue was isolated to DNS resolution rather than general workstation connectivity.

### Escalation

Because DNS infrastructure is outside the normal authority of the simulated help desk technician, the issue was escalated rather than making unauthorized changes to the DNS infrastructure.

The ticket documented the troubleshooting performed and the suspected cause.

### Resolution

The user was informed that the issue had been escalated to the appropriate technician for further investigation.

### Skills Demonstrated

* DNS troubleshooting
* `nslookup`
* Network troubleshooting
* Problem isolation
* Ticket documentation
* Proper escalation procedures

---

# Incident 3 — Internet Connectivity Failure

### User Report

The user reported that they could not access the Internet.

### Initial Troubleshooting

The technician verified that the workstation still had valid network configuration.

The technician then tested DNS resolution:

```powershell
nslookup google.com
```

DNS resolution succeeded.

This established that the workstation could still communicate with the DNS service.

The technician then tested external HTTPS connectivity:

```powershell
Test-NetConnection google.com -Port 443
```

The test failed.

This narrowed the problem from general network connectivity to outbound Internet connectivity.

### Investigation

The workstation was found to have an outbound firewall restriction affecting HTTP/HTTPS traffic.

The simulated firewall rule was:

```text
HELPDESK - Simulated Internet Outage
```

The rule blocked outbound TCP traffic on:

```text
80
443
```

### Escalation

Because firewall configuration may fall outside the authority of a first-line help desk technician, the issue was escalated to the appropriate systems/network technician rather than having the help desk technician modify the firewall policy.

The user was informed:

> "I'll send a technician your way."

### Resolution

The firewall configuration was subsequently restored by the appropriate administrative role.

### Skills Demonstrated

* TCP/IP troubleshooting
* DNS troubleshooting
* PowerShell networking tools
* Firewall investigation
* Network isolation
* Escalation
* Help desk communication
* Documentation

---

# Troubleshooting Methodology

The incidents were designed around a consistent troubleshooting process:

```text
1. Identify the problem
        ↓
2. Gather information
        ↓
3. Establish what is working
        ↓
4. Isolate the failure
        ↓
5. Determine whether the issue is within help desk scope
        ↓
6. Resolve or escalate
        ↓
7. Verify service restoration
        ↓
8. Document the result
```

This approach avoids immediately changing configuration without first determining the actual failure.

---

# Help Desk Scope

An important part of the lab is demonstrating that a help desk technician does **not necessarily have unrestricted administrative authority**.

The technician is expected to:

* Troubleshoot the workstation
* Gather diagnostic information
* Identify likely causes
* Perform authorized fixes
* Document findings
* Escalate issues outside their permissions

For example:

```text
Password problem
       ↓
Help Desk
       ↓
Resolve
```

while:

```text
DNS infrastructure problem
       ↓
Help Desk investigates
       ↓
Escalate
```

and:

```text
Firewall/network infrastructure problem
       ↓
Help Desk investigates
       ↓
Escalate
```

This models a tiered IT support environment rather than treating the help desk account as a domain administrator.

---

# Tools Used

### Ticketing

* FreeScout
* Gmail
* IMAP
* SMTP

### Microsoft Infrastructure

* Active Directory Domain Services
* DNS
* Group Policy
* Windows Server
* Windows 11
* Remote Desktop

### Networking

* TCP/IP
* DNS
* Network troubleshooting
* Azure networking
* NSGs
* Firewall rules

### Administration

* PowerShell
* Linux shell
* Apache
* PHP
* MariaDB
* Azure PowerShell

---

# Skills Demonstrated

## Systems Administration

* Windows Server administration
* Active Directory
* User and computer management
* Group Policy
* Remote Desktop
* Linux server administration
* Web application deployment

## Networking

* IPv4 configuration
* DNS troubleshooting
* TCP connectivity testing
* Firewall troubleshooting
* Azure virtual networking
* Network security groups

## Security

* Active Directory security groups
* Access control
* Remote Desktop permissions
* Firewall configuration
* Principle of least privilege
* Administrative escalation

## Help Desk

* Ticket creation
* User communication
* Troubleshooting methodology
* Documentation
* Issue isolation
* Escalation
* Verification

---

# Project Status

The core environment is operational.

The lab successfully demonstrates:

* Functional FreeScout ticketing
* Email-to-ticket workflow
* Technician-to-user email communication
* Active Directory authentication
* Domain-joined Windows clients
* Group Policy
* Centralized Remote Desktop access
* DNS
* Network troubleshooting
* Firewall troubleshooting
* Help desk escalation

The project demonstrates both **technical troubleshooting** and the operational side of IT support: determining what can be resolved at the help desk, documenting what was discovered, and escalating issues when administrative authority or infrastructure ownership falls outside the technician's role.

---

# Final Workflow

```text
                         User
                          │
                          ▼
                     Gmail Email
                          │
                          ▼
                      FreeScout
                          │
                          ▼
                    Help Desk
                          │
                 ┌────────┴────────┐
                 │                 │
              Resolve           Escalate
                 │                 │
                 ▼                 ▼
          User notified       Technician /
                              Administrator
                                    │
                                    ▼
                              Infrastructure
```

---

## Project Goal

The purpose of this project was to build a realistic environment that demonstrates more than simply configuring servers.

It combines **systems administration, networking, security, Active Directory, cloud infrastructure, troubleshooting, ticket management, documentation, and escalation procedures** into one working environment.

The end result is a small but functional IT infrastructure lab that simulates the workflow of an internal help desk supporting Windows users in a domain environment.

### Return page

[Return to Repository Hub](https://github.com/RobNor12/IT-Automation-Engineering/blob/main/README.md)
