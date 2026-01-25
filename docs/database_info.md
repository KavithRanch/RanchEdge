## Alembic
Alembic is a great tool which helps ensure that postgres database reflects the schema coded within the project at very stage in the project.

Steps:
1. When a change is made locally, we use Alembic to detect the changes from the current database schema and new SQLAlchemy models.
2. Alembic creates a migration file
3. Devs review the migration file
4. if all is well we continue and devs run the migration.

```bash
docker compose exec backend alembic revision --autogenerate -m "message" # creates the migration file

docker compose exec backend alembic upgrade head # Apply migration
```