import cPickle as pickle
from requests import get,exceptions


'''Generates the data to save cards
	Sample
	{
    '1': {
        'payload': {
            'data': 'data1'
        },
        'id': '1',
        'title': 'card1'
    },
    '2': {
        'payload': {
            'data': 'data2'
        },
        'id': '2',
        'title': 'card2'
    }
}'''
cardsDict = {}
for i in range(1,1001):
    cardDict = {}
    payloadDict = {}
    cardDict['id'] = str(i)
    cardDict['title'] = 'card'+str(i)
    payloadDict['data'] = 'data'+str(i)
    cardDict['payload'] = payloadDict
    cardsDict[str(i)] = cardDict

'''Generates the data for a specific deck
   Sample
   [
    {
        'cardIds': ['1','2'],
        'id': '1',
        'desc': 'deck1'
    },
    {
        'cardIds': ['11','12']
        'id': '2',
        'desc': 'deck2'
    }
]'''
decksList = []
for i in range(1,101):
    deckDict = {}
    deckDict['id'] = str(i)
    deckDict['desc'] = 'deck'+str(i)
    decksList.append(deckDict)    

'''Generates the data to save all decks for a user
	Sample
	{
    'decks': [
        {
            'id': '1',
            'desc': 'deck1'
        },
        {
            'id': '2',
            'desc': 'deck2'
        }
    ]
}'''
deckList = []
for i in range(1,101):
    deckDict = {}
    deckDict['id'] = str(i)
    deckDict['desc'] = 'deck'+str(i)
    cardIdsList = []
    for j in range((i*10-9),i*10+1):
        cardIdsList.append(str(j))
    deckDict['cardIds'] = cardIdsList
    deckList.append(deckDict)
      
decksDict = {}
decksDict['decks'] = decksList

#Save the generated data into pickles to be used by API
pickle.dump( cardsDict, open( "cards.p", "wb" ) )
pickle.dump( decksDict, open( "decks.p", "wb" ) )
pickle.dump( deckList, open( "deck.p", "wb" ) )


