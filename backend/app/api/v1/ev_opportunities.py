"""
This module defines the API endpoint for retrieving EV (Expected Value) opportunities.
It allows clients to query for EV opportunities with various filtering and sorting options, such as limiting the number of results, filtering by league or sportsbook, and sorting by EV or edge.
The endpoint interacts with the database to fetch the relevant data and returns it in a structured format.

Author: Kavith Ranchagoda
Last Updated:
"""

from fastapi import APIRouter, Query
from typing import Annotated
from app.constants.enums import EVSortingMethod
from app.schemas.ev_opportunities_response import EVOpportunitiesPage
from app.services.ev_service import fetch_ev_opportunities
from backend.app.db.session import SessionLocal

router = APIRouter(prefix="/api/v1/ev-opportunities", tags=["EV Opportunities"])


# Endpoint to retrieve EV opportunities with various filtering and sorting options
@router.get("/", response_model=EVOpportunitiesPage)
def get_ev_opportunities(
    limit: Annotated[int, Query(description="The maximum number of EV opportunities to return", ge=1, le=50)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    latest_snapshot: Annotated[
        bool, Query(description="Return only the latest snapshot or all historical snapshots both per league ")
    ] = True,
    is_positive_ev: Annotated[bool, Query(description="Return positive EV opportunities")] = True,
    min_ev: Annotated[float, Query(description="The minimum EV value to include in results", ge=0.0)] = 0.0,
    league_id: Annotated[int | None, Query(description="Filter by league ID")] = None,
    sportsbook_id: Annotated[int | None, Query(description="Filter by sportsbook ID")] = None,
    sort: Annotated[list[EVSortingMethod], Query(description="Sort by ev, edge, start time or pulled at")] = [
        EVSortingMethod.EV_DESC,
        EVSortingMethod.EDGE_DESC,
    ],
):

    # Create a new database session and fetch EV opportunities based on the provided query parameters
    with SessionLocal() as session:
        return fetch_ev_opportunities(
            session=session,
            limit=limit,
            offset=offset,
            latest_snapshot=latest_snapshot,
            is_positive_ev=is_positive_ev,
            min_ev=min_ev,
            league_id=league_id,
            sportsbook_id=sportsbook_id,
            sort=sort,
        )
