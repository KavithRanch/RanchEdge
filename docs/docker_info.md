# Docker Information
This is the first time using docker, so this documentation is purely for a quick overlay on how it works in general and within this project scope

---
## Purpose
Docker eliminates the issue of your code working on just your machine and not others by packaging all the code, libraries, dependencies and configurations. 

---
## Concept Components
Images and Containers are the founding principles of Docker.
### Docker Image
An image contains all necessary information to run a service:
- [x] Code
- [x] Libraries (python, pandas & etc.)
- [x] Dependencies 
- [x] Configurations (port #, .env variables & etc.)

Each image typically maps to one subsystem (backend, frontend, db & etc.)

### Docker Container
Containers are the workers that run the services. Multiple containers can map to one image. 

Each container is capable of handling a certain throughput of requests so adding more containers, while more expensive, helps spread the load of handling those service requests amongst the containers.

## Docker Dev Components
These components help create images and containers in code.
### Dockerfile
These define **how images are created**, basically a build script (like a MakeFile). Each dockerfile maps to a subsystem.


```dockerfile
# 1. Choose a base image (base python 3.11)
FROM python:3.11-slim

# 2. Set working directory inside container 
WORKDIR /app

# 3. Copy dependency list from computer to container
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code into the container
COPY app/ app/

# 6. Expose the port the app runs on
EXPOSE 8000

# 7. Command to start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml
Declares how the different **subsystems should work together**

```yml
version: "3.9"

services:
  backend:
    build: ./backend
    container_name: backend-container
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:15
    container_name: postgres-container
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: ranchdb
    ports:
      - "5432:5432"
```

#### Compose commands:

```bash
# Creates containers and builds anytime a docker image is new/modified
# Need to run the first time, when Dockerfile or requirements.txt changes
docker compose --build

# Creates and starts containers
docker compose up 

# Stops and removes all containers
docker compose down 

# Allows us to run commands from within a container
docker compose exec <service_name> <command>
# Examples:
docker compose exec db psql -U postgres -d ranchedge # Hop into psql and run db commands
docker compose exec backend alembic revision --autogenerate -m "message" # Create Alembic Migration File
docker compose exec backend alembic upgrade head # Apply the migration file to the head



```

### .dockerignore
Lists which files should be **avoided from packaging**. Things like *node_modules*, *.env*, *.git* and *local config files*.

