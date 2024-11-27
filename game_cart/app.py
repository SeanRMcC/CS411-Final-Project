from flask import Flask, jsonify, make_response, Response, request

from game_cart.db import db

app = Flask(__name__)

db.init_app(app)

with app.context():
    db.create_all()

@app.route("/api/health", methods=["GET"])
def healthcheck() -> Response:
    """
    Health check route to verify the service is running.

    Returns: 
        JSON response indicating the health status of the service.
    """
    app.logger.info("Health check")
    return make_response(jsonify({"status": "healthy"}), 200)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)