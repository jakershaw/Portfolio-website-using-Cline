# Portfolio Website - Architecture Diagram

## Project Overview
A Flask-based portfolio website with admin dashboard, project management, and user authentication.

---

## System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Browser[Web Browser]
    end

    subgraph "Application Layer"
        Flask[Flask Application<br/>run.py]
        Routes[Routes<br/>routes.py]
        Forms[Forms<br/>forms.py]
        Auth[Authentication<br/>Flask-Login]
    end

    subgraph "Data Layer"
        Models[Models<br/>models.py]
        DB[(SQLite Database<br/>portfolio.db)]
    end

    subgraph "Presentation Layer"
        Templates[Jinja2 Templates<br/>HTML]
        Static[Static Assets<br/>CSS, JS, Images]
    end

    subgraph "Configuration"
        Config[config.py]
        Env[.env]
    end

    Browser -->|HTTP Request| Flask
    Flask --> Config
    Config --> Env
    Flask --> Routes
    Routes --> Auth
    Routes --> Forms
    Routes --> Models
    Models --> DB
    Routes --> Templates
    Templates --> Static
    Templates -->|HTTP Response| Browser

    style Flask fill:#4CAF50
    style DB fill:#2196F3
    style Browser fill:#FF9800
    style Templates fill:#9C27B0
```

---

## Detailed Project Structure

```mermaid
graph LR
    subgraph "Root Directory"
        A[run.py<br/>Entry Point]
        B[config.py<br/>Configuration]
        C[.env<br/>Secrets]
        D[requirements.txt<br/>Dependencies]
        E[portfolio.db<br/>Database]
        F[migrate_add_fields.py<br/>Migration Script]
    end

    subgraph "app/ Directory"
        G[__init__.py<br/>App Factory]
        H[models.py<br/>Database Models]
        I[forms.py<br/>Form Classes]
        J[routes.py<br/>URL Routes]
    end

    subgraph "app/templates/"
        K[base.html<br/>Base Template]
        L[index.html<br/>Homepage]
        M[about.html<br/>About Page]
        N[project.html<br/>Project Detail]
        O[login.html<br/>Login Page]
        P[admin/<br/>Admin Templates]
    end

    subgraph "app/static/"
        Q[css/style.css<br/>Styles]
        R[js/main.js<br/>Scripts]
        S[uploads/<br/>Media Files]
    end

    A --> G
    G --> H
    G --> I
    G --> J
    J --> K
    K --> L
    K --> M
    K --> N
    K --> O
    K --> P
    J --> Q
    J --> R
    J --> S

    style A fill:#4CAF50
    style G fill:#2196F3
    style K fill:#9C27B0
```

---

## Database Schema

```mermaid
erDiagram
    USER ||--o{ PROJECT : creates
    
    USER {
        int id PK
        string username UK
        string password_hash
        string email
        string display_name
        string bio_header
        text bio
        string profile_photo_path
        string linkedin_url
        string github_url
        datetime created_at
        datetime updated_at
    }
    
    PROJECT {
        int id PK
        string title
        string description
        text content
        string github_url
        string image_path
        boolean published
        datetime created_at
        datetime updated_at
    }
```

---

## Request Flow - Public Routes

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Flask
    participant Routes
    participant Models
    participant Database
    participant Templates

    User->>Browser: Visit homepage
    Browser->>Flask: GET /
    Flask->>Routes: index()
    Routes->>Models: Query User & Projects
    Models->>Database: SELECT * FROM user, projects
    Database-->>Models: Return data
    Models-->>Routes: User & Project objects
    Routes->>Templates: Render index.html
    Templates-->>Routes: HTML content
    Routes-->>Flask: Response
    Flask-->>Browser: HTTP 200 + HTML
    Browser-->>User: Display homepage
```

---

## Request Flow - Admin Routes

```mermaid
sequenceDiagram
    participant Admin
    participant Browser
    participant Flask
    participant Auth
    participant Routes
    participant Forms
    participant Models
    participant Database

    Admin->>Browser: Submit login form
    Browser->>Flask: POST /login
    Flask->>Routes: login()
    Routes->>Forms: Validate LoginForm
    Forms-->>Routes: Valid
    Routes->>Models: Query User
    Models->>Database: SELECT * FROM user
    Database-->>Models: User data
    Models-->>Routes: User object
    Routes->>Auth: Check password
    Auth-->>Routes: Password correct
    Routes->>Auth: login_user()
    Auth-->>Routes: Session created
    Routes-->>Flask: Redirect to /admin
    Flask-->>Browser: HTTP 302
    Browser->>Flask: GET /admin
    Flask->>Routes: admin_dashboard()
    Routes->>Auth: Check @login_required
    Auth-->>Routes: Authenticated
    Routes->>Models: Query all projects
    Models->>Database: SELECT * FROM project
    Database-->>Models: Project data
    Models-->>Routes: Project list
    Routes-->>Browser: Render admin dashboard
    Browser-->>Admin: Display admin panel
```

---

## Component Interactions

```mermaid
graph TB
    subgraph "Frontend Components"
        Header[Header<br/>Profile Photo & Nav]
        Content[Main Content<br/>Dynamic Pages]
        Footer[Footer<br/>Social Links]
    end

    subgraph "Backend Components"
        RouteHandler[Route Handler<br/>Flask Blueprint]
        AuthManager[Auth Manager<br/>Flask-Login]
        FormValidator[Form Validator<br/>WTForms]
        FileUploader[File Uploader<br/>Werkzeug]
    end

    subgraph "Data Models"
        UserModel[User Model<br/>Profile & Auth]
        ProjectModel[Project Model<br/>Portfolio Items]
    end

    Header --> RouteHandler
    Content --> RouteHandler
    Footer --> RouteHandler
    
    RouteHandler --> AuthManager
    RouteHandler --> FormValidator
    RouteHandler --> FileUploader
    
    AuthManager --> UserModel
    FormValidator --> UserModel
    FormValidator --> ProjectModel
    FileUploader --> UserModel
    FileUploader --> ProjectModel

    style Header fill:#FF9800
    style RouteHandler fill:#4CAF50
    style UserModel fill:#2196F3
```

---

## File Upload Flow

```mermaid
graph TD
    A[User Selects File] --> B[Form Submission]
    B --> C{Validate File Type}
    C -->|Invalid| D[Show Error]
    C -->|Valid| E[Generate Unique Filename]
    E --> F[Save to uploads/ folder]
    F --> G[Store path in Database]
    G --> H[Update Model]
    H --> I[Redirect to Success Page]
    D --> J[Return to Form]

    style A fill:#FF9800
    style E fill:#4CAF50
    style G fill:#2196F3
```

---

## Authentication Flow

```mermaid
stateDiagram-v2
    [*] --> Anonymous
    Anonymous --> LoginPage: Click Login
    LoginPage --> Authenticating: Submit Credentials
    Authenticating --> Authenticated: Valid Credentials
    Authenticating --> LoginPage: Invalid Credentials
    Authenticated --> AdminDashboard: Access Admin
    Authenticated --> EditProfile: Edit Profile
    Authenticated --> ManageProjects: Manage Projects
    AdminDashboard --> [*]: Logout
    EditProfile --> [*]: Logout
    ManageProjects --> [*]: Logout
    Authenticated --> Anonymous: Logout
```

---

## Technology Stack

```mermaid
graph LR
    subgraph "Backend"
        A[Python 3.x]
        B[Flask Framework]
        C[SQLAlchemy ORM]
        D[Flask-Login]
        E[Flask-WTF]
    end

    subgraph "Frontend"
        F[HTML5]
        G[Bootstrap 5]
        H[Font Awesome]
        I[JavaScript]
    end

    subgraph "Database"
        J[SQLite]
    end

    subgraph "Libraries"
        K[Jinja2 Templates]
        L[Werkzeug Security]
        M[Markdown2]
    end

    A --> B
    B --> C
    B --> D
    B --> E
    C --> J
    B --> K
    B --> L
    B --> M
    F --> G
    F --> H
    F --> I

    style B fill:#4CAF50
    style J fill:#2196F3
    style G fill:#9C27B0
```

---

## Key Features Map

```mermaid
mindmap
    root((Portfolio Website))
        Public Features
            Homepage
                Bio Header
                Bio Text
                Project Grid
            About Page
                Detailed Bio
                Social Links
            Project Pages
                Markdown Content
                Images
                GitHub Links
        Admin Features
            Authentication
                Login/Logout
                Session Management
                Password Hashing
            Profile Management
                Photo Upload
                Bio Editing
                Social Links
            Project Management
                Create Projects
                Edit Projects
                Delete Projects
                Publish/Unpublish
        Technical Features
            Responsive Design
            File Uploads
            Database Migrations
            Form Validation
            Error Handling
```

---

## Deployment Architecture

```mermaid
graph TB
    subgraph "Development"
        Dev[Local Development<br/>Flask Debug Server<br/>SQLite Database]
    end

    subgraph "Production Ready"
        Server[Production Server<br/>Gunicorn/uWSGI]
        DB[Database<br/>SQLite/PostgreSQL]
        Static[Static Files<br/>CDN/Nginx]
    end

    subgraph "Version Control"
        Git[Git Repository]
    end

    Dev -->|Push| Git
    Git -->|Deploy| Server
    Server --> DB
    Server --> Static

    style Dev fill:#4CAF50
    style Server fill:#2196F3
    style Git fill:#FF9800
```

---

## Route Structure

```mermaid
graph TD
    Root[/ Homepage] --> Public{Public Routes}
    Root --> Admin{Admin Routes}
    Root --> Auth{Auth Routes}

    Public --> Index[/ - Homepage]
    Public --> About[/about - About Page]
    Public --> Project[/project/id - Project Detail]

    Auth --> Login[/login - Login Page]
    Auth --> Logout[/logout - Logout]

    Admin --> Dashboard[/admin - Dashboard]
    Admin --> EditProfile[/admin/profile - Edit Profile]
    Admin --> NewProject[/admin/project/new - New Project]
    Admin --> EditProject[/admin/project/id/edit - Edit Project]
    Admin --> DeleteProject[/admin/project/id/delete - Delete Project]

    style Public fill:#4CAF50
    style Admin fill:#FF9800
    style Auth fill:#2196F3
```

---

## Security Features

```mermaid
graph LR
    subgraph "Security Layers"
        A[Password Hashing<br/>Werkzeug]
        B[Session Management<br/>Flask-Login]
        C[CSRF Protection<br/>Flask-WTF]
        D[Form Validation<br/>WTForms]
        E[File Upload Validation<br/>Custom Logic]
        F[Login Required<br/>Decorators]
    end

    User[User] --> A
    User --> B
    User --> C
    Forms[Forms] --> C
    Forms --> D
    Upload[File Upload] --> E
    Admin[Admin Routes] --> F
    F --> B

    style A fill:#F44336
    style B fill:#FF9800
    style C fill:#4CAF50
```

---

## View this diagram:
- On GitHub: This markdown file will render automatically
- In VSCode: Install "Markdown Preview Mermaid Support" extension
- Online: Copy to https://mermaid.live for interactive viewing
- Export: Use mermaid-cli to generate PNG/SVG files

## Generate Images:
```bash
# Install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Generate PNG
mmdc -i ARCHITECTURE_DIAGRAM.md -o architecture.png

# Generate SVG
mmdc -i ARCHITECTURE_DIAGRAM.md -o architecture.svg
