from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.ozvefus.mongodb.net/Clurster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html') #HTML파일 불러옴

@app.route("/homework", methods=["POST"])
def homework_post():
    com_receive = request.form['comment_give'] #클->서
    nic_receive = request.form['nickname_give']

    if com_receive == '0':
        del_receive = request.form['del_give']
        print(del_receive)
        db.comments.delete_many({"nic" : del_receive})
        return jsonify({'msg': '삭제 완료'})

    doc = {
        'nic': nic_receive,
        'comment': com_receive
    }
    db.comments.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


@app.route("/homework", methods=["GET"])
def homework_get():
    comments = list(db.comments.find({}, {'_id': False})) #db의 전체 데이터를 찾음
    return jsonify({'comments':comments}) #comments라는 이름으로 데이터를 전송

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

