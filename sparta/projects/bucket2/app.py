from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.ozvefus.mongodb.net/Clurster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["GET"])
def bucket_get():
    menu_list = list(db.menu.find({}, {'_id': False}))
    ingredient_list = list(db.ingredient.find({}, {'_id': False}))

    return jsonify({'menu': menu_list,'ingredient': ingredient_list})

@app.route("/bucket", methods=["POST"])
def bucket_post():
    menu_receive = request.form['menu_give']
    day_receive = request.form['day_give']

    Menu=['김치찌개','동태찌개','부대찌개','청국장']
    Week =['월','화','수','목','금','토','일']

    if menu_receive not in Menu:
        return jsonify({'msg': '메뉴에 없는 음식입니다. 다시 입력하세요'})

    if day_receive not in Week:
        return jsonify({'msg': '요일을 잘못 입력하셨습니다. 다시 입력하세요'})

    menu_list = list(db.menu.find({'name':menu_receive}, {'_id': False}))
    # count = len(bucket_list)+1
    print(menu_list)

    if len(menu_list)==0:

        days = {'월':0, '화':0, '수':0, '목':0, '금':0, '토':0, '일':0}

        for day in days.keys():
            if day == day_receive:
                days[day] = days[day] + 1
                break

        doc = {
            'name': menu_receive,
            'Day': days,
            'num': 1
        }

        db.menu.insert_one(doc)

    else:
        Foods={'김치찌개': ['마늘','양파','대파','소금'],'청국장': ['양파','대파'],
              '부대찌개': ['마늘','소금'],'동태찌개': ['소금']}

        for ingre in Foods[menu_receive]:

            find_ingre = list(db.ingredient.find({'name': ingre}, {'_id': False}))
            new_num = int(find_ingre[0]['num']) - 1

            db.ingredient.update_one({'name': ingre}, {'$set': {'num': new_num}})

        menu = list(db.menu.find({'name': menu_receive}, {'_id': False}))
        new_num = int(menu[0]['num']) + 1
        day_dic = menu[0]['Day']

        for day in day_dic.keys():
            if day == day_receive:
                day_dic[day] = day_dic[day] + 1
                break

        db.menu.update_one({'name': menu_receive}, {'$set': {'num':new_num}})
        db.menu.update_one({'name': menu_receive}, {'$set': {'Day': day_dic}})

    return jsonify({'msg': '등록완료'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}}) #클라에서 넘어온 숫자는 모두 문자

    return jsonify({'msg': '버킷완료'})

@app.route("/bucket/del", methods=["POST"])
def bucket_del():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'del': 1}})  # 클라에서 넘어온 숫자는 모두 문자

    return jsonify({'msg': '삭제완료'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)