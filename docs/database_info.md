# Database Information

This project will be using SQLAlchemy & Alembic for establishing the database

## SQLAlchemy
It is python's main database framework. It allows python code to communicate with databases.

SQLAlchemy has two main components:
1. **Core**: It allows us to perform database operations in lower level SQL-like expressions
    - Bulk Operations 
    - Data Migrations
2. **ORM (Object-Relational Mapping)**: It is able to represent database components as objects (rows) and classes (tables). This makes it much easier to navigate relationships between components.
ORM is great for:
    - Defining database schema/models
    - Simple CRUD operations


For the scope of this project the ORM will be used for simple database calls including regular actions, simple filtering and so on. Core will be used for more complex and specific filtering calls as required.

## Alembic
Alembic is a great tool which helps ensure that postgres database reflects the schema coded within the project at very stage in the project.

Steps:
1. When a change is made locally, we use Alembic to detect the changes from the current database schema and new SQLAlchemy models.
2. Alembic creates a migration file
3. Devs review the migration file
4. if all is well we continue and devs run the migration.