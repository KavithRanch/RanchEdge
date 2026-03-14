from __future__ import annotations

from typing import Any


def _extract_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and "ev_opportunities" in payload:
        items = payload["ev_opportunities"]
        if isinstance(items, list):
            return items

    raise AssertionError(
        f"Unexpected response shape. Expected dict with 'ev_opportunities', got: "
        f"{list(payload.keys()) if isinstance(payload, dict) else type(payload).__name__}"
    )


def _assert_common_item_shape(item: dict[str, Any]) -> None:
    required_fields = {
        "ev_per_dollar",
        "edge",
        "is_positive_ev",
    }

    missing = required_fields - item.keys()
    assert not missing, f"Missing expected response fields: {missing}"

    assert isinstance(item["is_positive_ev"], bool)
    assert isinstance(item["ev_per_dollar"], (int, float))
    assert isinstance(item["edge"], (int, float))


def test_get_ev_opportunities_returns_200(client, ev_endpoint) -> None:
    response = client.get(ev_endpoint)
    assert response.status_code == 200


def test_get_ev_opportunities_returns_json(client, ev_endpoint) -> None:
    response = client.get(ev_endpoint)
    assert response.status_code == 200
    assert "application/json" in response.headers.get("content-type", "")


def test_get_ev_opportunities_returns_expected_page_shape(client, ev_endpoint) -> None:
    response = client.get(ev_endpoint)
    assert response.status_code == 200

    payload = response.json()

    assert isinstance(payload, dict)
    assert "total" in payload
    assert "next_offset" in payload
    assert "ev_opportunities" in payload
    assert isinstance(payload["total"], int)
    assert (payload["next_offset"] is None) or isinstance(payload["next_offset"], int)
    assert isinstance(payload["ev_opportunities"], list)


def test_get_ev_opportunities_item_shape_if_results_exist(client, ev_endpoint) -> None:
    response = client.get(ev_endpoint)
    assert response.status_code == 200

    items = _extract_items(response.json())

    if items:
        _assert_common_item_shape(items[0])


def test_is_positive_ev_filter_returns_only_positive_rows(client, ev_endpoint) -> None:
    response = client.get(ev_endpoint, params={"is_positive_ev": "true"})
    assert response.status_code == 200

    items = _extract_items(response.json())

    for item in items:
        _assert_common_item_shape(item)
        assert item["is_positive_ev"] is True


def test_min_ev_filter_returns_only_rows_meeting_threshold(client, ev_endpoint) -> None:
    min_ev = 0.01

    response = client.get(ev_endpoint, params={"min_ev": str(min_ev)})
    assert response.status_code == 200

    items = _extract_items(response.json())

    for item in items:
        _assert_common_item_shape(item)
        assert item["ev_per_dollar"] >= min_ev


def test_limit_parameter_caps_number_of_results(client, ev_endpoint) -> None:
    limit = 5

    response = client.get(ev_endpoint, params={"limit": limit})
    assert response.status_code == 200

    items = _extract_items(response.json())
    assert len(items) <= limit


def test_offset_parameter_does_not_crash(client, ev_endpoint) -> None:
    response = client.get(ev_endpoint, params={"offset": 1})
    assert response.status_code == 200

    items = _extract_items(response.json())
    assert isinstance(items, list)


def test_sort_by_ev_desc_if_supported(client, ev_endpoint) -> None:
    response = client.get(ev_endpoint, params={"sort": "ev_desc"})
    assert response.status_code == 200

    items = _extract_items(response.json())
    ev_values = [item["ev_per_dollar"] for item in items]

    assert ev_values == sorted(ev_values, reverse=True)


def test_sort_by_edge_desc_if_supported(client, ev_endpoint) -> None:
    response = client.get(ev_endpoint, params={"sort": "edge_desc"})
    assert response.status_code == 200

    items = _extract_items(response.json())
    edge_values = [item["edge"] for item in items]

    assert edge_values == sorted(edge_values, reverse=True)


def test_unknown_query_param_is_ignored_and_does_not_crash(client, ev_endpoint) -> None:
    response = client.get(ev_endpoint, params={"totally_fake_param": "123"})
    assert response.status_code == 200

    items = _extract_items(response.json())
    assert isinstance(items, list)


def test_invalid_limit_returns_422(client, ev_endpoint) -> None:
    response = client.get(ev_endpoint, params={"limit": -1})
    assert response.status_code == 422


def test_invalid_offset_returns_422(client, ev_endpoint) -> None:
    response = client.get(ev_endpoint, params={"offset": -1})
    assert response.status_code == 422


def test_invalid_sort_value_returns_422(client, ev_endpoint) -> None:
    response = client.get(ev_endpoint, params={"sort": "sideways"})
    assert response.status_code == 422