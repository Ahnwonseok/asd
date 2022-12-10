from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.ozvefus.mongodb.net/Clurster0?retryWrites=true&w=majority')
db = client.dbsparta

#데이터넣기
doc = {
    'name':'bob',
    'age':27
}
db.users.insert_one()

#데이터 전부 찾기
all_users = list(db.users.find({},{'_id':False}))

for user in all_users:
    print(user)

#조건에 맞는 데이터 찾기
user = db.users.find_one({'name':'bob'},{'_id':False})
print(user['age'])

#데이터 수정하기
db.users.update_one({'name':'bob'},{'$set':{'age':19}}) #name이 bob인 나이를 19로 수정

#데이터 삭제
db.users.delete_one({'name':'bob'})
