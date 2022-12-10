from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.ozvefus.mongodb.net/Clurster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def dashboard():
    return render_template('index.html')

@app.route("/index/net", methods=["GET"])
def bucket_get():
    #음식의 모든 정보를 html로 넘겨준다
    food_list = list(db.menu.find({}, {'_id': False}))
    #재료의 모든 정보를 html로 넘겨준다
    ingredient_list = list(db.ingredient.find({}, {'_id': False}))

    return jsonify({'menu': food_list, 'ingredient': ingredient_list})

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/blank.html')
def blank():
    return render_template('blank.html')

@app.route('/buttons.html')
def buttons():
    return render_template('buttons.html')

@app.route('/cards.html')
def cards():
    return render_template('cards.html')

@app.route('/charts.html')
def charts():
    return render_template('charts.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/tables.html')
def tables():
    return render_template('tables.html')

@app.route('/utilities-animation.html')
def animation():
    return render_template('utilities-animation.html')

@app.route('/utilities-border.html')
def border():
    return render_template('utilities-border.html')

@app.route('/utilities-color.html')
def color():
    return render_template('utilities-color.html')

@app.route('/utilities-other.html')
def other():
    return render_template('utilities-other.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)