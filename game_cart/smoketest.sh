#!/bin/bash

# Base URL of the Flask API
BASE_URL="http://localhost:5000"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

###############################################
#
# Health checks
#
###############################################

check_health() {
  echo "Checking API health..."
  response=$(curl -s -X GET "$BASE_URL/health")
  if echo "$response" | grep -q '"status": "healthy"'; then
    echo "API is healthy."
  else
    echo "API health check failed. Response: $response"
    exit 1
  fi
}

##########################################################
#
# User Management
#
##########################################################

create_user() {
  echo "Creating a new user..."
  response=$(curl -s -X POST "$BASE_URL/create-account" \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "password123"}')
  if echo "$response" | grep -q '"status": "user added"'; then
    echo "User created successfully."
  else
    echo "Failed to create user."
    exit 1
  fi
}

login_user() {
  echo "Logging in user..."
  response=$(curl -s -X POST "$BASE_URL/login" \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "password123"}')
  if echo "$response" | grep -q '"message": "User testuser logged in successfully."'; then
    echo "User logged in successfully."
  else
    echo "Failed to log in user."
    exit 1
  fi
}

update_password() {
  echo "Updating user password..."
  response=$(curl -s -X POST "$BASE_URL/update-password" \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "newPassword": "newpassword123"}')
  if echo "$response" | grep -q '"status": "password changed"'; then
    echo "Password updated successfully."
  else
    echo "Failed to update password."
    exit 1
  fi
}

##########################################################
#
# Game Management
#
##########################################################

search_games_by_keyword() {
  echo "Searching for games with keyword 'action'..."
  response=$(curl -s -X GET "$BASE_URL/search-games/action")
  if echo "$response" | grep -q '"games":'; then
    echo "Games searched successfully."
  else
    echo "Failed to search games."
    exit 1
  fi
}

##########################################################
#
# Cart Management
#
##########################################################

add_game_to_cart_by_id() {
  echo "Adding a game to the cart by ID..."
  response=$(curl -s -X POST "$BASE_URL/add-game" \
    -H "Content-Type: application/json" \
    -d '{"id": 39}')
  if echo "$response" | grep -q '"status": "game added"'; then
    echo "Game added successfully."
  else
    echo "Failed to add game."
    exit 1
  fi
}


delete_game_from_cart_by_id() {
  echo "Deleting a game from the cart by ID..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-game" \
    -H "Content-Type: application/json" \
    -d '{"id": 39}')
  if echo "$response" | grep -q '"status": "game deleted"'; then
    echo "Game deleted successfully."
  else
    echo "Failed to delete game."
    exit 1
  fi
}

get_games_in_cart() {
  echo "Retrieving all games in the cart..."
  response=$(curl -s -X GET "$BASE_URL/get-games")
  if echo "$response" | grep -q '"games":'; then
    echo "Games retrieved successfully."
  else
    echo "Failed to retrieve games."
    exit 1
  fi
}

get_total_price_of_cart() {
  echo "Retrieving the total price of the cart..."
  response=$(curl -s -X GET "$BASE_URL/get-total-price")
  if echo "$response" | grep -q '"price":'; then
    echo "Total price retrieved successfully."
  else
    echo "Failed to retrieve total price."
    exit 1
  fi
}

check_health
create_user
login_user
update_password
search_games_by_keyword
add_game_to_cart_by_id
delete_game_from_cart_by_id
get_games_in_cart
get_total_price_of_cart

echo "All tests passed successfully!"