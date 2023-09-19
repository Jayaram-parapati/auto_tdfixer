from bson import ObjectId
from flask import Flask, render_template, jsonify, url_for, request
from pymongo import MongoClient
import spacy
import json
from spacy.tokens import DocBin
import itertools
import sys

app = Flask(__name__)
mongoclient = MongoClient("mongodb://localhost:27017")

db = mongoclient["training_db_080923"]
training_data = db.mixed_entities.find({})

i = 1
for td in training_data:
    
    text = td["text"]
    max = len(text)
    # print(max)
    for ent in td["entities"]:
        start = int(ent[0])
        end = int(ent[1])
        label = ent[2]
        if((start == 0 and end == 0) or start == end or start < 0 or end <= 0 or start >= max or end >= max):
            ent.append("invalid")
            print("out of bounds error")

        for tent in td["entities"]:
            tstart = int(tent[0])
            tend = int(tent[1])
            tlabel = tent[2]
            if ((not(start == tstart and end == tend and label == tlabel)) and ((start >= tstart and end <= tend) or (tstart >= start and tend <= end))):
                if(not("invalid" in ent)):
                    ent.append("invalid")
                    print("overlap error")
        if(not("invalid" in ent)):
            ent.append("valid")
        # print(ent)
        ent_text = text[start:end]
        len_ent_text = len(ent_text)
        # print(ent_text,len(ent_text))
        lstriptxt = ent_text.lstrip()
        startchange_val = len_ent_text - len(lstriptxt)
        new_start = start + startchange_val
        rstriptxt = lstriptxt.rstrip()
        endchange_val = len(lstriptxt)-len(rstriptxt)
        new_end = end - endchange_val
        # print(ent_text,len_ent_text,rstriptxt,len(rstriptxt))
        if(len_ent_text>len(rstriptxt)):
            ent[0:2] = [new_start,new_end]
        # print(ent)    
        # text = text.replace(ent_text,rstriptxt)
    print(td["entities"])
    arrays_set = set()
    unique_arrays = []
    for ent in td["entities"]:
        ent_tuple = tuple(ent)
        if ent_tuple not in arrays_set:
            arrays_set.add(ent_tuple)
            unique_arrays.append(ent)
    td["entities"] = unique_arrays
    print(td["entities"])
    nlp = spacy.blank("en")
    db = DocBin()
    skipped = 0
    total = 0
    
    doc = nlp.make_doc(text)
    valid_ents = []
    try:
        for start, end, label,validsts in td["entities"]:
            span = doc.char_span(start,end,label=label,alignment_mode="contract")
            total += 1
            if span is None: #or span.text.startswith(" ") or span.text.endswith(" ") :
                print(f"⚠  Skipping Entity : {text[0:30]}...")
                skipped += 1
            else:
                valid_ents.append(span)
        doc.ents = valid_ents
        db.add(doc)
    except Exception as ex:
        print("⚠ ", ex)
        skipped += 1
    if(i<=60):
        db.to_disk(f"data/trained_data.spacy")
    else:
        db.to_disk(f"data/development_data.spacy")

    if(i>100):
        break
    i+=1 
    


   




    
        
    

        

         

      
       



          




      
        





 

  
