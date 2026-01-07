# SaaS Control Panel
## Python Advanced – System Administration Project

---

## 1. Project Overview

This project is a **mini SaaS (Software as a Service) platform** developed for the course **Python Advanced (System Administration)**.

The objective is to demonstrate how **Python can be used as a system administration and automation tool**, capable of managing containers, services, and users dynamically using Docker.

The project simulates a real SaaS environment where:
- Users register and automatically receive an isolated service
- Administrators manage users and infrastructure
- All system operations are automated using Python

---

## 2. SaaS Logic

In a real SaaS platform:
- Each user must be isolated
- Resources are created and destroyed dynamically
- Automation replaces manual system tasks
- Administration is centralized

This project follows the same logic:
- Each user gets a **dedicated Docker container**
- Containers are created automatically at registration
- Containers are deleted automatically when users are removed
- Administrators manage users and containers via web interfaces

This makes the project close to real-world SaaS and cloud platforms.

---

## 3. Global Architecture

The platform is built using a **micro-services architecture** composed of three independent services.

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
|  - Container admin   |
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

Each service has a **single and clear responsibility**, following professional system design principles.

---

## 4. Services Description

### 4.1 Auth-Service (Port 5000)

**Role:** Authentication and user administration.

**Responsibilities:**
- User registration
- User login
- Store users in SQLite database
- Admin authentication
- Admin dashboard (list users, delete users)
- Trigger container creation and deletion via Control-Panel API

This service represents the **security and business logic layer** of the SaaS.

---

### 4.2 Control-Panel (Port 5001)

**Role:** System administration and container orchestration.

**Responsibilities:**
- Communicate directly with Docker Engine
- Create user containers dynamically
- Start containers
- Stop containers
- Delete containers
- Inspect container status
- Expose REST APIs for provisioning

This service demonstrates **Python used as a system administrator**.

---

### 4.3 User-App (Dynamic Port)

**Role:** Dedicated application environment for each user.

**Responsibilities:**
- Display user dashboard
- Show username and email
- Provide logout functionality
- Run inside an isolated Docker container

Each user runs in a **separate container**, ensuring isolation and security.

---

## 5. Python Advanced – System Administration

This project uses Python as a **system administration language**.

Python is responsible for:
- Docker container lifecycle management
- Infrastructure automation
- System resource control
- Service orchestration
- Replacing manual CLI-based administration

This demonstrates **advanced Python usage beyond basic scripting**.

---

## 6. Container Lifecycle Management (Detailed)

Each user container follows a complete lifecycle controlled by Python:

1. **Creation**
   - Triggered automatically after user registration
   - Docker SDK creates the container
   - Ports are assigned dynamically

2. **Execution**
   - Container runs the user application
   - Environment variables are injected

3. **Monitoring**
   - Admin can view container status
   - Admin can open the container in browser

4. **Stop / Start**
   - Containers can be stopped or restarted by admin

5. **Deletion**
   - Triggered when a user is deleted
   - Container is removed automatically
   - System resources are released

All lifecycle operations are handled programmatically in Python.

---

## 7. How to Use the Project (Step by Step)

### Step 1: Clone the repository
```bash
git clone https://github.com/Habibdrira/saas-control-panel.git
cd saas-control-panel
```

### Step 2: Build images automatically (recommended)
```bash
docker compose build --no-cache
```

### Step 3: Run the platform
```bash
docker compose up
```

---

### Manual build of user-app (optional)
```bash
cd user-app
docker build -t user-app .
```

This step is useful for development, debugging, or demonstration purposes.

---

### Access URLs

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

## 8. Docker Compose – Final Configuration

The project uses Docker Compose to build and run services.

```yaml
version: "3.9"

services:
  auth-service:
    build: ./auth-service
    ports:
      - "5000:5000"
    depends_on:
      - control-panel
      - user-app

  control-panel:
    build: ./control-panel
    ports:
      - "5001:5001"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - user-app

  user-app:
    build: ./user-app
    image: user-app
```

This configuration ensures:
- Automatic image building
- Dynamic container creation
- Proper service orchestration

---

## 9. Tools and Technologies Used

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

## 10. System Requirements

- Linux operating system
- Docker installed
- Docker Compose installed
- Python 3.10 or higher

> Docker on Windows is not supported.

---

## 11. Learning Outcomes

This project demonstrates:
- Python advanced programming
- System administration automation
- Docker container orchestration
- SaaS architecture design
- DevOps fundamentals
- Micro-services architecture

---

## 12. Conclusion

This project is a **complete and functional SaaS prototype** focused on **Python Advanced System Administration**.

It demonstrates how Python can:
- Automate infrastructure tasks
- Manage containers dynamically
- Control system resources
- Implement real SaaS logic

The project fully satisfies the requirements of **Python Advanced (Administration Système)**.

---

## Author

Habib Drira  
Python | Docker | System Administration | DevOps
