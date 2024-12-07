# Game Cart: 
## Buying games has never been easier!
By Sean McCarty (mccartys@bu.edu), Jed Tan (jctan@bu.edu), and Chanrithya Ngim (nclan@bu.edu)

### What is Game Cart? 
Game cart is a REST API that allows users to:

* Look up games by a keyword
* Add a game + its information to to their cart given its game id
* Delete a game by its id
* Return a list of all games and their prices in the user's cart
* Return the total price of the user's cart

We used the [cheapshark api](https://apidocs.cheapshark.com/) to get game search as well as game prices. 

---
## Routes:

#### /search-game/\<keyword>

* Request type: GET
* Purpose: Search for games based on the keyword (returns a max of 10 games)
* Path Parameters: 
    * keyword (str): The keyword that will be used in the search
* Response format: JSON
    * Success Response Example: 
        * Code 200
        * Content: `{ "games": [LIST OF GAMES MATCHING QUERY]}`
* Example curl request:
`curl -X GET http://localhost:5000/search-games/batman` 
* Example JSON response:
```
{
  "games": [
    {
      "id": "612",
      "name": "LEGO Batman",
      "price": "15.95"
    },
    {
      "id": "167613",
      "name": "LEGO Batman 2",
      "price": "15.95"
    },
    ...
  ]
}
```

#### /add-game

* Request type: POST
* Purpose: Adds a game (name, id, price) to the cart with a given id
* Request Body: 
    * id (int): The id of the game 
* Response format: JSON
    * Success Response Example:
        * Code 201
        * Content: `{"game": GAME NAME, "status": "game added"}`
* Example curl request:
`curl -X POST http://localhost:5000/add-game -H "Content-Type: application/json" -d '{"id": 612}'`
* Example JSON response:
```
{
  "game": "LEGO Batman",
  "status": "game added"
}
```

#### /delete-game

* Request type: DELETE
* Purpose: Deletes a game from the cart with a given id
* Request Body: 
    * id (int): The id of the game
* Response format JSON
    * Success Response Example:
        * Code 200
        * Content: `{"status": "game deleted"}`
* Example curl request:
`curl -X DELETE http://localhost:5000/delete-game -H "Content-Type: application/json" -d '{"id": 612}'`
* Example JSON response:
```
{
  "status": "game deleted"
}
```

#### /get-games

* Request type: GET
* Purpose: Returns all of the games in the cart
* Response format: JSON
    * Success Response Example:
        * Code: 200
        * Content: `{"games": [ALL GAMES IN CART]}`
* Example curl request:
`curl -X GET http://localhost:5000/get-games`
* Example JSON response:
```
{
  "games": [
    {
      "id": 400,
      "name": "Nancy Drew: The Haunted Carousel",
      "price": 2.09
    },
    {
      "id": 500,
      "name": "iBomber Defense",
      "price": 0.74
    },
    ...
  ]
}
```

#### /get-total-price

* Request type: GET
* Purpose: Returns the price of all of the games in the cart
* Response format: JSON 
    * Success Response Example:
        * Code: 200
        * Content: `{"price": TOTAL PRICE OF CART}`
* Example curl request:
`curl -X GET http://localhost:5000/get-total-price`
* Example JSON response:
```
{
  "price": 4.07
}
```