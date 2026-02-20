# Expected Value (EV)
EV is generally a method for decision-making under uncertainty. It basically answers the question of `"if I make this decision repeatedly, will it yield good value on average"`. It tells us how profitable the opportunity is over the long-term.

It powers decisions in a plethora of fields including business-related decisions, investing/trading, sports markets and others.

## The Process
1. Ingest Sportsbook Odds
    * Convert American to Decimal odds
2. Calculate Implied Probability
    * We'll always see that when you sum implied probability of all outcomes, it will always be > 100%
    * This is due to Sportsbooks own Vig which is a factored into their odds which always guarantees a profit
    * Similar to trading fees/spread which allow investment firms to guarantee a profit regardless of how your investment goes.
3. Remove Vig to get "Fair Probability"
    * Normalize the implied probability to get the book's probability out of 100
4. Estimate True probability (Methods will be refined with future releases)
    * This is our data-driven assessment which also uses fair probability to put together our own true probability on the event.
    * **As of 0.6.0**: We take mean of all fair probabilities for an outcome over all sportsbooks as our True Probability
5. EV calculation
    * To calculate EV we use the decimal odds and our true probability
6. Check if it is a +EV opportunity meeting a certain threshold (eg. > 4%)
    * With a +EV opportunity, we expect over the long term, that outcome will provide value
7. Edge Calculation
    * Can calculate edge by substracting true_probability - implied_probability
    * It tells us by how many percentage points the sportsbook mispriced its probability compared to our modelling.