from flask import Flask,Markup,render_template
from pymongo import MongoClient
import json
from utils import makeResponse
from bson import ObjectId
from flask import request
import jsonify
from collections import Counter

client = MongoClient('localhost', 27017)
db = client['movies']
app = Flask(__name__)

@app.route('/',methods=['POST'])
def hello_world():
    return 'Hello World!'

@app.route('/searchbyImdb',methods=['POST'])
def searchbyImdb():
	body =json.loads(request.data)
	doc = db.moviesnewfinal.find_one({"imdb_id":body['imdb_id']},{"_id":False})
	return  json.dumps({"result":doc})


@app.route('/searchbyQuery',methods=['POST'])
def searchbyQuery():
	table = db.moviesnewfinal
	body =json.loads(request.data)
	print(body['query'])
	doc =[]
	for s in table.find({body['field']:{"$regex": body['query']}},{"_id":False}).limit(10):
		doc.append(s)
	return  makeResponse(doc)

@app.route('/genres')
def genres():
    with open("./data/genres.json", "r") as f:
    	content = json.load(f)
    return makeResponse(content)

@app.route('/production_companies')
def production_companies():
    with open("./data/production_companies.json", "r") as f:
    	content = json.load(f)
    return makeResponse(content)

@app.route('/searchbyCharacter',methods=['POST'])
def searchbyCharacter():
	table = db.moviesnewfinal
	body =json.loads(request.data)
	condition ={"name":{"$regex": '^'+body['query'] , '$options' : 'i'}}
	doc =[]
	if "filter" not in body or len(body["filter"])==0:
		for s in table.find(condition,{"_id":False}).limit(10):
			doc.append(s)

	else:
		for s in table.find(condition,check(body['filter'])).limit(10):
			doc.append(s)
	return  makeResponse(doc)

@app.route('/searchbyPage',methods=['POST'])
def searchbyPage():
	table = db.moviesnewfinal
	body =json.loads(request.data)
	doc = []
	p = body['page']
	l = body['limit']
	totalData = table.count()
	print totalData
	if p*l > totalData or p ==0:
		doc.append({"result":"page is not present"})

	elif "filter" not in body or len(body["filter"])==0:
		for s in table.find({},{"_id":False}).limit(l).skip(l*(p-1)):
			doc.append(s)
	else:
		for s in table.find({},check(body['filter'])).limit(l).skip(l*(p-1)):
			doc.append(s)

	return  makeResponse(doc)


@app.route('/searchbyPageGenres',methods=['POST'])
def searchbyPageGenres():
	table = db.moviesnewfinal
	body =json.loads(request.data)
	p = body['page']
	l = body['limit']

	condition={body['field']:{"$regex": body['query']}}
	doc = []
	if p*l > totalData or p ==0:
		doc.append({"result":"page is not present"})

	elif "filter" not in body or len(body["filter"])==0:
		for s in table.find(condition,{"_id":False}).limit(l).skip(l*(p-1)):
			doc.append(s)
	else:
		if len(body["filter"])>0:
			for s in table.find(condition,check(body['filter'])).limit(l).skip(l*(p-1)):
				doc.append(s)

	return  makeResponse(doc)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3011,debug=True)
