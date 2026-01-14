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
+Bool is_admin
+register()
+update_profile()
}
class Vehicle {
+String title
+String description
+String engine_type
+String license_plate
+Int doors
+Float length
+Float price
}
class Note {
+String comment
}
class Route {
+String route_number
+String name
+String description
}
BaseModel <|-- User
BaseModel <|-- Vehicle
BaseModel <|-- Note
BaseModel <|-- Route
User "1" --> "*" Vehicle : owns
User "1" --> "*" Note : writes
Vehicle "1" --> "*" Note : receives
Route "1" --> "*" Vehicle : uses

```
**ER diagram**
```mermaid
erDiagram
USER ||--o{ VEHICLE : owns
USER ||--o{ NOTE : writes
VEHICLE ||--o{ NOTE : receives
ROUTE ||--o{ VEHICLE : uses
USER {
string id
string first_name
string last_name
string email
string password
string role
boolean is_admin
}
VEHICLE {
string id
string title
string description
string engine_type
float length
float price
int doors
string owner_id FK
}
ROUTE {
string id
string route_number
string name
string description
}
NOTE {
string id
string comment
string user_id FK
string vehicle_id FK
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
API->>BusinessLogic: Validate & create User
BusinessLogic->>Database: Insert new User
Database-->>BusinessLogic: OK
BusinessLogic-->>API: Success (Status 201)
API-->>User: User created
```
**Create a new vehicle**
```mermaid
sequenceDiagram
participant  User
participant  API
participant  BusinessLogic
participant  Database
User->>API: Create  Vehicle  (title, desc, motorisation, price, etc.)
API->>BusinessLogic: Validate & create  Vehicle
BusinessLogic->>Database: Insert  Vehicle
Database-->>BusinessLogic: OK
BusinessLogic-->>API: Success (Status 201)
API-->>User: Vehicle  created
```
**Add a new note**
```mermaid
sequenceDiagram
participant  User
participant  API
participant  BusinessLogic
participant  Database
User->>API: Submit  Note  (text)
API->>BusinessLogic: Validate & create  Note
BusinessLogic->>Database: Insert  Note
Database-->>BusinessLogic: OK
BusinessLogic-->>API: Success  (Status 201)
API-->>User: Note  added
```
**Fetching a list of vehicles**
```mermaid
sequenceDiagram
participant  User
participant  API
participant  BusinessLogic
participant  Database
User->>API: Request  list  of  vehicles
API->>BusinessLogic: Fetch  vehicles
BusinessLogic->>Database: Query  vehicles
Database-->>BusinessLogic: Return  vehicles
BusinessLogic-->>API: List  of  vehicles
API-->>User: Send  vehicles  JSON
```
