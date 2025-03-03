import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask,redirect,url_for,render_template,request,jsonify

from pymongo import MongoClient
import requests
from bson import ObjectId
from werkzeug.utils import secure_filename

from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app=Flask(__name__)
@app.route('/',methods=['GET'])
def home():
    fruit=list(db.fruit.find({}))
        # Handle POST Request here
    return render_template('dashboard.html', fruit=fruit)



@app.route('/fruit',methods=['GET','POST'])
def fruit():
    fruit=list(db.fruit.find({}))
    print(fruit)
    return render_template('fruit.html', fruit=fruit)


@app.route('/Addfruit',methods=['GET','POST'])
def Addfruit():
    if request.method=='POST':
        nama=request.form['nama']
        harga=request.form['harga']
        deskripsi=request.form['deskripsi']

        gambar=request.files['gambar']
        extension=gambar.filename.split('.')[-1]
        today=datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
        gambar_name=f"{mytime}.{extension}"
        save_to=f'static/imgFruit/{gambar_name}'
        gambar.save(save_to)

        doc={
            'nama':nama,
            'harga':harga,
            'deskripsi':deskripsi,
            'gambar':gambar_name
        }
        db.fruit.insert_one(doc)



        # Handle POST Request here
        return redirect(url_for('fruit'))
    return render_template('Addfruit.html')


@app.route('/Editfruit/<_id>',methods=['GET','POST'])
def Editfruit(_id):
    if request.method=='POST':
        nama=request.form['nama']
        harga=request.form['harga']
        deskripsi=request.form['deskripsi']

        gambar=request.files['gambar']
        extension=gambar.filename.split('.')[-1]
        today=datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
        gambar_name=f"{mytime}.{extension}"
        save_to=f'static/imgFruit/{gambar_name}'
        gambar.save(save_to)

        doc={
            'nama':nama,
            'harga':harga,
            'deskripsi':deskripsi,
        }

        if gambar_name:
            doc['gambar']=gambar_name 
        db.fruit.update_one({'_id':ObjectId(_id)},{'$set':doc})



        # Handle POST Request here
        return redirect(url_for('fruit'))
        # Handle POST Request here
        return render_template('index.html')
    id=ObjectId(_id)
    data = list(db.fruit.find({'_id': id}))
    return render_template('Editfruit.html',data=data)




@app.route('/Deletefruit/<_id>',methods=['GET','POST'])
def Deletefruit(_id):
    id=ObjectId(_id)
    db.fruit.delete_one({'_id':id})
    return redirect(url_for('fruit'))



if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run('0.0.0.0',port=5000,debug=True)