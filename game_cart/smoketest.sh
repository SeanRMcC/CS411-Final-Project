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
  username=$1
  password=$2

  echo "Creating a new user: $username"
  response=$(curl -s -X POST "$BASE_URL/create-account" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$username\", \"password\": \"$password\"}")
  if echo "$response" | grep -q '"status": "user added"'; then
    echo "User created successfully: $username"
  else
    echo "Failed to create user. Response: $response"
    exit 1
  fi
}

login_user() {
  username=$1
  password=$2

  echo "Logging in user: $username"
  response=$(curl -s -X POST "$BASE_URL/login" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$username\", \"password\": \"$password\"}")
  if echo "$response" | grep -q '"message": "User .* logged in successfully."'; then
    echo "User logged in successfully: $username"
  else
    echo "Failed to log in user. Response: $response"
    exit 1
  fi
}


update_password() {
  username=$1
  new_password=$2

  echo "Updating password for user: $username"
  response=$(curl -s -X POST "$BASE_URL/update-password" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$username\", \"newPassword\": \"$new_password\"}")
  if echo "$response" | grep -q '"status": "password changed"'; then
    echo "Password updated successfully for user: $username"
  else
    echo "Failed to update password. Response: $response"
    exit 1
  fi
}

##########################################################
#
# Game Management
#
##########################################################

search_games_by_keyword() {
  keyword=$1

  echo "Searching for games with keyword ($keyword)..."
  response=$(curl -s -X GET "$BASE_URL/search-games/$keyword")
  if echo "$response" | grep -q '"games":'; then
    echo "Games searched successfully with keyword ($keyword)."
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
  id=$1

  echo "Adding game by ID ($id)..."
  response=$(curl -s -X POST "$BASE_URL/add-game" \
    -H "Content-Type: application/json" \
    -d "{\"id\": $id}")

  if echo "$response" | grep -q '"status": "game added"'; then
    echo "Game added successfully by ID ($id)."
  else
    echo "Failed to add game. Response: $response"
    exit 1
  fi
}


delete_game_from_cart_by_id() {
  id=$1

  echo "Deleting a game from the cart by ID ($id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-game" \
    -H "Content-Type: application/json" \
    -d "{\"id\": $id}")
  if echo "$response" | grep -q '"status": "game deleted"'; then
    echo "Game deleted successfully by id ($id)."
  else
    echo "Failed to delete game."
    exit 1
  fi
}

get_games_in_cart() {
  echo "Retrieving all games in cart..."
  response=$(curl -s -X GET "$BASE_URL/get-games")
  if echo "$response" | grep -q '"games":'; then
    echo "Games retrieved successfully."
  else
    echo "Failed to retrieve games."
    exit 1
  fi
}

get_total_price_of_cart() {
  echo "Retrieving total price of cart..."
  response=$(curl -s -X GET "$BASE_URL/get-total-price")
  if echo "$response" | grep -q '"price":'; then
    echo "Total price retrieved successfully."
  else
    echo "Failed to retrieve total price."
    exit 1
  fi
}

check_health

create_user user1 login123
login_user user1 login123
update_password user1 login123

search_games_by_keyword "Action"

add_game_to_cart_by_id 39
add_game_to_cart_by_id 66
add_game_to_cart_by_id 236717

delete_game_from_cart_by_id 39
delete_game_from_cart_by_id 66
delete_game_from_cart_by_id 236717

get_games_in_cart
get_total_price_of_cart

echo "All tests passed successfully!"