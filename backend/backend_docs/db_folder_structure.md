# Database Folder Structure
This document contains db folder project structure

## engine.py
The engine.py file serves as the medium for connecting to Postgres. It doesn't open connections but just create the engine which will faciliate connections

## session.py
The session.py file serves as the medium for creating sessions with the database in order to run queries, update tables and other batabase actions

## base.py
base.py serves as the file defining how tables should be modelled.



