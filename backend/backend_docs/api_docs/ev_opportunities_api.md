# GET /api/v1/ev-opportunities
This API will be specifically used for users to gain access to all ev opportunities

It will be sortable by edge and event_id in both ascending and descending order

It will be filterable by edge, event commence time, sportsbook.

It will paginated displaying 20 opportunities at a time.

### Query Parameters:
- **limit** &rarr; default=20, max=50
- **offset** &rarr; default=0
- **latest_snapshot** &rarr; default=True
    * Will return latest snapshot per league requested in league_id (or for each if league_id is Null)
- **is_positive_ev** &rarr; default=True
- **min_ev** &rarr; default=0.0
- **league_id** &rarr; Optional
- **sportsbook_id** &rarr; Optional
- **sort** &rarr; default=ev_desc,edge_desc
    * Could also possibly be ev_(asc/desc), edge_(asc/desc), start_time_(asc/desc), pulled_at_(asc/desc)

### Response Shape:
This shape will be in the form 

