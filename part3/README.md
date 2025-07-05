# 🏡 HBnB Evolution — Technical Documentation

Welcome to the technical blueprint of **HBnB Evolution**, a simplified AirBnB-like web application. This document outlines the **architecture**, **business logic**, and **interaction flows** between core system components.

---

## 📌 Project Overview

**HBnB Evolution** allows users to:
- Register and manage user profiles
- List and manage places for rent
- Submit and view reviews on places
- Associate places with amenities

This documentation serves as a foundation for future development phases by clearly defining system architecture and behavior.

---

## 🧱 1. High-Level Architecture

### 🎯 Objective

Visualize the system's **three-layer architecture**:
1. **Presentation Layer** – User-facing services and APIs
2. **Business Logic Layer** – Core application models and logic
3. **Persistence Layer** – Handles communication with the database

### 🧩 Package Diagram

```mermaid
classDiagram
    class PresentationLayer {
        <<interface>>
        + APIService
    }

    class BusinessLogicLayer {
        + Facade
        + User, Place, Review, Amenity
    }

    class PersistenceLayer {
        + UserDAO, PlaceDAO, ReviewDAO, AmenityDAO
        + DBConnection
    }

    PresentationLayer --> BusinessLogicLayer : uses (via Facade)
    BusinessLogicLayer --> PersistenceLayer : accesses data

# 🏡 HBnB Evolution — Technical Documentation

Welcome to the technical blueprint of **HBnB Evolution**, a simplified AirBnB-like web application. This document outlines the **architecture**, **business logic**, and **interaction flows** between core system components.

---

## 📌 Project Overview

**HBnB Evolution** allows users to:
- Register and manage user profiles
- List and manage places for rent
- Submit and view reviews on places
- Associate places with amenities

This documentation serves as a foundation for future development phases by clearly defining system architecture and behavior.

---

## 🧱 1. High-Level Architecture

### 🎯 Objective

Visualize the system's **three-layer architecture**:
1. **Presentation Layer** – User-facing services and APIs
2. **Business Logic Layer** – Core application models and logic
3. **Persistence Layer** – Handles communication with the database

🧠 2. Business Logic Class Diagram

🎯 Objective
Define entities with attributes, behaviors, and relationships.

📘 Class Diagram

classDiagram
    class BaseModel {
        +UUID id
        +datetime created_at
        +datetime updated_at
        +save()
        +to_dict()
    }

    class User {
        +string first_name
        +string last_name
        +string email
        +string password
        +bool is_admin
    }

    class Place {
        +string title
        +string description
        +float price
        +float latitude
        +float longitude
    }

    class Review {
        +int rating
        +string comment
    }

    class Amenity {
        +string name
        +string description
    }

    User --|> BaseModel
    Place --|> BaseModel
    Review --|> BaseModel
    Amenity --|> BaseModel

    User --> "0..*" Place : owns >
    Place --> "0..*" Review : receives >
    User --> "0..*" Review : writes >
    Place --> "0..*" Amenity : includes >

🔄 3. API Sequence Diagrams

🎯 Objective
Depict how system layers interact to handle API calls.

🧑‍💻 User Registration

sequenceDiagram
    participant User
    participant APIService
    participant Facade
    participant UserDAO
    participant DBConnection

    User->>APIService: POST /register
    APIService->>Facade: handle_user_creation()
    Facade->>UserDAO: save_user()
    UserDAO->>DBConnection: INSERT INTO users
    DBConnection-->>UserDAO: success
    UserDAO-->>Facade: user_id
    Facade-->>APIService: response
    APIService-->>User: 201 Created + user_id

🏠 Place Creation

sequenceDiagram
    participant User
    participant APIService
    participant Facade
    participant PlaceDAO
    participant DBConnection

    User->>APIService: POST /places
    APIService->>Facade: create_place()
    Facade->>PlaceDAO: save_place()
    PlaceDAO->>DBConnection: INSERT INTO places
    DBConnection-->>PlaceDAO: success
    PlaceDAO-->>Facade: place_id
    Facade-->>APIService: response
    APIService-->>User: 201 Created + place_id

⭐ Review Submission

sequenceDiagram
    participant User
    participant APIService
    participant Facade
    participant ReviewDAO
    participant DBConnection

    User->>APIService: POST /reviews
    APIService->>Facade: create_review()
    Facade->>ReviewDAO: save_review()
    ReviewDAO->>DBConnection: INSERT INTO reviews
    DBConnection-->>ReviewDAO: success
    ReviewDAO-->>Facade: review_id
    Facade-->>APIService: response
    APIService-->>User: 201 Created + review_id

🗺️ Fetch Places (By Location)

sequenceDiagram
    participant User
    participant APIService
    participant Facade
    participant PlaceDAO
    participant DBConnection

    User->>APIService: GET /places?location=NYC
    APIService->>Facade: fetch_places(location)
    Facade->>PlaceDAO: get_places_by_location()
    PlaceDAO->>DBConnection: SELECT * FROM places WHERE location=NYC
    DBConnection-->>PlaceDAO: results
    PlaceDAO-->>Facade: place_list
    Facade-->>APIService: response
    APIService-->>User: 200 OK + place_list

📂 Repo Structure

holbertonschool-hbnb/
└── part1/
    ├── diagrams/
    │   ├── package_diagram.mmd
    │   ├── class_diagram.mmd
    │   ├── sequence_user_register.mmd
    │   ├── sequence_place_creation.mmd
    │   ├── sequence_review_submission.mmd
    │   └── sequence_place_fetch.mmd
    └── README.md ← (You are here!)

