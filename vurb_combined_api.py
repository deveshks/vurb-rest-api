#!flask/bin/python

from flask import Flask, jsonify, abort, make_response,request
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from requests import get
import json
import time
import requests_cache
import os

app = Flask(__name__, static_url_path="")
api = Api(app)

requests_cache.install_cache(cache_name='vurb_combined_api_cache', backend='sqlite', expire_after=180)

payload_fields = {
    'data':fields.String
}

card_fields = {
    'id':fields.String,
    'title':fields.String,
    'payload':fields.Nested(payload_fields)
}

deck_fields_with_cards = {
    'id':fields.String,
    'desc':fields.String,
    'cards':fields.List(fields.Nested(card_fields))
}

combineddecks = {
	'decks':fields.List(fields.Nested(deck_fields_with_cards))
}

#For a given user, give all decks with the card details included
class CombinedDecksAPI(Resource):
    def get(self,username):
	try:
   		os.remove('response.txt')
   	except OSError:
   		pass
	f = open('response.txt','a')
    	numpages = int(request.args.get('pages'))
    	countperpage = int(request.args.get('results'))
    	nextPageToken = 1
    	start = time.time()
        '''Keep on incrementing nextPageToken until it is -1'''
    	while(nextPageToken != -1):
            #For every nextPageToken we get, call the API, and get the deck ID's from it
    		r = get('http://localhost:5000/users/'+username+'/decks?pages='+str(numpages)+"&results="+str(countperpage)+"&nextPageToken="+str(nextPageToken))
    		decksJSON = r.json()
    		decks = decksJSON['decks']
    		nextPageToken = decksJSON['nextPageToken']
    		resultSizeEstimate = decksJSON['resultSizeEstimate']
            #We get the deck empty, that means there are no more decks to be fetched, we exit
    		if(len(decks)>0):
	    		decksDict = {}
    			decksCardsIdDict = {}
    			decksCardsDict = {}
    			for i in range(0,len(decks)):
    				deckinfo = decks[i]
    				decksDict[deckinfo['id']] = deckinfo['desc']
    		
                # Use deck id to call below API, which gives us all the card ids of all the decks
                # which we store in a set
    			cardsIdSet = set()
    			for key in decksDict:
    				deckId = key
    				r = get('http://localhost:5000/decksalt/'+deckId)
    				deckJSON = r.json()
    				cardIds = deckJSON['cardIds']
    				decksCardsIdDict[key] = cardIds
    				for i in cardIds:
    					cardsIdSet.add(i)

                #Here we get detailed card info for all our cards. 
                #We then combined our deck id's with the 
                #detailed card info to present our output
    			cardsIdStr = ",".join(cardsIdSet)
    			r = get('http://localhost:5000/cards/"'+str(cardsIdStr)+'"')
    			cards = r.json()

    			for key in decksCardsIdDict:
    				cardsList = []
    				for i in decksCardsIdDict[key]:
    					cardsList.append(cards[i])
    				decksCardsDict[key] = cardsList	

    			combineddecksList = []	
    			for key in decksDict:
    				combineddeckDict = {}
    				deckId = key
    				deckDesc = decksDict[key]
    	
    				combineddeckDict['id'] = deckId
    				combineddeckDict['desc'] = deckDesc
    				combineddeckDict['cards'] = decksCardsDict[deckId]
    				combineddecksList.append(combineddeckDict)

    			combineddecksStr = [ob for ob in combineddecksList]
    			combinedDeck = {}
    			combinedDeck['decks'] = combineddecksStr
    			combinedDeck['nextPageToken'] = nextPageToken
    			combinedDeck['resultSizeEstimate'] = resultSizeEstimate
    			json_string = json.dumps(combinedDeck)
                #The combined output is written in the file
    			f.write(json_string)
    			f.write('\n')
    			f.write('---------------------------')	
    			f.write('\n')		

api.add_resource(CombinedDecksAPI, '/users/<username>/combineddecks', endpoint='combineddecks')

if __name__ == '__main__':
    app.run(debug=True,port=6000)
