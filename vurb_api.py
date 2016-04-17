#!flask/bin/python

from flask import Flask, jsonify, abort, make_response,request
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
import json
import time
import cPickle as pickle
import requests_cache

app = Flask(__name__, static_url_path="")
api = Api(app)

requests_cache.install_cache(cache_name='vurb_api_cache', backend='sqlite', expire_after=180)

#Load the data to be returned by the API
deck = pickle.load( open( "deck.p", "rb" ) )

decks = pickle.load( open( "decks.p", "rb" ) )

cards = pickle.load( open( "cards.p", "rb" ) )

#Object definitions for the data
payload_fields = {
	'data':fields.String
}

card_fields = {
	'id':fields.String,
	'title':fields.String,
	'payload':fields.Nested(payload_fields)
}


deck_fields_with_cardIds = {
	'id':fields.String,
	'desc':fields.String,
	'cardIds':fields.List(fields.String)
}


deck_fields_with_cards = {
	'id':fields.String,
	'desc':fields.String,
	'cards':fields.List(fields.Nested(card_fields))
}

deck_fields_without_cards = {
	'id':fields.String,
	'desc':fields.String
}

decks_fields = {
	'decks':fields.List(fields.Nested(deck_fields_without_cards)), 
	'nextPageToken':fields.Integer,
	'resultSizeEstimate':fields.Integer
}

''' Lists all decks for a user
<numpages> is the number of pages to be retreived, with <numresults> results per page, 
and nextPageToken returns the next page of decks to be fetched. 
In my case, it is simply an integer pointing to the next page.
The response is sliced according to the numpages, with nextPageToken appended. 
It is appended -1 if it was the last page. resultSizeEstimate is now dumb and is assigned 
the value <numpages> times <numresults>'''
class DecksAPI(Resource):
	def get(self,username):

		numpages = int(request.args.get('pages'))
		countperpage = int(request.args.get('results'))
		nextPageToken = int(request.args.get('nextPageToken'))
		startIndex = (nextPageToken-1)*countperpage
		endIndex = ((nextPageToken)*countperpage)
		deckSlice = decks['decks'][startIndex:endIndex]
		deckSliceDict = {}
		deckSliceDict['decks'] = deckSlice
		'''The nextPageToken assignment is handled here, where we check 
		if the deck size being returned equals the numresults, 
		or nextPageToken exceeds numpages, in both cases, 
		that means we have finished up showing 
		all requested results, and we set nextPageToken= -1
		nextPageToken is incremented by 1 in API (1b) to 
		get the next set of results.'''
		if(len(deckSlice) == countperpage and nextPageToken < numpages):
			deckSliceDict['nextPageToken'] = nextPageToken+1
		else:
			deckSliceDict['nextPageToken'] = -1  
		deckSliceDict['resultSizeEstimate'] = numpages*countperpage
		if(len(deckSlice) == 0):
			deckSliceDict['nextPageToken'] = -1
		return  marshal(deckSliceDict, decks_fields)

'''Getets the specific deck, with the contained cards information expanded. It fetches the decks 
list with just the card ids listed, and uses those card id's to get the card information.
 <id> is assumed to be a number for simplicity'''
class DeckAPI(Resource):

	def get(self, id):
		dck = [d for d in deck if d['id'] == id]
		#Get the list of card ids for deck with id 'id'
		cardIdsList = dck[0]['cardIds']
		cardsList = []
		for i in cardIdsList:
			cardsList.append(cards[i])
		#Put the cards info for the given card id list into a dictionary
		resultdeck = {}
		resultdeck['id'] = dck[0]['id']
		resultdeck['desc'] = dck[0]['desc']
		resultdeck['cards'] = [ob for ob in cardsList]
		if len(dck) == 0:
			abort(404)
		return marshal(resultdeck, deck_fields_with_cards)

'''Gets the specific decks, with only the card id's listed'''
class DeckAltAPI(Resource):
	def get(self, id):
		#get the deck with the given id
		dck = [d for d in deck if d['id'] == id]
		if len(dck) == 0:
			abort(404)
		return marshal(dck[0], deck_fields_with_cardIds)
		
'''Gets a list of  cards detailed info, given the list of comma separated card id's in <cardIdStr'''
class CardAPI(Resource):

	def get(self,cardIdStr):
		#Get the list of card ids 
		cardIdsList = json.loads(cardIdStr).split(",")
		cardsDict = {}
		#Put the cards info for the given into a dictionary
		for i in cardIdsList:
			cardsDict[i] = cards[i]
		return cardsDict

#defining the API's
api.add_resource(DecksAPI, '/users/<username>/decks', endpoint='decks')
api.add_resource(DeckAPI, '/decks/<id>', endpoint='deck')
api.add_resource(DeckAltAPI,'/decksalt/<id>',endpoint='deckalt')
api.add_resource(CardAPI, '/cards/<cardIdStr>', endpoint='card')

if __name__ == '__main__':
	app.run(debug=True,port=5000)