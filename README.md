This code is part of the coding assignment for Vurb Software Developer Intern (http://vurb.com/) The assignment was to implement an API endpoint for Vurb Decks and Cards.  
A Card is the smallest data unit that represents information about an entity. These cards can be saved into decks that are owned by users. Thus, A deck is a collection of cards.  
The implementation was done using Python FLASK-RESTful and Requests Library. More detail can be found in Description.txt  

There are 3 API's implemented  
1. GET users/{username}/decks  
(deck list endpoint, lists all decks for a user with minimal metadata,paginated using pageToken params, pageToken retrieves specific page of results)  
```json
{ 
  "decks": [ 
    { 
      "id": string, 
      "desc": string, 
    }, 
    ... 
  ], 
  "nextPageToken": string, 
  "resultSizeEstimate": integer 
} 
```
2. GET /decks/{id}  
(deck endpoint, gets the specified deck)  
```json
{ 
  "id": string, 
  "desc": string, 
  "cards": [ 
    { 
      "id": string, 
      "title": string, 
      "payload": { 
        ... 
      } 
    }, 
    ... 
  ] 
} 
```
3. GET users/{username}/combineddecks  
(decks detail endpoint that uses the above two endpoints and prepares a combined 
response with deck detailed info resolved)  
```json
{ 
  "decks": [ 
   { 
     "id": string, 
     "desc": string, 
     "cards": [ 
      { 
        "id": string, 
        "title": string, 
        "payload": { 
          ... 
        } 
      }, 
      ... 
    ] 
  } 
  ... 
  ], 
  "nextPageToken": string, 
  "resultSizeEstimate": integer 
}
```
