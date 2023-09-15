from bson import ObjectId
from flask import Flask, render_template, jsonify, url_for, request
from pymongo import MongoClient

app = Flask(__name__)
mongoclient = MongoClient("mongodb://localhost:27017")

db = mongoclient["training_db"]
ents = db["mix_entities"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tdscount/")
def count():
    tdcount = ents.count_documents({})
    return {"tdcount":tdcount}

@app.route("/td/<int:index>")
def get_td(index):
    td = ents.find({}).skip(index).limit(1)
    td = list(td)[0]
    
    if "_id" in td:
        td['_id'] = str(td['_id'])
    return td

@app.route("/removeent/", methods=["GET","POST"])
def remove_ent():
    data = request.get_json()
    ent = data["ent"]
    id = data["id"]
    res = ents.find_one({"_id":ObjectId(id)},{"entities":{"entities":ent}})
    print(res)
    return res



@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('images/favicon.png')

if __name__ == "__main__":
    app.run(debug=True, port=8080)