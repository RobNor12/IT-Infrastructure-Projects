# Credential Generator & Lifecycle Manager

A Python-based administrative utility designed to automate the creation and decommissioning of standardized organizational credentials while reducing manual work and input errors.

The project demonstrates practical scripting, input validation, credential lifecycle management, CSV-based data persistence, administrative authentication, and defensive programming.

---

# Project Overview

Managing credentials manually can introduce inconsistent naming, unnecessary administrative work, and avoidable input errors.

This utility was designed to provide a standardized workflow for:

```text
Administrator Authentication
          ↓
Credential Generation
          ↓
Credential Persistence
          ↓
Credential Review
          ↓
Credential Decommissioning
          ↓
Updated Credential Records
```

The program uses predefined naming conventions and validation rules to produce standardized credential identifiers while providing administrators with an interactive method for reviewing and removing existing records.

---

# Objectives

* Automate standardized credential generation.
* Reduce manual credential-creation errors.
* Enforce organizational naming conventions.
* Validate administrative access before performing credential-management operations.
* Provide an interactive credential decommissioning workflow.
* Maintain credential records using structured local data.
* Implement defensive input validation throughout the application.
* Practice Python scripting and administrative automation.

---

# Environment

| Component             | Technology      | Purpose                               |
| --------------------- | --------------- | ------------------------------------- |
| Application           | Python          | Core application logic                |
| Data Processing       | Pandas          | CSV data manipulation and persistence |
| Credential Generation | Python `random` | Randomized identifier generation      |
| File Handling         | Python `os`     | File and path validation              |
| Program Control       | Python `sys`    | Controlled application termination    |
| Data Storage          | CSV             | Local credential record persistence   |

---

# Key Technical Components

## Administrative Authentication

The `auth` functionality validates administrator access against the application's localized credential tracking data.

The authentication process also includes a defensive check for unexpected credential entries.

This provides the application with a basic mechanism for detecting potentially abnormal credential-file conditions before continuing with administrative operations.

---

## Standardized Credential Generation

The `gen_credentials` functionality collects administrator-provided names and applies standardized formatting rules.

The generation process includes:

* Input validation.
* Character-length restrictions.
* Initial extraction.
* Standardized credential formatting.
* Randomized numeric suffix generation.
* Persistence of generated records.

Generated credentials follow the application's naming convention:

```text id="8f1t0b"
initials_randomsuffix
```

Example:

```text id="j3x2wd"
rlm_123456789
```

The name input is restricted to **3–15 characters** before the identifier is generated.

---

## Credential Decommissioning

The `remove_credentials` functionality provides an interactive method for reviewing existing credential records.

Administrators can:

* Review individual credential entries.
* Decide whether an entry should be removed.
* Retain credentials that are still required.
* Purge decommissioned credentials.
* Exit the workflow without unnecessarily modifying remaining records.

This provides a basic credential lifecycle workflow rather than treating credential creation as a one-time operation.

---

# Input Validation

The application uses validation loops throughout the interactive workflow.

Validation is used to prevent unexpected input from progressing through the program and to provide administrators with another opportunity to correct invalid entries.

Examples include:

* Name validation.
* Character-length enforcement.
* Administrative authentication.
* Menu selection validation.
* Credential-management decisions.
* Controlled program termination.

The goal is to make administrative workflows predictable and reduce accidental data modification.

---

# Data Persistence

Credential records are maintained using local structured data files.

Pandas is used to manipulate and persist credential information in CSV format.

This provides a simple data-management layer while keeping the project lightweight and easy to inspect.

The application expects the required credential and password files to be available within the application's working environment.

> **Security Note:** The included local data-file approach is intended for a scripting/automation project and should not be treated as a production credential-storage architecture. Production systems should use an appropriate secrets-management platform and secure credential storage mechanisms.

---

# Application Workflow

```text
Start Program
     │
     ▼
Administrator Authentication
     │
     ├── Authentication Failed
     │        │
     │        ▼
     │     Exit / Retry
     │
     ▼
Main Administrative Workflow
     │
     ├── Generate Credentials
     │        │
     │        ▼
     │   Validate Input
     │        │
     │        ▼
     │   Generate Identifier
     │        │
     │        ▼
     │   Save Record
     │
     ├── Manage Existing Credentials
     │        │
     │        ▼
     │   Review Records
     │        │
     │        ▼
     │   Remove or Retain
     │        │
     │        ▼
     │   Save Changes
     │
     └── Exit
```

---

# How to Use

## Setup

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

Ensure the required application data files are located securely within the program environment.

The application expects its password and credential tracking files to be available before administrative operations are performed.

---

## Run the Application

```bash
python cred_generator.py
```

The application will prompt the administrator to:

1. Authenticate.
2. Select the desired credential-management operation.
3. Generate or review credentials.
4. Confirm administrative actions.
5. Save changes or exit safely.

---

# Troubleshooting & Defensive Design

The project was designed around the principle that administrative scripts should not assume every user input or file state is valid.

The application therefore uses:

* Validation loops.
* File-existence checks.
* Controlled program exits.
* Administrative authentication.
* Credential-file integrity checks.
* Explicit confirmation during credential removal.
* Structured CSV persistence.

These controls help prevent common scripting problems such as invalid input, unexpected file states, and accidental credential deletion.

---

# Skills Demonstrated

## Python Development

* Python scripting
* Functions and modular logic
* Input handling
* Validation loops
* Exception-aware administrative workflows
* File handling
* Program control

## Automation

* Administrative task automation
* Standardized identifier generation
* Credential lifecycle workflows
* Automated data persistence

## Security

* Administrative authentication
* Credential lifecycle management
* Input validation
* Defensive programming
* File integrity checking
* Secure handling considerations for credential-related data

## Data Management

* Pandas
* CSV data manipulation
* Structured record persistence
* Credential record management

---

# Technologies

* Python
* Pandas
* CSV
* `os`
* `sys`
* `random`

---

# Repository Structure

```text
├── cred_generator.py
├── requirements.txt
├── password_file
├── credential_file
├── README.md
└── LICENSE
```

Credential data files should not contain real production credentials and should be protected from unauthorized access.

---

# Future Enhancements

Potential future improvements include:

* Replace local credential storage with a dedicated secrets-management solution.
* Add password hashing instead of storing authentication secrets directly.
* Implement role-based administrative permissions.
* Add audit logging for credential creation and deletion.
* Add timestamp and administrator information to lifecycle events.
* Add encrypted local storage for development environments.
* Replace CSV persistence with a database-backed storage layer.
* Add automated tests for credential-generation and validation logic.
* Integrate the utility with Active Directory or another identity-management platform.

---

# Project Outcome

The completed project demonstrates how a repetitive administrative task can be converted into a structured automation workflow.

The utility combines:

```text
Authentication
      +
Input Validation
      +
Standardized Generation
      +
Data Persistence
      +
Credential Decommissioning
```

This project provided hands-on experience with **Python automation, administrative scripting, credential lifecycle management, structured data handling, defensive programming, and security-conscious application design**.

---

# License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

---

## Return Page

[Return to Repository Hub](https://github.com/RobNor12/IT-Automation-Engineering/blob/main/README.md)
