# Taskify

Taskify is a web-based task management application that helps users organize and manage their day-to-day tasks in one place.

Users can create an account, log in securely, add tasks, organize them into categories, update their task details and status, and delete tasks when they are no longer needed.

## Features

* User Registration
* User Login and Logout
* Session-based Authentication
* Add New Tasks
* Edit Existing Tasks
* Delete Tasks
* Task Status Management
* Task Categories
* Delete Categories
* User Profile Management
* Edit User Details
* Delete User Account
* User-specific Task Management
* Flash Messages for User Feedback
* Responsive UI using Bootstrap

## Tech Stack

### Backend

* **Python**
* **Flask**

### Database

* **SQLite**
* **SQLAlchemy ORM**

### Frontend

* **HTML**
* **Jinja2 Templates**
* **Bootstrap**
* **CSS**

## Database Models

Taskify uses SQLAlchemy ORM to manage its database.

### User

The `Users` model stores user information such as:

* User ID
* Name
* Email
* Password

Each user can have multiple tasks and categories.

### Task

The `Tasks` model stores:

* Task ID
* Task description
* Task status
* Date added
* User ID
* Category ID

### Category

The `Category` model stores:

* Category ID
* Category name
* User ID

A category can contain multiple tasks.

## Application Flow

1. A new user registers on Taskify.
2. The user's information is stored in the SQLite database.
3. After registration, the user is logged in using a Flask session.
4. The user can access their homepage and view their tasks.
5. New tasks can be added with a category.
6. Existing tasks can be edited, including their status and category.
7. Tasks can be deleted after confirmation.
8. Users can view and manage their categories.
9. Users can edit their profile information or delete their account.
10. The user can log out at any time.

## Task Management

Taskify follows the basic CRUD pattern:

* **Create:** Add a new task
* **Read:** View existing tasks
* **Update:** Edit task details, status and category
* **Delete:** Remove tasks

Tasks are associated with the currently logged-in user, allowing each user to manage their own tasks independently.

## Authentication

Taskify uses Flask sessions to maintain the logged-in user's identity.

After successful registration or login, the application stores the user's ID and name in the session. Protected pages check the session before allowing access.

Users who are not logged in are redirected to the login or home page.

## Database

Taskify uses **SQLite** as its database and **SQLAlchemy** as the ORM.

The database contains relationships between:

```text
User
 ├── Tasks
 └── Categories
       └── Tasks
```

This allows tasks and categories to be associated with individual users.

## Project Structure

A typical project structure is:

```text
Taskify/
│
├── app.py
├── templates/
│   ├── index.html
│   ├── signup.html
│   ├── login.html
│   ├── home.html
│   ├── task.html
│   ├── edit.html
│   ├── category.html
│   ├── user.html
│   ├── base.html
│   ├── edituser.html
│   └── conf.html
│
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Taskify
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it using:

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux / macOS / WSL:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install flask flask-sqlalchemy
```

### 4. Run the Application

```bash
python app.py
```

The application runs on:

```text
http://127.0.0.1:8000
```

## Data Validation

Taskify performs basic validation while registering users and creating or editing tasks.

For example:

* User names must have a meaningful length.
* Email length is validated.
* Passwords must contain between 8 and 15 characters.
* Tasks must contain between 2 and 200 characters.
* Duplicate email registration is prevented.

## User Account Management

Users can manage their account from the profile section.

They can:

* Edit their name
* Update their password
* Delete their account

When an account is deleted, the user's associated tasks and categories are also removed.

## Conclusion

Taskify provides a simple and user-friendly way to manage everyday tasks. The project demonstrates the use of Flask for web application development, SQLAlchemy ORM for database operations, SQLite for data storage, Jinja2 for dynamic HTML rendering, and Bootstrap for frontend styling.
