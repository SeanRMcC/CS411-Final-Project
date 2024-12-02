from flask import Flask, jsonify, make_response, Response, request

from game_cart.db import db
from game_cart.models.user_model import User
from game_cart.utils.cheapsharkapi import search_for_games

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////app/db/app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

####################################################
#
# Healthchecks
#
####################################################

@app.route("/health", methods=["GET"])
def healthcheck() -> Response:
    """
    Health check route to verify the service is running.

    Returns: 
        JSON response indicating the health status of the service.
    """
    app.logger.info("Health check")
    return make_response(jsonify({"status": "healthy"}), 200)

####################################################
#
# User management
#
####################################################

@app.route("/create-account", methods=["POST"])
def create_user() -> Response:
    """
    Route to create a new user.

    Expected JSON Input:
        - username (str): The username for the new user.
        - password (str): The password for the new user.

    Returns:
        JSON response indicating the success of user creation.
    Raises:
        400 error if input validation fails.
        500 error if there is an issue adding the user to the database.
    """
    app.logger.info("Creating new user")
    try:
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return make_response(jsonify({"error": "Invalid input, both username and password are required"}), 400)
        
        app.logger.info("Adding user: %s", username)
        User.create_user(username, password)

        app.logger.info("User added: %s", username)
        return make_response(jsonify({"status": "user added", "username": username}), 201)
    except Exception as e:
        app.logger.error("Failed to add user: %s", str(e))
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/login", methods=["POST"])
def login() -> Response:
    """
    Route to log in a user.

    Expected JSON Input:
        - username (str): The username of the user.
        - password (str): The user's password.

    Returns:
        JSON response indicating the success of the login.

    Raises:
        400 error if input validation fails.
        401 error if authentication fails (invalid username or password).
        500 error for any unexpected server-side issues.
    """
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        app.logger.error("Invalid request payload for login.")
        return make_response(jsonify({"error": "Invalid input, both username and password are required"}), 400)

    username = data["username"]
    password = data["password"]

    try:
        if not User.check_password(username, password):
            app.logger.warning("Login failed for username: %s", username)
            return make_response(jsonify({"error": "Invalid username or password"}), 401)
        
        app.logger.info("User %s logged in successfully.", username)
        return make_response(jsonify({"message": f"User {username} logged in successfully."}), 200)
    
    except Exception as e:
        app.logger.error("Error during login for username %s: %s", username, str(e))
        return make_response(jsonify({"error", "An unexpected error occurred."}), 500)
    
@app.route("/update-password", methods=["POST"])
def update_password() -> Response:
    """
    Route to change a user's password. 

    Expected JSON Input: 
        - username (str): The username of the account whose password will change.
        - newPassword (str): The new password.

    Returns: 
        JSON response indicating the success of the password change. 

    Raises:
        400 error if input validation fails.
        401 error if authentication fails (username does not exist).
        500 error for any unexpected server-side issues.
    """
    app.logger.info("Chaninger a user's password")
    try:
        data = request.get_json()

        username = data.get("username")
        new_password = data.get("newPassword")

        if not username or not new_password:
            return make_response(jsonify({"error": "Invalid input, both username and new password are required"}), 400)
        
        app.logger.info("Changing user %s's password", username)
        User.update_password(username, new_password)

        app.logger.info("Password changed for %s", username)
        return make_response(jsonify({"status": "password changed", "username": username}), 201)
    except ValueError:
        app.logger.error("User %s does not exist", username)
        return make_response(jsonify({"error": f"user {username} does not exist"}), 401)
    except Exception as e:
        app.logger.error("Failed to update password: %s", str(e))
        return make_response(jsonify({"error": str(e)}), 500)
    
####################################################
#
# Game cart routes
#
####################################################

@app.route("/search-games/<keyword>", methods=["GET"])
def search_games(keyword: str) -> Response:
    """
        Route to search for games given a keyword.

        Path Parameters:
            - keyword (str): The keyword that will be used to search for the games.

        Returns:
            JSON response with the list of games matching the search.
        Raises:
            500 error if there is an issue retrieving the games from the api.
    """
    app.logger.info(f"Searching for games with keyword {keyword}")
    try:
        games = search_for_games(keyword)

        return make_response(jsonify({"games": games}), 200)
    except Exception as e:
        app.logger.error(f"Error searching for games: {e}")
        return make_response(jsonify({"error": str(e)}), 500)
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)