# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import numpy as np
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ishita1234'
app.config['MYSQL_DB'] = 'mini_project1'

mysql = MySQL(app)

@app.route('/')

@app.route('/home')
def home():
    return render_template('home.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            #msg = 'Logged in successfully !'
            return render_template('index.html')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


#@app.route('/index')

@app.route('/predict', methods=['POST'])
def predict():
    # Put all form entries values in a list
    features = [float(i) for i in request.form.values()]
    # Convert features to array
    array_features = [np.array(features)]
    # Predict features
    prediction = model.predict(array_features)

    output = prediction

    # Check the output values and retrive the result with html tag based on the value
    if output == 1:
        return render_template('index.html', result='The patient is not likely to have heart disease!')
    else:
        return render_template('Sym.html', result='The patient is likely to have heart disease!')

@app.route('/symptoms', methods=['GET', 'POST'])
def symptoms():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        ss1 = request.form.get("S1")
        # getting input with name = lname in HTML form
        ss2 = request.form.get("S2")
        ss3 = request.form.get("S3")
        ss4 = request.form.get("S4")
        ss5 = request.form.get("S5")
        ss6 = request.form.get("S6")
        x = [ss1,ss2,ss3,ss4,ss5,ss6]

        test_list = [ ['Lightheadedness', 'racing heartbeat', 'slow pulse', 'Dizziness', 'chest pain'] ,
                      ['coldness', 'numbness', 'pain', 'weakness'],
                      ['chest pain', 'Coughing', 'Fever', 'skin rash', 'Dizziness'],
                      ['Shortness of breath', 'weakness', 'Swelling', 'Irregular heartbeat', 'Reduced ability to exercise'],
                      ['Chest pain', 'weakness', 'Pain', 'Shortness of breath'],
                      ['bluish tint', 'Fast breathing', 'Poor weight gain', 'Lung infections', 'Reduced ability to exercise'],
                      ['weakness', 'trouble speaking', 'trouble seeing', 'dizziness'],
                      ['bluish tint', 'Irregular heartbeat', 'Swelling', 'shortness of breath', 'fatigue'],
                      ['Swelling', 'Breathlessness', 'coughing', 'Fatigue', 'Irregular heartbeat', 'Dizziness'],
                      ['Shortness of breath', 'Chest pain', 'dizziness', 'Rapid pulse', 'Rapid breathing', 'Coughing up blood'],
                      ['Fatigue', 'Shortness of breath', 'Irregular heartbeat', 'Swelling', 'Chest pain', 'Fainting']
                    ]

        pre = ['1) Have regular checkups 2) Do Medications 3) Eating a healthful, balanced, low-fat diet 4) Limiting or avoiding substances that contribute to abnormal heart rhythm 5) Exercise regularly',
               '1) Stop smoking  2) Exercise regularly 3) Maintain a healthy weight 4) Eat healthy foods 5) Manage stress',
               '1) Quit smoking 2) Keep check and control the cholesterol levels 3) Exercise regularly 4) Eat healthy foods 5) Get proper sleep 6) Control the blood sugar level',
               '1) Stick to a healthy weight 2) Exercise regularly 3) Eat healthy foods 4) Avoiding smoke or use recreational drugs 5) Reduce your stress 6) Get enough sleep.',
               '1) Exercise regularly 2) Eat healthy foods 3) Avoiding smoking 4) Manage stress',
               '1) Stop smoking  2) Exercise regularly 3) Maintain a healthy weight 4) Eat healthy foods 5) Manage stress',
               '1) Exercise more 2) Lose weight 3) Do not drink alcohol 4) Treat diabetes 5) Quit smoking',
               '1) Ensure your blood sugar levels are under control 2) Vaccinated against rubella & flu 3) Avoid drinking alcohol and using illegal drugs 4) Exercise more',
               '1) Quitting smoking 2) Losing excess weight 3) Avoiding alcohol & illegal drugs 4) Getting enough sleep and rest 5) Reducing stress',
               '1) Stop smoking  2) Exercise regularly 3) Maintain a healthy weight 4) Eat healthy foods 5) Manage stress',
               '1) Getting regular physical activity 2) Maintaining a healthy weight 3) Eating a heart-healthy diet 4) Managing stress']

        d = ['Arrhythmias', 'Atherosclerosis', 'Heart infections', 'Heart failure', 'Heart attack',
             'Heart problems at birth', 'Stoke', 'Congenital heart disease', 'Heart muscle disease (Cardiomyopathy)',
             'Pulmonary embolism', 'valvular heart disease']

        covid = ['Fever', 'Coughing', 'Fatigue', 'Loss of taste or smell', 'Nasal congestion', 'Conjunctivitis',
                 'Sore throat', 'Headache', 'pain', 'Skin rash', 'vomiting', 'Diarrhea', 'Dizziness']

        def intersection(x, test_list):
            inter = [list(filter(lambda a: a in x, sublist)) for sublist in test_list]
            return inter

        det = intersection(x, test_list)
        y = [len(q) for q in det]
        dis=[ ]
        pre1=[ ]
        for i in range(len(y) - 1):
            if (y[i] >= 3):
                dis.append(d[i])
                pre1.append(pre[i])
                #msgdis = "Disease user might be facing: "
            #else:
                #msgdis = " "

        msgdis = "Disease user might be facing: "

        def listToString(s):
            str1 = ""
            for ele in s:
                str1 += " , " + ele
            str1 = "\n"+ str1
            return str1

        disease=listToString(dis)
        pre2=listToString(pre1)
        msg = msgdis + disease

        def inter_covid(x, covid):
            inter1 = [value for value in x if value in covid]
            return inter1

        det1 = inter_covid(x, covid)
        covidmsg = listToString(det1)
        if (len(det1) >= 3):
            msg11="Possibility of Covid, due to the symptoms:\n" + covidmsg
            #print(det1)
        else:
            msg11=" Congratulation! Not possibility of Covid"

        return render_template("Sym.html" , result1= msg, result2 = msg11, result3 = pre2, result='The patient is likely to have heart disease!')