# Portfolio Technical Documentation


## User Stories

**Admin**
-   “As an admin, I want to supervise the fleet, so that I can manage budgets and contracts effectively.”
-   The admin must have access to all strategic data and reports. No restrictions apply.

**Manager**
-   “As a manager, I want to define, manage and schedule planning, so that I can manage vehicle availability easily.”
-   The manager must have access to the full fleet and its availability, and to a schedule they can modify. They will not have access to strategic financial data.

**Technician**
-   “As a technician, I want to track interventions and repairs, so that I can ensure vehicles remain operational.”
-   The technician will have access to details about each vehicle, including reports, issues, notes, and alerts. They will not have access to budgets or contracts.

**Driver**
-   “As a driver, I want to drive a safe vehicle, so that I can transport passengers without incidents or technical issues.”
-   The driver will have access to routes, schedules, and status alerts, and can submit complaints or requests. They will not have access to fleet management or strategic data.

## Design System Architecture
```mermaid
classDiagram
class PresentationLayer {
<<Facade>>
+API Services
+Controllers
}
class BusinessLogicLayer {
+User
+Vehicle
+Route
+Note
+BaseModel
}
class PersistenceLayer {
+Repositories
+Database
}
PresentationLayer --> BusinessLogicLayer : Calls
BusinessLogicLayer --> PersistenceLayer : Data Access
```

## Mock-up
https://www.figma.com/make/PGpOrxlnHuEgmc2D14URK0/Application-de-gestion-de-flotte?t=OuzGVjcRWPqfKHCu-1

## Components, classes and database
**Classes diagram**
```mermaid
classDiagram
class BaseModel {
    +UUID id
    +Date created_at
    +Date updated_at
    +save()
    +delete()
    +to_dict()
    +update(attrs)
    +list(filters)
}

class User {
    +String first_name
    +String last_name
    +String email
    +String password
    +String role
    +register()
    +update_profile()
}

class Vehicle {
    +String number
    +Int capacity
    +String status
    +String engine_type
    +String euro_standard
    +Int doors
    +Float length
    +Float price
}

class Report {
    +String comment
}

class Route {
    +String route_number
    +String name
    +String description
}

class Assignment {
    +Date date
    +String time
}

class Maintenance {
    +String type
    +Date date
    +String time
}

BaseModel <|-- User
BaseModel <|-- Vehicle
BaseModel <|-- Report
BaseModel <|-- Route
BaseModel <|-- Assignment
BaseModel <|-- Maintenance

User "1" --> "*" Report : writes
Vehicle "1" --> "*" Report : receives

Vehicle "1" --> "*" Assignment : assigned_to
Route "1" --> "*" Assignment : includes

Vehicle "1" --> "*" Maintenance : has

```
**ER diagram**
```mermaid
erDiagram
USER ||--o{ REPORT : writes
VEHICLE ||--o{ REPORT : receives
VEHICLE ||--o{ ASSIGNMENT : assigned_to
ROUTE ||--o{ ASSIGNMENT : includes
VEHICLE ||--o{ MAINTENANCE : has

USER {
    string id
    string first_name
    string last_name
    string email
    string password
    string role
}

VEHICLE {
    string id
    string number
    int capacity
    string status
    float length
    float price
    int doors
    int seats
    string engine_type
    string euro_standard
}

ROUTE {
    string id
    string route_number
    string name
    string description
}

REPORT {
    string id
    string comment
    string user_id FK
    string vehicle_id FK
}

ASSIGNMENT {
    string id
    string vehicle_id FK
    string route_id FK
    date date
    string time
}

MAINTENANCE {
    string id
    string vehicle_id FK
    string type
    date date
    string time
}

```
## High-Level Sequence Diagrams
**User Registration**

Note: A user can select between one of these three roles during registration: manager, technician, or driver. The admin role is reserved for the first created account.
```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: Register (email, password, role, etc.)
API->>BusinessLogic: Validate & create user
BusinessLogic->>Database: INSERT User
Database-->>BusinessLogic: OK
BusinessLogic-->>API: Success (201)
API-->>User: User created

```
**Add a new bus**
```mermaid
sequenceDiagram
participant Admin
participant API
participant BusinessLogic
participant Database

Admin->>API: Create Bus (number, capacity, status, etc.)
API->>BusinessLogic: Validate & create bus
BusinessLogic->>Database: INSERT Bus
Database-->>BusinessLogic: OK
BusinessLogic-->>API: Success (201) + Bus ID
API-->>Admin: Bus created

```
**Fetch a List of buses**
```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: Request list of Bus
API->>BusinessLogic: Fetch Bus
BusinessLogic->>Database: Query Bus
Database-->>BusinessLogic: Return Bus
BusinessLogic-->>API: List of Bus
API-->>User: Send Bus JSON

```
**Submit a new report**
```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: Submit report (busId, text)
API->>BusinessLogic: Check bus exists, validate & create report
BusinessLogic->>Database: INSERT Report
Database-->>BusinessLogic: OK
BusinessLogic-->>API: Success (201)
API-->>User: Report added

```
**Assigning a bus to a route**
```mermaid
sequenceDiagram
participant Manager
participant API
participant BusinessLogic
participant Database

Manager->>API: Assign bus to route (busId, routeId, date, time)
API->>BusinessLogic: Check bus availability
BusinessLogic->>Database: SELECT status, assignments
Database-->>BusinessLogic: Bus data
BusinessLogic->>BusinessLogic: Verify availability
BusinessLogic->>Database: INSERT Assignment (busId, routeId, date, time)
Database-->>BusinessLogic: OK
BusinessLogic-->>API: Success (201)
API-->>Manager: Bus assigned

```
**Schedule maintenance**
```mermaid
sequenceDiagram
participant Technician
participant API
participant BusinessLogic
participant Database

Technician->>API: Schedule maintenance (busId, type, date, time)
API->>BusinessLogic: Validate request
BusinessLogic->>Database: SELECT status
Database-->>BusinessLogic: Bus data
BusinessLogic->>BusinessLogic: Check availability
BusinessLogic->>Database: INSERT Maintenance
Database-->>BusinessLogic: OK
BusinessLogic-->>API: Success (201)
API-->>Technician: Maintenance scheduled

```
**Retire a bus**
```mermaid
sequenceDiagram
participant Admin
participant API
participant BusinessLogic
participant Database

Admin->>API: Retire bus (busId, reason)
API->>BusinessLogic: Check bus exists
BusinessLogic->>Database: SELECT status
Database-->>BusinessLogic: Bus data
BusinessLogic->>BusinessLogic: Verify bus is inactive
BusinessLogic->>Database: UPDATE Bus SET status = "Retired"
Database-->>BusinessLogic: OK
BusinessLogic-->>API: Success (200)
API-->>Admin: Bus retired

```

## Selected technologies
**Back-End**
- Python : Simple language, it can hold each cases of this project
- Flask : This framework is easy to implement with Python for it's module

**Database**
- PostgreSQL : Very efficient, scalable, secured and open-source

**Front-End**
- JavaScript : Very polyvalent, from refining the front-end, to fetch or serialize datas to back-end
- HTML, CSS : Pages and styles will be manually builded
- Jinja : It can build a single page with multiples pages (takes a pre-builded header, footer and aside menu with a main page)