from dataclasses import asdict, dataclass
import logging
from typing import Any, List

from sqlalchemy.exc import IntegrityError

from game_cart.db import db
from game_cart.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

@dataclass
class Games(db.Model):
    __tablename__ = "games"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(80), nullable=False)
    price: float = db.Column(db.Float, nullable=False)

    @classmethod
    def create_game(cls, id: int, name: str, price: float) -> None:
        """
            Add a new game in the database.

            Args:
                id (int): The id of the game.
                name (str): The name of the game.
                price (float): The price of the game.

            Raises:
                IntegrityError: If there is a db error.
        """

        new_game = cls(id=id, name=name, price=price)
        try: 
            db.session.add(new_game)
            db.session.commit()
            logger.info("Game successfully added to the database: %s", name)
        except Exception as e:
            db.session.rollback()
            if isinstance(e, IntegrityError):
                logger.error(f"Integrity error with following entry: id {id} name {name} price {price}")
                raise ValueError(f"Game with id {id} already exists")
            else:
                logger.error(f"Database error: {str(e)}")
                raise

    @classmethod
    def delete_game(cls, game_id: int) -> None:
        """
            Delete a game from the database.

            Args: 
                game_id (int): The id of the game to delete.

            Raises:
                ValueError: If a game with that id is not in the database.
        """
        game = cls.query.filter_by(id=game_id).first()
        if not game:
            logger.info(f"Game with id {game_id} not found")
            raise ValueError(f"Game with id {game_id} not found")
        db.session.delete(game)
        db.session.commit()
        logger.info(f"Game with id {game_id} deleted successfully")
    
    @classmethod
    def get_all_games(cls) -> List[dict[str, Any]]:
        """
            Retrieves all games from the database.

            Returns:
                List[dict[str, Any]]: A list of all of the games in the database.

        """
        games = cls.query.all()

        logger.info("Games retrieved successfully")

        return [asdict(game) for game in games]
