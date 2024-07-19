from flask import Flask, jsonify,request
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Karsah_2104'
app.config['MYSQL_DB'] = 'contact_app'
app.config['PORT'] = 3306
mysql = MySQL(app)


@app.route('/users', methods=['GET'])
def login():
    try:
        email = request.args.get('email')
        password = request.args.get('password')
        mycursor = mysql.connection.cursor()
        sql = "SELECT UserPassword,UserID FROM WHERE UserEmail = %s"
        val = (email,)
        mycursor.execute(sql,val)
        response = mycursor.fetchone()

        if(password == response[0]) :
            return jsonify({'status': 'Login Successful','id' : response[1]}),200
        else:
            return jsonify('Login Failed'), 400

    except Exception as e:
        print(e)
        return jsonify('An error has occured'),500


@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if data is None:
            return jsonify('No data provided'), 400

        email = request.json['email']
        password = request.json['password']

        if not email or not password:
            return jsonify('Missing required fields'), 400

        mycursor = mysql.connection.cursor()
        sql = "SELECT * FROM users WHERE UserEmail = %s"
        val = (email,)
        mycursor.execute(sql, val)
        if mycursor.fetchone():
            return jsonify('Email already exists'), 400

        sql = "INSERT INTO users (UserEmail, UserPassword) VALUES (%s, %s)"
        val = (email,password)
        mycursor.execute(sql, val)
        mysql.connection.commit()

        sql = "SELECT UserID FROM users WHERE UserEmail = %s"
        val = (email,)
        mycursor.execute(sql,val)
        id = mycursor.fetchone()
        return jsonify('User created successfully'), 201

    except Exception as e:
        return jsonify('An error has occured'),500


@app.route('/contacts',methods = ['POST'])
def create_contact():
    try:
        data = request.get_json()

        if data is None:
            return jsonify('No data provided'), 400
        name = request.json['name']
        email = request.json['email']
        phoneNo = request.json['phoneNo']
        userID = request.json['userID']

        if not name or not phoneNo or not userID:
            return jsonify('Missing required fields'), 400

        mycursor = mysql.connection.cursor()
        sql = "SELECT * FROM contacts WHERE ContactPhone = %s AND UserID = %s"
        val = (phoneNo,userID,)
        mycursor.execute(sql, val)
        if mycursor.fetchone():
            return jsonify('Contact already exists'), 400


        sql = "INSERT INTO contacts (ContactName, ContactEmail, ContactPhone,UserID) VALUES (%s, %s,%s,%s)"
        val = (name,email,phoneNo,userID,)
        print('pass1')
        print(userID)
        mycursor.execute(sql, val)
        print('pass')
        mysql.connection.commit()
        return jsonify('Contact added successfully'), 201
    except Exception as e:
        print(e)
        return jsonify('An error has occured'),500




@app.route('/contacts/<int:id>', methods = ['GET'])
def getAllContacts (id):
    try:
        mycursor = mysql.connection.cursor()
        sql = "SELECT ContactID,ContactName,ContactEmail,ContactPhone FROM contacts WHERE UserID = %s"
        val = (id,)
        mycursor.execute(sql,val)
        response = mycursor.fetchall()
        return jsonify(response),200
    except Exception as e:
        return ('An error has occured'),500


@app.route('/contacts/<int:id>' , methods =['DELETE'])
def deleteContact(id):
    try:
        mycursor = mysql.connection.cursor()
        sql = "DELETE FROM contacts WHERE ContactID = %s"
        val = (id,)
        mycursor.execute(sql,val)
        mysql.connection.commit()
        return jsonify('Contact sucessfully deleted!'),204
    except Exception as e:
        return jsonify('An error has occured')

@app.route('/contacts/<int:id>',methods=['PUT'])
def updateContact(id) :
    try:
        mycursor = mysql.connection.cursor()

        name = request.json['name']
        phoneNo = request.json['phoneNo']
        email = request.json['email']

        sql = "UPDATE contacts SET ContactName = %s , ContactPhone = %s, ContactEmail = %s WHERE ContactID = %s"
        val = (name,phoneNo,email,id,)
        mycursor.execute(sql,val)
        mysql.connection.commit()
        return jsonify('Contact updated Sucessfully')
    except Exception as e:
        print(e)

        return jsonify('An error has ooccured')


if __name__ == '__main__':
    app.run(debug=True)
