import json
from flask import Flask,Markup,render_template

app = Flask(__name__)
def makeResponse(data):
    return app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
def check(data):

	dict = {
	"_id": False,
	"name":False,
	"budget":False,
	"genres":False,
	"description":False,
	"popularity":False,
	"production_companies":False,
	"vote_average":False,
	"vote_count":False,
	"release_date":False,
	"revenue":False,
	"runtime":False,
	"imdb_id":False,
	"adult":False,	
	"language":False
	}
	for ele in data:
		if ele in dict:
			del dict[ele]
	return dict
