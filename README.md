This code is part of the coding assignment for Vurb Software Developer Intern (http://vurb.com/) The assignment was to implement an API endpoint for Vurb Decks and Cards.  
A Card is the smallest data unit that represents information about an entity. These cards can be saved into decks that are owned by users. Thus, A deck is a collection of cards.  
The implementation was done using Python FLASK-RESTful and Requests Library. More detail can be found in Description.txt  

There are 3 API's implemented  
* GET /users/{username}/decks  
(deck list endpoint, lists all decks for a user with minimal metadata,paginated using pageToken params, pageToken retrieves specific page of results)  
```json
{
    "decks": [
        {
            "desc": "deck1",
            "id": "1"
        }
    ],
    "nextPageToken": 2,
    "resultSizeEstimate": 2
}
```
* GET /decks/{id}  
(deck endpoint, gets the specified deck)  
```json
{
    "cards": [
        {
            "id": "1",
            "payload": {
                "data": "data1"
            },
            "title": "card1"
        },
        {
            "id": "2",
            "payload": {
                "data": "data2"
            },
            "title": "card2"
        }
    ],
    "desc": "deck1",
    "id": "1"
}
```
* GET /users/{username}/combineddecks  
(decks detail endpoint that uses the above two endpoints and prepares a combined 
response with deck detailed info resolved)  
```json
{
    "decks": [
        {
            "cards": [
                {
                    "title": "card1",
                    "id": "1",
                    "payload": {
                        "data": "data1"
                    }
                },
                {
                    "title": "card2",
                    "id": "2",
                    "payload": {
                        "data": "data2"
                    }
                }
            ],
            "id": "1",
            "desc": "deck1"
        }
    ],
    "nextPageToken": 2,
    "resultSizeEstimate": 2
}
```
