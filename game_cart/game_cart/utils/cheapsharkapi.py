import logging
import requests
from typing import List, Any

from game_cart.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

base_url = "https://www.cheapshark.com/api/1.0/"

def search_for_games(keyword: str) -> List[dict[str, Any]]:
    """
        Gets a maximum of ten games and their prices based off of a keyword
        from cheapshark.com.

        Args:
            keyword (str): The search keyword.       

        Returns:
            List[dict[str, Any]]: A list of games where each entry contains
                the name of the game, the id, and the price.

        Raises:
            RuntimeError: If the request to cheapshark.com times out or causes any other exception.
    """
    url = f"{base_url}games?title={keyword}"

    try:
        logger.info(f"Fetching games with keyword {keyword}")
        response = requests.get(url, timeout=5)

        response.raise_for_status()

        data = response.json()

        games = []
        for game in data:
            games.append({
                "name": game["external"],
                "id": game["gameID"],
                "price": game["cheapest"]
            })
        
        MAX_NUM_GAMES = 10

        return games[:MAX_NUM_GAMES]


    except requests.exceptions.Timeout:
        logger.error("Request to cheapshark.com timed out.")
        raise RuntimeError("Request to cheapshark.com timed out.")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to cheapshark.com failed: {str(e)}")
        raise RuntimeError(f"Request to cheapshark.com failed: {str(e)}")

def get_game_info(gameID: int) -> dict[str, Any]:
    """
        Gets the price and name of the game corresponding to a given id
        from cheapshark.com

        Args:
            gameID (int): The id of the game whose info will be returned.

        Returns:
            dict[str, Any]: A dict containing the game id, name, and price or an 
                empty dict if a game does not exist with gameID

        Raises:
            RuntimeError: If the request to cheapshark.com times out or causes any other exceptions.
    """
    url = f"{base_url}games?id={gameID}"

    try:
        logger.info(f"Fetching game info for game with id: {gameID}.")
        response = requests.get(url, timeout=5)

        response.raise_for_status()

        data = response.json()

        return {
            "name": data["info"]["title"],
            "id": gameID,
            "price": data["cheapestPriceEver"]["price"]
        }
    except requests.exceptions.HTTPError:
        logger.warning(f"The id {gameID} does not have a corresponding game.")   
        return {}

    except requests.exceptions.Timeout:
        logger.error("Request to cheapshark.com timed out.")
        raise RuntimeError("Request to cheapshark.com timed out.")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to cheapshark.com failed: {str(e)}")
        raise RuntimeError(f"Request to cheapshark.com failed: {str(e)}")

