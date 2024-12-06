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


