## MVP Scope

The RanchEdge MVP is a decision-support system designed to find market misprices and analyses how these perform over time in comparison to their expected value

### Features
- Automatically ingests sportsbook odds for NBA player prop markets
- Computes vig-removed consensus probabilities
- Identifies positive expected value (+EV) opportunities
- Stores and serves those opportunities via an API
- Allows users to log bets taken
- Evaluates decision quality by comparing expected vs actual performance over time

### Explicit MVP Constraints
- NBA only
- Two-outcome markets only (Over/Under)
- One odds source minimum
- Flat stake model
- Manual bet settlement
- No outcome prediction models
- No authentication