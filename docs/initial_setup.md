The following steps assume you have VS Code, Git and Docker installed on your local device

```bash 
# 1. Clone and navigate the project root folder
git clone https://github.com/<your-username>/RanchEdge.git
cd RanchEdge

# 2. Create the .env file from the .env.example template and replace the keys with your own
cp .env.example .env

# 3. Build the docker containers (-d is to gain access to cmd line again)
docker compose up -d --build

# 4. Create database tables by applying latest alembic migration
docker compose exec backend alembic upgrade head

# 5. Populate static seed reference tables
docker compose exec backend python -m app.cli.seed

# 6. Pull Odds mapped to a sport/league, betting markets, and sportsbooks which persists information to db and creates a odds_snapshot
docker compose exec backend python -m app.cli.ingest_odds \
  --sport_league basketball_nba \
  --markets h2h \
  --sportsbooks fanduel espnbet

# 7. Compute the true probabilities of an existing snapshot (if you ran previous command only one then snapshot_id = 1)
docker compose exec backend python -m app.cli.true_probabilities --snapshot <snapshot_id>

# 8. Compute the search for positive ev opportunities of an existing snapshot
docker compose exec backend python -m app.cli.ev_opportunities --snapshot <snapshot_id>
# You're all set for now!
```