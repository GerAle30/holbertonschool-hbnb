# HBnB - Phase 2: Bringing Architecture to Life

> *“Design is not just what it looks like and feels like. Design is how it works.” – Steve Jobs*

Welcome to the second phase of the HBnB evolution — the moment where design becomes product. This stage transforms the conceptual foundation into a functional, modular, and scalable RESTful API using Python, Flask, and flask-restx.

---

## ✨ Vision

In this phase, we focus on crafting the **core functionality** of an AirBnB-like application. The goal is to build software that feels seamless and behaves predictably — one endpoint, one purpose, one simple architecture that just works.

We are not building "a backend".
We are building **an experience** for developers, a structure designed to scale, extend, and last.

---

## 🧱 Architecture Overview

The application is organized into three cleanly separated layers:

```
Presentation Layer (API via Flask & flask-restx)
│
├── Business Logic Layer (Entity models and Facade pattern)
│
└── Persistence Layer (In-memory storage, prepared for database in Phase 3)
```

This modular structure ensures a clear **separation of concerns**, simplifies testing, and accelerates future enhancements such as authentication and SQL integration.

---

## 🧠 Features

### ✅ Implemented

* RESTful API for:

  * Users
  * Places
  * Reviews
  * Amenities
* In-memory repository for testing and prototyping
* Facade pattern to coordinate logic across layers
* Data serialization with clean response formatting
* Swagger documentation via `flask-restx`

### ❌ Not Yet Implemented (Planned in Part 3)

* JWT Authentication
* SQLAlchemy Persistence
* Role-Based Access Control

---

## 🔍 Tech Stack

* **Language:** Python 3.x
* **Framework:** Flask
* **API Layer:** flask-restx
* **Design Pattern:** Facade
* **Storage:** In-memory repository (planned migration to SQLAlchemy)

---

## 📁 Project Structure

```
part2/
├── app.py                  # Application entry point
├── config.py               # Configuration settings
├── requirements.txt
│
├── presentation/
│   ├── api.py              # API blueprint and namespace setup
│   └── resources/          # REST resources (user, place, etc.)
│
├── business/
│   ├── facade.py           # Facade pattern logic controller
│   └── entities/           # Core business models
│
├── persistence/
│   └── memory_repository.py # In-memory repository (mocked database)
│
└── tests/                  # Unit and integration tests
```

---

## 🚀 Getting Started

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

### View API Docs

Go to [http://localhost:5000/api/v1/](http://localhost:5000/api/v1/)
You’ll see a **beautiful, auto-generated Swagger UI**.

---

## 🧪 Example Usage (with `curl`)

### Create a User

```bash
curl -X POST http://localhost:5000/api/v1/users/ \
     -H "Content-Type: application/json" \
     -d '{"first_name": "Steve", "last_name": "Jobs", "email": "steve@apple.com"}'
```

### List All Users

```bash
curl http://localhost:5000/api/v1/users/
```

---

## 🧠 Design Philosophy

This project follows a Jobsian mindset:

* **Simplicity is power:** Every file has a reason. Every line has a purpose.
* **Design for the future:** The in-memory repository anticipates a smooth transition to SQLAlchemy.
* **Separation is clarity:** API, logic, and persistence are strictly decoupled.

---

## 🛠️ Contributors

Project developed as part of the Holberton School curriculum by \[Alejandro Garcia Sanchez].



