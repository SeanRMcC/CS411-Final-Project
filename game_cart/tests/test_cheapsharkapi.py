import pytest
import requests
from game_cart.utils.cheapsharkapi import search_for_games, get_game_info

KEYWORD = "minecraft"
GAME_ID = 258010
MAX_NUM_GAMES = 10

@pytest.fixture
def mock_search_response(mocker):
    """Fixture to mock the response for searching games."""
    mock_response = mocker.Mock()
    mock_response.json.return_value = [
        {"external": "Minecraft Legends", "gameID": "258010", "cheapest": "39.99"},
        {"external": "Minecraft Dungeons", "gameID": "234902", "cheapest": "19.99"},
        {"external": "Minecraft Dungeons (XBOX)", "gameID": "225056", "cheapest": "19.99"},
        {"external": "Minecraft Dungeons: Ultimate DLC Bundle", "gameID": "234200", "cheapest": "19.99"},
    ]
    mocker.patch("requests.get", return_value=mock_response)
    return mock_response


@pytest.fixture
def mock_game_info_response(mocker):
    """Fixture to mock the response for fetching game info by ID."""
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "info": {"title": "Minecraft Legends"},
        "cheapestPriceEver": {"price": "39.99"},
    }
    mocker.patch("requests.get", return_value=mock_response)
    return mock_response


def test_search_for_games(mock_search_response):
    """Test the search_for_games function."""
    result = search_for_games(KEYWORD)
    assert len(result) == 4
    assert result[0]["name"] == "Minecraft Legends"
    assert result[0]["price"] == "39.99"


def test_search_for_games_timeout(mocker):
    """Simulate a timeout for search_for_games."""
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)

    with pytest.raises(RuntimeError, match="Request to cheapshark.com timed out."):
        search_for_games(KEYWORD)


def test_search_for_games_request_failure(mocker):
    """Simulate a request failure for search_for_games."""
    mocker.patch(
        "requests.get", side_effect=requests.exceptions.RequestException("Connection error")
    )

    with pytest.raises(RuntimeError, match="Request to cheapshark.com failed: Connection error"):
        search_for_games(KEYWORD)


def test_get_game_info(mock_game_info_response):
    """Test the get_game_info function."""
    result = get_game_info(GAME_ID)
    assert result["name"] == "Minecraft Legends"
    assert result["price"] == "39.99"
    assert result["id"] == GAME_ID


def test_get_game_info_timeout(mocker):
    """Simulate a timeout for get_game_info."""
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)

    with pytest.raises(RuntimeError, match="Request to cheapshark.com timed out."):
        get_game_info(GAME_ID)


def test_get_game_info_request_failure(mocker):
    """Simulate a request failure for get_game_info."""
    mocker.patch(
        "requests.get", side_effect=requests.exceptions.RequestException("Connection error")
    )

    with pytest.raises(RuntimeError, match="Request to cheapshark.com failed: Connection error"):
        get_game_info(GAME_ID)
