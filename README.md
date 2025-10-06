# 🚀 CLI Blogging Platform - A DBMS Project with Python

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Database](https://img.shields.io/badge/database-MySQL-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Welcome to the CLI Blogging Platform! This is a complete command-line content management system built with Python and backed by a MySQL database. It's designed to be a practical, hands-on demonstration of core database management principles, from relational schema design to complex query execution.

---

## 📋 Table of Contents

1.  [Project Overview](#-project-overview)
2.  [Live Demo](#-live-demo)
3.  [Key Features](#-key-features)
4.  [Architecture & Schema](#-architecture--schema)
5.  [Technology Stack](#-technology-stack)
6.  [Setup and Installation](#-setup-and-installation)
7.  [Future Improvements](#-future-improvements)
8.  [License](#-license)

---

## ✨ Project Overview

The primary goal of this project is to model a real-world application (a blog) into a robust relational database and build a secure, interactive command-line interface to manage it. By avoiding a complex web frontend, this project puts the focus squarely on backend logic and database interaction, making it an ideal project for any DBMS or software engineering course.

---

## 💻 Live Demo

Here’s a sneak peek of what it looks like to use the application in the terminal:

```sh
$ project_code.py

===== Welcome to the Blog CLI =====
1. Login
2. Register
3. Exit
> 2

--- Register a New User ---
Enter username: alice
Enter password: ●●●●●
✅ User registered successfully!

===== Welcome to the Blog CLI =====
1. Login
2. Register
3. Exit
> 1

--- User Login ---
Enter username: alice
Enter password: ●●●●●

✅ Welcome, alice!

===== Main Menu =====
Logged in as: alice
1. Create a Post
2. List All Posts
...
> 1

--- Create a New Post ---
Enter post title: My First Adventure
Enter post content: Today, I started building this awesome CLI project!

✅ Post created successfully!

===== Main Menu =====
...
> 2

--- All Blog Posts ---
[1] My First Adventure (by alice)

```
---
## 🌟 Key Features

- **Secure User Authentication**: Full registration and login flow with sha256 password hashing.
- **Complete Post Management (CRUD)**: Create, read, edit, and delete blog posts.
- **Ownership Authorization**: Strict checks ensure users can only modify or delete their own content.
- **Interactive Commenting**: Users can view posts and leave comments.
- **Flexible Content Categorization**: A many-to-many relationship allows posts to have multiple categories.
- **User-Friendly CLI**: A menu-driven interface guides the user through all available actions.

---

## 🏛️ Architecture & Schema

- The project follows a simple, three-tier architecture, all running locally.
```sh
[ User ] <--> [ Terminal (CLI) ] <--> [ Python Application Logic ] <--> [ MySQL Database ]
```
- The database schema is the heart of the project, featuring five interconnected tables to model the blog's data structure effectively.
- **users** & **posts**: A one-to-many relationship. One user can write many posts.
- **posts** & **comments**: A one-to-many relationship. One post can have many comments.
- **posts** & **categories**: A many-to-many relationship. A post can belong to multiple categories, and a category can contain multiple posts. This is achieved using a junction table called post_categories.

---

## 🛠️ Technology Stack
- **Backend**: Python 3
- **Database**: MySQL
- **Key Libraries**:
     - **mysql-connector-python**: The official driver for connecting Python to MySQL.
     - **hashlib**: For implementing secure password hashing.
     - **getpass**: For allowing users to type their password without it being displayed on screen.

---

## ⚙️ Setup and Installation

Follow these steps to get your local environment running.
1. Prerequisites
    - **Python 3.8** or higher
    - **XAMPP** (or a standalone MySQL server)
    - **Git** for cloning the repository.
2. Clone the Repository
```sh
git clone [https://github.com/KunalChoudhary07/Command-Line-Interface-Blogging-Platform.git](https://github.com/KunalChoudhary07/Command-Line-Interface-Blogging-Platform.git)
cd Command-Line-Interface-Blogging-Platform
```
3. Set Up the Database
   1. Start the _**MySQL**_ service from your XAMPP Control Panel.
   2. Navigate to http://localhost/phpmyadmin.
   3. If the localhost is not working than start _Apache_ service from your XAMPP Control Panel.
   4. Create a new database named _**blog_db**_.
   5. Select _**blog_db**_ and go to the SQL tab.
   6. Execute the script provided in schema.sql to create all the tables._
    - Note: The full SQL script can be found in a schema.sql file in the repository.
4. Install Dependencies
- Using a virtual environment is highly recommended and in this we have created a new Virtual environment.
```sh
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Install requirements
pip install mysql-connector-python
```
- Using the default Virtual environment where python is installed.
```sh
# Install requirements
pip install mysql-connector-python
```
5. Run the Application
```sh
project_code.py
```

---

## 🔮 Future Improvements

- This project has a solid foundation that can be extended with many exciting features:
     - **Web Frontend**: Build a web-based API using Flask or Django and connect it to a modern frontend framework like React or Vue.js.
     - **Post Search**: Implement a search functionality to find posts by title or content.
     - **Full User Profiles**: Allow users to write and edit a personal bio.
     - **Advanced Security**: Upgrade password hashing from sha256 to a stronger, salted algorithm using a library like bcrypt.
     - **Comment Moderation**: Fully implement the pending status for comments, allowing authors to approve or deny them.

---

## 📜 License
- **This project is licensed under the MIT License.**
