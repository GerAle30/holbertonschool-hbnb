# HBnB Evolution - Part 1: Technical Documentation

## 📘 Introduction

This document provides the foundational technical documentation for the HBnB Evolution application, a simplified version of an AirBnB-like platform. It outlines the architecture, entity relationships, and interaction flows across the core components of the system. This documentation serves as a blueprint to guide the implementation phase, ensuring clarity, consistency, and alignment with business requirements.

---

## 📐 High-Level Architecture

### 🗂 Package Diagram

The HBnB application is structured using a **three-layer architecture**:

1. **Presentation Layer**: Contains the API services that handle HTTP requests and responses.
2. **Business Logic Layer**: Contains core models and domain logic for handling users, places, reviews, and amenities.
3. **Persistence Layer**: Manages data access through DAO objects and communicates directly with the database.

**Design Pattern Used:** The **Facade Pattern** is applied to separate business logic from the presentation layer, promoting loose coupling and maintainability.

*Refer to the Mermaid.js diagram and sequence explanation provided in the technical assets.*

---

## 🧠 Business Logic Layer - Class Diagram

### Key Entities:

* **BaseModel**: Parent class with `id`, `created_at`, `updated_at`, `save()`, and `to_dict()`.
* **User**: Attributes include `email`, `password`, `first_name`, `last_name`, and `is_admin`.
* **Place**: Contains `title`, `description`, `price`, `latitude`, `longitude`, and foreign key `user_id`.
* **Review**: Includes `text`, `rating`, `place_id`, `user_id`.
* **Amenity**: Defined by `name` and `description`.

**Relationships**:

* `User` → `Place` (1\:N)
* `User` → `Review` (1\:N)
* `Place` → `Amenity` (N\:M)
* `Place` → `Review` (1\:N)

**Design Features**:

* Inheritance from `BaseModel`
* Composition and associations properly depicted using UML notation

*Diagram provided in classDiagram Mermaid.js format.*

---

## 🔁 Sequence Diagrams for API Calls

### 1. 🧾 User Registration

**Flow:**

* User submits `POST /register`
* APIService validates and calls `Facade.handle_user_creation()`
* Facade creates user and calls `UserDAO.save()`
* DBConnection executes `INSERT INTO users`
* Response: `201 Created + user_id`

### 2. 🏠 Place Creation

**Flow:**

* User submits `POST /places`
* APIService sends data to `Facade.fetch_place_details()`
* Facade constructs and sends to `PlaceDAO.save()`
* DBConnection executes `INSERT INTO places`
* Response: `201 Created + place_id`

### 3. ⭐ Review Submission

**Flow:**

* User submits `POST /reviews`
* APIService calls `Facade.get_reviews()`
* Facade sends review to `ReviewDAO.save()`
* DBConnection executes `INSERT INTO reviews`
* Response: `201 Created + review_id`

### 4. 🔍 Fetch List of Places

**Flow:**

* User submits `GET /places?location=NYC`
* APIService forwards to `Facade.fetch_place_details()`
* Facade queries `PlaceDAO.get_places_by_filter()`
* DBConnection runs `SELECT * WHERE location=NYC`
* Response: `200 OK + List<Place>`

*Each of these flows is documented with Mermaid.js sequence diagrams in the project directory.*

---

## 📄 Summary of Deliverables

### ✅ Diagrams Included:

* High-Level Package Diagram
* Detailed Class Diagram
* 4 Sequence Diagrams:

  * User Registration
  * Place Creation
  * Review Submission
  * Place Search

### ✅ Explanatory Notes:

* Each diagram includes its purpose, key components, and interaction logic.
* All elements follow UML standards and align with the business requirements.

---

## 💡 Final Notes

* **UML Standards** were used across all diagrams.
* **Mermaid.js** was the tool of choice to enable live editing and version-controlled diagrams.
* The **facade pattern** was critical to separate concerns and improve maintainability.

---

## 🔗 Resources

* GitHub Repository: [holbertonschool-hbnb](https://github.com/GerAle30/holbertonschool-hbnb)
* Documentation Directory: `part1`

---

## 📌 Project Recap

| Task | Description                | Score |
| ---- | -------------------------- | ----- |
| 0    | High-Level Package Diagram | 90%   |
| 1    | Class Diagram              | 88%   |
| 2    | Sequence Diagrams (4)      | 86%   |
| 3    | Documentation Compilation  | 88%   |

---

**Status:** ✅ Documentation Complete — ready for implementation!
