from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.ozvefus.mongodb.net/Clurster0?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    com_receive = request.form['com_give']
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']

    #크롤링
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    image = og_image['content']
    title = og_title['content']
    description = og_description['content']

    bucket_list = list(db.comment.find({}, {'_id': False}))
    count = len(bucket_list)+1

    #db저장
    doc = {
        'num': count,
        'del': 0,
        'image':image,
        'title':title,
        'desc':description,
        'star':star_receive,
        'comment':com_receive
    }

    db.comment.insert_one(doc)

    return jsonify({'msg':'저장완료'})

@app.route("/movie/del", methods=["POST"])
def bucket_del():
    num_receive = request.form['num_give']
    db.comment.update_one({'num': int(num_receive)}, {'$set': {'del': 1}})  # 클라에서 넘어온 숫자는 모두 문자

    return jsonify({'msg': '삭제완료'})

@app.route("/movie", methods=["GET"])
def movie_get():
    comments = list(db.comment.find({}, {'_id': False})) #db의 전체 데이터를 찾음

    return jsonify({'comments':comments}) #comments라는 이름으로 데이터를 전송

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)