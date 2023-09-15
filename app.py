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

@app.route("/td/<int:index>")
def get_td(index):
    td = ents.find({"docbin":False}).skip(index).limit(1)
    td = list(td)[0]
    
    if "_id" in td:
        td['_id'] = str(td['_id'])
    return td

@app.route("/tdbrokencount/")
def get_tdbrokencount():
    cnt = ents.count_documents({"docbin":False})
    return {"count":cnt}

@app.route("/tdfixedcount/")
def get_tdfixedcount():
    cnt = ents.count_documents({"fixed":True})
    return {"count":cnt}

@app.route("/removeent/", methods=["GET","POST"])
def remove_ent():
    data = request.get_json()
    ent = data["ent"]
    id = data["id"]
    res = ents.update_one({"_id":ObjectId(id)},{"$pull":{"entities":ent}})
    # print(res)
    return data

@app.route("/edit_ent_values/", methods=["GET","POST"])
def edit_ent():
    data = request.get_json()
    ent = data["ent"]
    # print(ent)
    ent[0],ent[1] = int(ent[0]),int(ent[1])
    id = data["id"]
    if((ent[0] != "" or ent[1] != "") and (ent[1] > ent[0])):
        res = ents.update_one({"_id":ObjectId(id)},{"$push":{"entities":ent}})

    return data



@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('images/favicon.png')

if __name__ == "__main__":
    app.run(debug=True, port=8080)