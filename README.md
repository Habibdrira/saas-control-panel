# SaaS Control Panel
## Python Advanced – System Administration Project

---

## 1. Project Overview

This project is a **mini SaaS (Software as a Service) platform** designed and implemented to demonstrate **advanced Python usage in system administration**.

The core idea of the project is to simulate how a real SaaS platform works:
- Users register and automatically receive their own isolated service
- Administrators manage users and infrastructure
- Python is used as an **automation and orchestration tool**, not just a web backend

This project focuses on **system-level automation**, **container lifecycle management**, and **service isolation** using Docker.

---

## 2. SaaS Logic Explained

In a real SaaS platform:
- Each user should be isolated
- Resources must be created and destroyed dynamically
- Administration must be centralized
- Automation is mandatory

This project follows the same logic:
- Each user gets a **dedicated Docker container**
- Containers are created automatically on registration
- Containers are deleted automatically when users are removed
- Administrators control users and infrastructure via web dashboards

This design mimics real-world SaaS platforms used in cloud environments.

---

## 3. Global Architecture

The project is built using a **micro-services architecture**, composed of three independent services.

```
User Browser
     |
     |  Login / Register
     v
+----------------------+
|     Auth-Service     |  (Port 5000)
|  - Authentication    |
|  - Users database    |
|  - Admin users panel |
+----------+-----------+
           |
           | REST API calls
           v
+----------------------+
|    Control-Panel     |  (Port 5001)
|  - Docker management |
|  - Containers admin  |
|  - System actions    |
+----------+-----------+
           |
           v
+----------------------+
|    Docker Engine     |
+----------+-----------+
           |
           v
+----------------------+
|     User-App         |  (Dynamic Port)
|  - One container     |
|  - One user          |
|  - Isolated service  |
+----------------------+
```

Each service has a **single responsibility**, which is a key principle in professional system design.

---

## 4. Services and Their Roles

### 4.1 Auth-Service (Port 5000)

**Purpose:**  
User authentication and user administration.

**Responsibilities:**
- User registration
- User login
- Store users in SQLite database
- Admin authentication
- Admin dashboard to list users
- Delete users
- Trigger container creation and deletion through Control-Panel API

This service represents the **business and security layer** of the SaaS.

---

### 4.2 Control-Panel (Port 5001)

**Purpose:**  
System administration and container orchestration.

**Responsibilities:**
- Communicate directly with Docker Engine
- Create containers dynamically
- Start containers
- Stop containers
- Delete containers
- Inspect container status
- Expose REST APIs for provisioning

This service represents the **system administrator role**, implemented entirely in Python.

---

### 4.3 User-App (Dynamic Port)

**Purpose:**  
Dedicated application environment for each user.

**Responsibilities:**
- Display user information
- Provide a running service
- Logout and return to authentication service

Each user runs inside an **isolated Docker container**, which is a core SaaS principle.

---

## 5. Python Advanced – System Administration Aspect

This project uses Python as a **system administration language**.

Python is used to:
- Control Docker Engine programmatically
- Automate container lifecycle
- Manage system resources
- Replace manual CLI commands
- Synchronize database actions with system actions

This goes far beyond basic Python scripting and demonstrates **real system automation**.

---

## 6. Container Lifecycle Management (Detailed)

Each user container goes through a full lifecycle managed by Python:

1. **Creation**
   - Triggered automatically after user registration
   - Docker SDK creates the container
   - Ports are assigned dynamically

2. **Running**
   - Container serves the user application
   - Environment variables are injected

3. **Monitoring**
   - Admin can view container status
   - Admin can open container service in browser

4. **Stop / Start**
   - Admin can stop or restart containers at any time

5. **Deletion**
   - Triggered when user is deleted
   - Container is removed automatically
   - Resources are freed

All these steps are handled by Python code, not manual commands.

---

## 7. How to Use the Project (Step by Step)

### Step 1: Clone the repository
```bash
git clone https://github.com/Habibdrira/saas-control-panel.git
cd saas-control-panel
```

### Step 2: Build the project
```bash
docker compose build --no-cache
```

### Step 3: Run the platform
```bash
docker compose up
```

---

### Step 4: Access the services

- User login:  
  http://localhost:5000/user/login

- User registration:  
  http://localhost:5000/user/register

- Admin (Auth-Service):  
  http://localhost:5000/admin/login

- Admin (Control-Panel):  
  http://localhost:5001/login

---

### Default Admin Credentials
```
Username: admin
Password: admin123
```

---

## 8. Tools and Technologies Used

| Category | Technology |
|--------|-----------|
| Programming Language | Python 3 |
| Backend Framework | Flask |
| Container Management | Docker SDK for Python |
| Container Platform | Docker |
| Frontend | HTML / CSS / JavaScript |
| Orchestration | Docker Compose |
| Operating System | Linux (Ubuntu / Rocky / FreeBSD) |

---

## 9. System Requirements

- Linux operating system
- Docker installed
- Docker Compose installed
- Python 3.10 or higher

> Docker on Windows is not supported for this project.

---

## 10. Learning Outcomes

By working on this project, the following skills are demonstrated:
- Python advanced programming
- System administration automation
- Docker container orchestration
- SaaS architecture design
- DevOps fundamentals
- Micro-services architecture

---

## 11. Conclusion

This project is a **complete and functional SaaS prototype** focused on **Python Advanced System Administration**.

It demonstrates how Python can be used to:
- Automate infrastructure
- Manage containers dynamically
- Implement real SaaS logic
- Replace manual system administration tasks

The project fully satisfies the requirements of **Python Advanced (Administration Système)**.

---

## Author

Habib Drira  
Python | Docker | System Administration | DevOps
