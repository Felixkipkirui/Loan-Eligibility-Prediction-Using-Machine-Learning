from flask import Flask, render_template, request, redirect, url_for, session, json, jsonify,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
#import mysql.connector
import random
import string
from werkzeug.utils import secure_filename
import os
#from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from flask import flash
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.feature_selection import f_classif

app = Flask(__name__)


app.secret_key = '123456789'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'fkl@2030'
app.config['MYSQL_DB'] = 'binex'

mysql = MySQL(app)

# The route() function of the Flask class is a decorator, 
@app.route('/')
def landing():
	return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    
    if request.method == 'POST' and 'id' in request.form and 'password' in request.form:

        id = request.form['id']
        password = request.form['password']

        #print(request.form)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE ID_Number = %s AND Password = %s', (id, password))
        account = cursor.fetchone()

        print("Acount:", account)
        if account:
            session['loggedin'] = True
            session['CustomerID'] = account['CustomerID']
            session['name'] = account['Name']
            session['id'] = account['ID_Number']
            session['address'] = account['Address']
            session['email'] = account['Email']
            session['contact'] = account['Contact']
            session['username'] = account['Username']
            session['annual'] = account['AnnualIncome']
            session['salary'] = account['MonthlyInhandSalary']
            session['acc'] = account['NumberOfAcc']
            session['card'] = account['NumberOfCards']
            session['loans'] = account['NoOfLoans']
            session['avg'] = account['AvgDaysDelayed']
            session['delayed'] = account['DelayedPayment']
            session['debt'] = account['OutstandingDebt']
            session['age'] = account['CreditHistoryAge']
            session['monthly'] = account['MonthlyBalance']
            # Redirect to home page
            return redirect(url_for('dashboard'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('customerID', None)
   session.pop('name', None)
   session.pop('id', None)
   session.pop('address', None)
   session.pop('email', None)
   session.pop('contact', None)
   session.pop('username', None)
   
   return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/form', methods=['GET'])
def form():
    if 'loggedin' in session:
        return render_template('form.html')
    return redirect(url_for('login'))

# Load the pre-trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)


@app.route('/predict', methods=['POST'])
def predict():
    
    # Get the input features from the form
    annual_income = float(request.form['annual_income'])
    monthly_salary = float(request.form['monthly_salary'])
    num_bank_accounts = float(request.form['num_bank_accounts'])
    num_credit_cards = float(request.form['num_credit_cards'])
    interest_rate = float(request.form['interest_rate'])
    num_loans = float(request.form['num_loans'])
    avg_days_delayed = float(request.form['avg_days_delayed'])
    num_delayed_payments = float(request.form['num_delayed_payments'])
    credit_mix = float(request.form['credit_mix'])
    outstanding_debt = float(request.form['outstanding_debt'])
    credit_history_age = float(request.form['credit_history_age'])
    monthly_balance = float(request.form['monthly_balance'])

    # Create a feature array
    features = np.array([[annual_income, monthly_salary, num_bank_accounts,
                          num_credit_cards, interest_rate, num_loans,
                          avg_days_delayed, num_delayed_payments, credit_mix,
                          outstanding_debt, credit_history_age, monthly_balance]])

    # Make the prediction
    prediction = model.predict(features)[0]

    # Determine the message based on the prediction
    if prediction == 'Poor':
        popup_type = 'Poor'
        popup_message = "You are not eligible for a loan."
        #msg = 'hello'
        
    elif prediction == 'Standard':
        popup_type = 'Standard'
        popup_message = "You are eligible for a loan. Please proceed with the application process."
        #msg = 'hello'
       
    else:
        popup_type = 'Good'
        popup_message = "You are eligible for a loan. Please proceed with the application process."
        #msg = 'hello'
       
   
    return jsonify({'popup_type': popup_type, 'popup_message': popup_message})
    #return render_template('success.html', msg=msg)

@app.route('/faq')
def faq():
    if 'loggedin' in session:
        
        return render_template('faq.html')
    return redirect(url_for('login'))

@app.route('/howitworks')
def howitworks():
    if 'loggedin' in session:
        
        return render_template('howitworks.html')
    return redirect(url_for('login'))


@app.route('/contact-us')
def contactus():
    if 'loggedin' in session:
        
        return render_template('contact.html')
    return redirect(url_for('login'))

@app.route('/terms')
def terms():
    if 'loggedin' in session:
        
        return render_template('terms.html')
    return redirect(url_for('login'))

@app.route('/success')
def success():
    if 'loggedin' in session:
        
        return render_template('success.html')
    return redirect(url_for('login'))

@app.route('/failure')
def failure():
    if 'loggedin' in session:
        
        return render_template('failure.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug=True)
