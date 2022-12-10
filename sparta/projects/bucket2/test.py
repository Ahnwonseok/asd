from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.ozvefus.mongodb.net/Clurster0?retryWrites=true&w=majority')
db = client.dbsparta

doc = [{'name': '마늘','num': 50},
       {'name': '양파','num': 50},
       {'name': '대파','num': 50},
       {'name': '소금','num': 50},
       {'name': '설탕','num': 50}]

db.ingredient.insert_many(doc)