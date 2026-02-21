from fastapi import APIRouter, Query
from typing import Annotated
from app.constants.enums import EVSortingMethod
from app.schemas.ev_opportunities_response import EVOpportunitiesPage
from app.services.ev_service import fetch_ev_opportunities
from backend.app.db.session import SessionLocal

router = APIRouter(prefix="/api/v1/ev-opportunities", tags=["EV Opportunities"])


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
    # Placeholder implementation - replace with actual logic to fetch and filter EV opportunities

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
