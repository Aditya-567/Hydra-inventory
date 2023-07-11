# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 16:39:56 2020

@author: hp
"""

from flask import Flask, render_template, request
import key_config as keys
import boto3
import requests
from werkzeug.utils import secure_filename

BUCKET_NAME='empbuk'

app = Flask(__name__)

x=''
dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    region_name=keys.AWS_DEFAULT_REGION)

s3 = boto3.client('s3',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    region_name=keys.AWS_DEFAULT_REGION)

from boto3.dynamodb.conditions import Key, Attr


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
        GST1 = request.form['GST1']
        Address = request.form['Address']
        
        global x
        x =name

        table = dynamodb.Table('users')
        
        table.put_item(
                Item={
        'name': name,
        'email': email,
        'password': password,
        'password2' : password2,
        'GST1' : GST1,
        'Address' : Address
            }
        )
        
        img = request.files['file']
        if img:
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )
        msg = "Registration Complete. Please Login to your account !"
    
        return render_template('login1.html',msg = msg)
    return render_template('signup.html')



@app.route('/check',methods=['GET', 'POST'])
def check():
    if request.method=='POST':
        
        email = request.form['email']
        password = request.form['password']
        

        table = dynamodb.Table('users')
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
        items = response['Items']
        name = items[0]['name']
        print(items[0]['password'])
        if password == items[0]['password']:
            
            return render_template("dashbord2.html",name = name)
    return render_template("login1.html")


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('homepage.html')


@app.route('/dash', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        #verify if the file is valid
        #here invoke js to do something (for example flash("test"))
        return render_template('hex1.html', flash_message="True")

    return render_template('hex1.html', flash_message="False")

@app.route('/product', methods=['GET', 'POST'])
def product():
    
    userdata=x + 'table'
    if request.method=='POST':
            #tablecreate()
            product1 = request.form['product1']
            quantity1 = request.form['quantity1']
            producttable = dynamodb.Table("table")
        
            producttable.put_item(
            Item={
            'product1'   : product1,
            'quantity1'  : quantity1,
                }
            )
            msg = "Item added"
            return render_template('dashbord2.html', flash_message=True , msg=msg)
    return render_template('product.html', flash_message=False)

userdata=x + 'table'
def tablecreate():

        table2 = dynamodb.create_table(
        TableName=userdata,
        KeySchema=[
            {
                'AttributeName': 'product1', 'KeyType': 'HASH'
            },
            {
                'AttributeName': 'quantity1', 'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'product1', 'AttributeType': 'S'
            },
            {
                'AttributeName': 'quantity1', 'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
        )
        
        table2.meta.client.get_waiter('table_exists').wait(TableName=userdata)
        
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        table = dynamodb.Table(userdata)
        
        minquantity = request.form['minquantity']
        
        table.put_item(
                Item={
        'minquantity': minquantity

            }
        )
        return render_template('min.html', flash_message=True)
        
@app.route('/display')
def test_route():

    # Get the table
    table = dynamodb.Table(userdata)

    # Query the table to get all items
    response = table.scan()

    # Get the items from the response
    items = response['Items']

    # Render the template with the items
    return render_template('table.html', items=items)

@app.route('/subscription', methods=['GET', 'POST'])
def sub():
    return render_template('bill.html')

@app.route('/payment1', methods=['GET', 'POST'])
def pay1():
    table = dynamodb.Table('users')

    response = table.scan()

    items = response['Items']

    return render_template('payment.html',items=items)

@app.route('/payment2', methods=['GET', 'POST'])
def pay2():
    table = dynamodb.Table('users')

    response = table.scan()

    items = response['Items']

    return render_template('payment1.html',items=items)

@app.route('/payment3', methods=['GET', 'POST'])
def pay3():
    table = dynamodb.Table('users')

    response = table.scan()

    items = response['Items']

    return render_template('payment2.html',items=items)


@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )
                msg = "Upload Done ! "

    return render_template("file_upload_to_s3.html",msg =msg)


if __name__ == "__main__":
    
   app.run(host='0.0.0.0', port=80, debug=True)

