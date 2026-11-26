# Microsoft 365 Help Desk Admin Lab

A hands-on lab where I administered a Microsoft 365 Business Premium trial tenant the way a tiered help desk team would: creating and licensing users, building groups and shared mailboxes, assigning role-based admin access, supporting MFA, and writing up each incident as a ticket-style resolution.

> **Note:** All data in this lab is fictional. Users, company name, and tenant are test-only, and the tenant was decommissioned when the trial ended.

---

## Objectives

- Learn the Microsoft 365 admin center and Entra ID from a help desk perspective
- Design a simple access model: group owners, tiered technicians, and a Global Admin
- Apply least privilege using role-based administration
- Practice common incidents: password resets, group errors, offboarding, restores, and MFA
- Document each resolution in a clear, ticket-style format (issue, cause, fix, verification)

## Environment

| Item | Detail |
|---|---|
| Platform | Microsoft 365 Business Premium (30-day trial) |
| Tenant | `BayouITServicesCo.onmicrosoft.com` (test) |
| Admin tools | Microsoft 365 admin center, Microsoft Entra admin center, Exchange admin center |
| Documentation | Ticket-style write-ups in this README |
| Optional | Microsoft Graph PowerShell, Intune |

**Support tiers:** Tier 1 = Helpdesk Administrator, Tier 2 = User Administrator, Tier 3 = Global Administrator.

## Roles and Ownership

| Account | Role | Purpose |
|---|---|---|
| Admin account(Robert Norris) | Global Administrator | Tenant-level changes and billing only |
| Test IT 1 | Helpdesk Administrator | Tier 1 support (password resets, basic tasks) |
| Test IT 2 | User Administrator | Tier 2 escalations (user removal, license changes) |
| Test HR Owner | Owner of HR group | Manages HR group membership |
| Test Sales Owner | Owner of Sales group | Manages Sales group membership |
| Test IT Owner | Owner of IT-Helpdesk group | Manages IT-Helpdesk group membership |
| Test HR 1, Test HR 2 | Standard users | HR department members |
| Test Sales 1, Test Sales 2 | Standard users | Sales department members |

## Skills Demonstrated

- Microsoft 365 admin center and Entra ID user lifecycle management
- License assignment and troubleshooting
- Microsoft 365 groups, security groups, and group ownership
- Shared mailboxes and group mailboxes
- Role-based access control and tiered escalation
- MFA configuration and troubleshooting
- Sign-in log review
- Ticket-style documentation

---

## Lab Walkthrough

### 1. Tenant setup
[Describe what you did: signed up for the trial, created the admin account, named the tenant, and turned off recurring billing.]

The trial started with only [1] license, which my admin account was already using. I added [9] licenses to the trial subscription so I could create licensed test users.

### 2. Users


### 3. Groups

| Group | Type | Owner | Members |
|---|---|---|---|
| HR | Microsoft 365 | Test HR Manager | Test HR 1, Test HR 2 |
| Sales | Microsoft 365 | Test Sales Manager | Test Sales 1, Test Sales 2 |
| IT-Helpdesk | Security | Test IT Manager | Test IT 1, Test IT 2 |

### 4. Mailboxes
I created a shared mailbox for the help desk: `helpdesksharedemail@BayouITServicesCo.onmicrosoft.com`, with Test IT 1, Test IT 2 and Test IT Owner as members.

### 5. Incidents

Each incident below is written up as a ticket-style resolution.

#### Incident 1: Password reset
- **Reported:** Test_hr_2 reported from their phone that they have forgotten their password and need help
- **Cause:** The user had forgotten their password
- **Fix:** Test_it_1 reset their password and provided them with a temporary password to allow them to log back in 
- **Verification:** Test_hr_2 had signed in as per the request of test_it_2, test_hr_2 gave the help desk email confirming they were able to get back into their account

#### Incident 2: User added to the wrong group
- **Reported:** Test_hr_1 reported to the help desk team that a member was added to their group as they were instructed to by their manager 
- **Cause:** Test_it_1 was incorrectly added to the Human Resources group
- **Fix:** Test_it_1 was removed from the Human Resources group but was still a member of the help desk group
- **Verification:** Test_it_1 no longer showed up as a member of the Human Resources group, and could no longer access that content

#### Incident 3: Employee leaves the company
- **Reported:** Test_sales_owner reported to the help desk group that a member of their group left the company
- **Tier 1 attempt:** Test 1 attempted to remove the removed member, but they did not have sufficient authority 
- **Escalation:** Escalated the incident to help desk tier 2 who removed that member from the company
- **Fix:** Test_it_2
- **Verification:** [Confirmed the user appeared in Deleted users and could not sign in.]

#### Incident 4: User removed by mistake
- **Reported:** [A manager reported the wrong employee had been offboarded.]
- **Cause:** [User was removed in error.]
- **Fix:** [Restored the user from Deleted users, set a new password, and re-added their license and groups.]
- **Verification:** [Signed in as the restored user and confirmed access to Sales resources.]

![Restored user](screenshots/10-restored-user.png)

#### Incident 5: User cannot use MFA
- **Reported:** [User walked up to the help desk after replacing their phone and could no longer approve sign-in prompts.]
- **Identity verification:** [Confirmed the user's identity before making changes, e.g., employee ID and department, and confirmed with their manager.] MFA resets are a common social engineering target, so verification comes first.
- **Cause:** [Registered authentication method was on the old device.]
- **Fix:** [Required MFA re-registration through the user's authentication methods in Entra ID. If Tier 1 lacked permission, note the denial, who it was escalated to, and which role was needed.]
- **Verification:** [User re-registered a new device and signed in successfully, then emailed the help desk mailbox to confirm the issue was resolved.]

*Note: This is a simulated scenario. MFA lockouts are typically handled in person, by phone, or through a manager rather than by email, since a locked-out user may not be able to reach their own inbox.*

![MFA re-registration](screenshots/11-mfa.png)
![Sign-in logs](screenshots/12-signin-logs.png)

---

## Troubleshooting and Lessons Learned

**Not enough licenses.** Creating a licensed user failed because the trial started with only one license. I added licenses to the subscription and confirmed recurring billing was still off.

**Shared mailbox messages not appearing.** A technician did not see test emails because shared mailboxes do not deliver copies into members' personal inboxes. Members open the shared mailbox from their own Outlook. After adding it, the messages appeared.

**Helpdesk Administrator cannot remove users.** I created a Tier 2 account with the User Administrator role instead of over-privileging the Tier 1 account, and handled offboarding through escalation.

Key takeaways:
- [What surprised you or what you'd do differently]
- [One thing about how cloud identity differs from on-prem Active Directory]
- [One thing about how you'd explain this to an end user]

## How This Connects to My Other Labs

- [Azure Hybrid Active Directory Lab](../IT-Infrastructure-Projects): on-prem identity concepts that map directly to Entra ID
- [IT Help Desk & Infrastructure Lab](../IT-Infrastructure-Projects): earlier lab covering a FreeScout ticketing workflow and escalation

**Author:** Robert Norris III
[LinkedIn](https://www.linkedin.com/in/robertn-331315345) | [GitHub](https://github.com/RobNor12)
