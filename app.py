from flask import Flask, request, render_template, redirect, flash
from flask_mysqldb import MySQL
import random

import config

app = Flask(__name__)
app.secret_key = "secret"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ibills'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def HomeScreen():
    return render_template('HomeScreen.html')

@app.route('/AboutScreen')
def AboutScreen():
    return render_template('AboutScreen.html')

@app.route('/ServicesScreen')
def ServicesScreen():
    return render_template('ServicesScreen.html')

@app.route('/ContactsScreen')
def ContactsScreen():
    return render_template('ContactsScreen.html')

@app.route('/SignUpScreen', methods=['GET', 'POST'])
def SignUpScreen():
    if(request.method == "POST"):
        username = request.form['username']
        password = request.form['password']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        birthday = request.form['birthday']
        contactNo = request.form['contactNo']
        emailAddress = request.form['emailAddress']
        address = request.form['address']

        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM users")
        mysql.connection.commit()
        cur.close()
        
        noSimilarAccount = True
        for row in cur:
            if("{username}".format(username=row['username']) == username):
                noSimilarAccount = False

        if(noSimilarAccount):
            randomValue = random.randint(101, 999)
            #This is an INSERT QUERY
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (id,username,password,firstName,lastName,birthday,contactNo,emailAddress,address, type) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)", (randomValue, username, password, firstName, lastName, birthday, contactNo, emailAddress, address, "user"))
            mysql.connection.commit()
            cur.close()

            return redirect('/AccountSuccessfullyCreated')
        else:
            flash("Username is already taken!")

    return render_template('SignUpScreen.html')
    
@app.route('/AccountSuccessfullyCreated')
def AccountSuccessfullyCreated():
    return render_template('AccountSuccessfullyCreatedScreen.html')

@app.route('/SignInScreen', methods=['GET', 'POST'])
def SignInScreen():
    config.currentlyLoggedIn = ""
    config.currentlyLoggedInFirstName = ""
    config.currentlyLoggedInLastName = ""
    config.currentlyLoggedInUserID = 0

    if(request.method == "POST"):

        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        results = cur.execute("SELECT * FROM users")
        mysql.connection.commit()
        cur.close()
        if not results:
            flash("There are no registered users!")
        else:
            wrongdetails = False
            for row in cur:
                if("{username}".format(username=row['username']) == username):
                    if("{password}".format(password=row['password']) == password):
                        wrongdetails = False
                        break
                    else:
                        wrongdetails = True
                else:
                    wrongdetails = True

        if(wrongdetails):
            flash("Incorrect Login Details!")
        else:
            if("{type}".format(type=row['type']) == "user"):
                config.currentlyLoggedInUsername = username
                return redirect('/MainMenuScreen')
            elif("{type}".format(type=row['type']) == "billprovider"):
                config.currentlyLoggedInUsername = username
                return redirect('/BillProviderMainMenuScreen')
            else:
                config.currentlyLoggedInUsername = username
                return redirect('/AdminScreen')


    return render_template('SignInScreen.html')

@app.route('/MainMenuScreen')
def MainMenuScreen():
    sum=0
    billProvider2=""

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username=" + "'" + config.currentlyLoggedInUsername + "'")
    config.currentlyLoggedInData = cur.fetchone()

    numberOfBills = cur.execute("SELECT * FROM bills WHERE userUsername=" + "'" + config.currentlyLoggedInUsername + "'" + "AND paid='No'")
    getBillsOfCurrentlyLoggedIn = cur.fetchall()

    for row in cur:
        sum += int("{billAmount}".format(billAmount=row['billAmount']))
    
    cur.execute("SELECT * FROM bills WHERE userUsername=" + "'" + config.currentlyLoggedInUsername + "'" + " AND paid='No' ORDER BY dateDue")
    nearDeadline = cur.fetchone()
    print(nearDeadline)
    if(nearDeadline):
        cur.execute("SELECT * FROM users WHERE username=" + "'" + nearDeadline['billerUsername'] + "'")
        billProvider2 = cur.fetchone()
        print("asdasdadasda")

    numberOfBills2 = cur.execute("SELECT * FROM bills WHERE userUsername=" + "'" + config.currentlyLoggedInUsername + "'" + " AND paid='Yes'" )
    getPaidBillsOfCurrentlyLoggedIn = cur.fetchall()

    mysql.connection.commit()
    cur.close()

    return render_template('MainMenuScreen.html', currentlyLoggedIn=config.currentlyLoggedInData, bills=getBillsOfCurrentlyLoggedIn, totalBillsSum=sum, billNearDeadline=nearDeadline, billProvider2=billProvider2, numberOfBills=numberOfBills, numberOfBills2=numberOfBills2, bills2=getPaidBillsOfCurrentlyLoggedIn)

@app.route('/ProfileScreen', methods=['GET', 'POST'])
def ProfileScreen():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username=" + "'" + config.currentlyLoggedInUsername + "'")
    config.currentlyLoggedInData = cur.fetchone()

    mysql.connection.commit()
    cur.close()

    if(request.method == "POST"):
        
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        contactNo = request.form['contactNo']
        emailAddress = request.form['emailAddress']
        birthday = request.form['birthday']
        address = request.form['address']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        if(password == confirmPassword):
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET firstName='" + firstName + "'," + "lastName='" + lastName + "'," + "contactNo='" + contactNo + "'," + "emailAddress='" + emailAddress + "'," + "birthday='" + birthday + "'," + "address='" + address + "'," + "password='" + password + "'" + "WHERE username='" + config.currentlyLoggedInUsername + "'")
            mysql.connection.commit()
            cur.close()
            
            return redirect('/ProfileScreen')
        else:
            flash("Password is not the same!")

    return render_template('ProfileScreen.html', currentlyLoggedIn=config.currentlyLoggedInData)

@app.route('/PaymentOptionsScreen')
def PaymentOptionsScreen():
    return render_template('PaymentOptionsScreen.html', currentlyLoggedIn=config.currentlyLoggedInData)

@app.route('/BillingDetailsScreen', methods=['GET', 'POST'])
def BillingDetailsScreen():
    referenceNo = request.form['refNumber']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bills WHERE referenceNo=" + "'" + referenceNo + "'")
    billDetails = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE username=" + "'" + billDetails['billerUsername'] + "'")
    billProvider = cur.fetchone()
    mysql.connection.commit()
    cur.close()

    return render_template('BillingDetailsScreen.html', billDetails=billDetails, billProvider=billProvider, firstName=config.currentlyLoggedInFirstName, lastName=config.currentlyLoggedInLastName, userID=config.currentlyLoggedInUserID)

@app.route('/BillingDetailsScreenPay', methods=['GET', 'POST'])
def BillingDetailsScreenPay():
    referenceNo = request.form['refNumber']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE bills SET paid='Yes'" + "WHERE referenceNo='" + referenceNo + "'")
    mysql.connection.commit()
    cur.close()

    return redirect('/MainMenuScreen')

@app.route('/BillProviderMainMenuScreen')
def BillProviderMainMenuScreen():
    config.username = ""
    config.userID = "0"

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username=" + "'" + config.currentlyLoggedInUsername + "'")
    config.currentlyLoggedInData = cur.fetchone()

    numberOfBills = cur.execute("SELECT * FROM bills WHERE billerUsername=" + "'" + config.currentlyLoggedInUsername + "' AND paid='No'")
    getBillsOfCurrentlyLoggedIn = cur.fetchall()

    getToValidateNumberOfBills = cur.execute("SELECT * FROM bills WHERE billerUsername=" + "'" + config.currentlyLoggedInUsername + "'" " AND paid='Yes' AND validated='No'")

    numberOfBills2 = cur.execute("SELECT * FROM bills WHERE billerUsername=" + "'" + config.currentlyLoggedInUsername + "' AND paid='Yes'")
    getPaidBillsOfCurrentlyLoggedIn = cur.fetchall()

    mysql.connection.commit()
    cur.close()
    
    return render_template('BillProviderMainMenuScreen.html', currentlyLoggedIn=config.currentlyLoggedInData, bills=getBillsOfCurrentlyLoggedIn, numberOfBills=numberOfBills, numberOfBills2=numberOfBills2, getToValidateNumberOfBills=getToValidateNumberOfBills, getPaidBillsOfCurrentlyLoggedIn=getPaidBillsOfCurrentlyLoggedIn)

@app.route('/GenerateBillScreen')
def GenerateBillScreen():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE type='user'")
    getAllUsers = cur.fetchall()

    cur.execute("SELECT * FROM users WHERE username=" + "'" + config.username + "'" "")
    getSelectedUser = cur.fetchall()

    mysql.connection.commit()
    cur.close()

    return render_template('GenerateBillScreen.html', currentlyLoggedIn=config.currentlyLoggedInData, users=getAllUsers, username2=config.username, selectedUser=getSelectedUser)

@app.route('/GenerateBillScreenGetUser', methods=['GET', 'POST'])
def GenerateBillScreenGetUser():
    config.username = ""
    username = request.form['userInput']
    config.username = username
    
    return redirect('GenerateBillScreen')

@app.route('/GenerateBillScreenCreateBill', methods=['GET', 'POST'])
def GenerateBillScreenCreateBill():
    billingPeriodFrom = request.form['inputBillingPeriodFrom']
    billingPeriodTo = request.form['inputBillingPeriodTo']
    billingDue = request.form['inputBillingDue']
    monthlyConsumption = request.form['inputMonthlyConsumption']
    billAmount = request.form['inputBillAmount']

    randomValue = random.randint(10001, 99999)

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO bills (referenceNo, userUsername, billerUsername, billAmount, billingPeriod, billConsumption, dateDue) VALUES (%s,%s,%s,%s,%s,%s,%s)", (randomValue, config.username, config.currentlyLoggedInUsername, billAmount, billingPeriodFrom + " to " + billingPeriodTo, monthlyConsumption, billingDue))
    mysql.connection.commit()
    cur.close()

    flash("Bill Created Successfully!")

    config.username = ""

    return redirect('GenerateBillScreen')

@app.route('/ValidatePaymentsScreen')
def ValidatePaymentsScreen():
    config.username = ""
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bills WHERE billerUsername=" + "'" + config.currentlyLoggedInUsername + "'" " AND paid='Yes' AND validated='No'")
    billDetails = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    return render_template('ValidatePaymentsScreen.html', currentlyLoggedIn=config.currentlyLoggedInData, billDetails=billDetails)

@app.route('/ValidatePaymentsScreenValidate', methods=['GET', 'POST'])
def ValidatePaymentsScreenValidate():
    referenceNo = request.form['refNumber']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE bills SET validated='Yes'" + "WHERE referenceNo='" + referenceNo + "'")
    mysql.connection.commit()
    cur.close()

    flash("Validated Bill Successfully!")

    return redirect('/ValidatePaymentsScreen')

@app.route('/AdminScreen')
def AdminScreen():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM users WHERE type='user'")
    getAllUsers = cur.fetchall()

    cur.execute("SELECT * FROM users WHERE type='billprovider'")
    getAllBillProviders = cur.fetchall()

    mysql.connection.commit()
    cur.close()

    return render_template('AdminScreen.html', getAllUsers=getAllUsers, getAllBillProviders=getAllBillProviders)

@app.route('/AdminScreenRemoveUser', methods=['GET', 'POST'])
def AdminScreenRemoveUser():

    userID = request.form['accId']
    
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id='" + userID + "'")
    mysql.connection.commit()
    cur.close()

    flash("Successfully Removed User!")

    return redirect('/AdminScreen')

@app.route('/AdminScreenRemoveBillProvider', methods=['GET', 'POST'])
def AdminScreenRemoveBillProvider():

    billerId = request.form['billerId']
    
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id='" + billerId + "'")
    mysql.connection.commit()
    cur.close()

    flash("Successfully Removed Bill Provider!")

    return redirect('/AdminScreen')

@app.route('/CreateBillProviderScreen', methods=['GET', 'POST'])
def CreateBillProviderScreen():
    if(request.method == "POST"):
        username = request.form['usernameInput']
        password = request.form['passwordInput']
        confirmPassword = request.form['confirmPasswordInput']
        companyName = request.form['companyNameInput']
        service = request.form['serviceInput']

        if(password == confirmPassword):
            randomValue = random.randint(1, 99)
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (id,username,password,billerName,typeOfService,type) VALUES (%s,%s,%s,%s,%s,%s)", (randomValue, username, password, companyName, service, "billprovider"))
            mysql.connection.commit()
            cur.close()
            
            return redirect('/AdminScreen')
        else:
            flash("Password is not the same!")

    return render_template('CreateBillProviderScreen.html')



app.run(debug=True)