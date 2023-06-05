from flask import Flask, render_template, request, session, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_mail import Mail,Message
from twilio.rest import Client
from werkzeug.utils import secure_filename
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
from io import BytesIO
from flask_babel import Babel
import secrets 
import urllib
import json
import io
import base64
import os
import random
import cloudinary

token2 = secrets.token_hex(9) 
current_datetime=datetime.now()
str_date = current_datetime.strftime("%d-%m-%Y")


def otp_sys():
    otp = ""
    for i in range(6):
        otp += str(random.randint(0, 9))
    return otp


def Indexsss():
    result = db.session.query(
        customer.ptype,
        func.avg(customer.rate).label('avg_rate'),
        func.min(customer.rate).label('min_rate'),
        func.max(customer.rate).label('max_rate'),
        func.max(customer.sno).label('last_rate')
       ).group_by(customer.ptype).all()

    for row in result:
        product1 = product.query.filter_by(name=row.ptype).first()
        prc = customer.query.filter_by(sno=row.last_rate).first()
        if product1:
            product1.average = row.avg_rate
            product1.minimum = row.min_rate
            product1.maximum = row.max_rate
            product1.curr_price = prc.rate
        else:
            product1 = product(
                name=row.ptype,
                average=row.avg_rate,
                minimum=row.min_rate,
                maximum=row.max_rate,
                curr_price = prc.rate,
            )
            db.session.add(product)
    db.session.commit()

def final_price(weight,rate):
    charge = 20 * weight
    finalamt = (weight*rate) - charge
    return finalamt

otp = otp_sys()

def sms_send(mobile):
    account_sid = 'ACc0d050cdc292ff33a1dc453617664fd2'
    auth_token = '91ae15678e36e183dfee52965e3f9fb8'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    body=otp,
    from_=+13612736162,
    to='+91{}'.format(str(mobile))
    )
    print(message.sid)


app = Flask(__name__)
babel = Babel(app)

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app.secret_key = "super-secret-key"
cloudinary.config( 
  cloud_name = "dfrtu63wr", 
  api_key = "893282433118986", 
  api_secret = "ne6HENwALDfZgt8tiSKqQjXfKjM" 
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market1.sqlite'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
app.config['UPLOAD_FILE'] = params['image_uploder']
db = SQLAlchemy(app)
app.app_context().push()
mail = Mail(app)


app.config.update(dict(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'krishnakabra04@gmail.com',
    MAIL_PASSWORD = 'Santosh@123',
))


class product(db.Model):
    # name img average maximum minimum curr_price date
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    img = db.Column(db.String(80), unique=True, nullable=False)
    average = db.Column(db.Integer, unique=False, nullable=False)
    maximum = db.Column(db.Integer, unique=False, nullable=False)
    minimum = db.Column(db.Integer, unique=False, nullable=False)
    curr_price = db.Column(db.Integer, unique=False, nullable=False)
    date = db.Column(db.String(120), unique=False, nullable=False)


class shop(db.Model):
    # name mobile address bitno password date
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    mobile = db.Column(db.Integer, unique=False, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    bitno = db.Column(db.String(120), unique=False, nullable=False)
    date = db.Column(db.String(120), unique=False, nullable=False)


class customer(db.Model):
    # sno,name,gaav,ptype,count,dname,phone,rate,weight,hamali,battav,moisture,date
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    gaav = db.Column(db.String(80), unique=False, nullable=False)
    ptype = db.Column(db.String(80), unique=False, nullable=False)
    count = db.Column(db.Integer, unique=False, nullable=False)
    dname = db.Column(db.String(80), unique=False, nullable=False)
    phone = db.Column(db.String(12), unique=False, nullable=True)
    rate = db.Column(db.Integer, unique=False, nullable=True)
    total = db.Column(db.Integer, unique=False, nullable=True)
    weight = db.Column(db.Numeric(10, 2), unique=False, nullable=True)
    hamali = db.Column(db.Integer, unique=False, nullable=True)
    battav = db.Column(db.Integer, unique=False, nullable=True)
    moisture = db.Column(db.Integer, unique=False, nullable=True)
    date = db.Column(db.String(120), unique=False, nullable=True)


class account(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Account_name = db.Column(db.String(80), unique=False, nullable=False)
    Account_no = db.Column(db.String(120), unique=False, nullable=False)
    mobile = db.Column(db.String(120), unique=False, nullable=False)
    ifsccode = db.Column(db.String(120), unique=False, nullable=False)
    branch = db.Column(db.String(120), unique=False, nullable=False)
    date = db.Column(db.String(120), unique=False, nullable=False)


class slogin(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    mobile = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    valid = db.Column(db.Boolean, unique=False, nullable=False)
    date = db.Column(db.String(120), unique=False, nullable=False)


class contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    phone = db.Column(db.String(12), unique=False, nullable=False)
    message = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.String(80), unique=False, nullable=False)


@app.route("/")
@app.route("/home")
def index():
    data = product.query.all()
    Indexsss()
    return render_template("index.html",data=data)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/downloadbills", methods=["GET", "POST"])
def downloadbills():
    data2 = product.query.all()
    if request.method == "POST":
        name = request.form.get("name")
        ptype = request.form.get("ptype")
        sno = request.form.get("phone")
        data = customer.query.filter_by(sno=sno).first()
        if(data.name == name and data.ptype == ptype):
            redirect("/download/"+sno)
        else:
            flash('Invalid details Check Once')
            redirect("/downloadbills")
    return render_template("downloadbills.html",data=data2)


@app.route("/contact", methods=['GET', 'POST'])
def contacts():
    if (request.method == "POST"):
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        entry = contact(name=name, email=email, phone=phone,
                        message=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template("contact.html")


@app.route('/slogin', methods=['GET', 'POST'])
def slogin():
    if 'user' in session and session['user'] == True:
        data = customer.query.all()
        return render_template("dash.html",data=data)

    if request.method == 'POST':
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        data = shop.query.filter_by(mobile = mobile).first()
        if (int(mobile) == int(data.mobile) and password == data.password):
            try:
                sms_send(mobile)
            except:
                print(otp)
            # session['user'] = True
            return render_template("otp.html",mobile=mobile)
        else:
            flash('Wrong Login Credentials. Please try again.', 'error')
            return redirect(url_for('slogin'))
    else:
        return render_template("login.html", params=params)


@app.route("/price_display/<string:name>")
def price_display(name):
    data = customer.query.filter_by(ptype=name).all()
    symbols = [d.date for d in data]
    prices = [d.rate for d in data]
    plt.plot(symbols, prices)
    plt.title(name)
    plt.xlabel("DATE")
    plt.ylabel("PRICE")
    plt.grid()
    plt.xticks(rotation=0)
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    data1 = product.query.filter_by(name=name).first()
    return render_template("priceDisplay.html", graph_url=graph_url,name=name,data=data,data1=data1)


@app.route("/bitwork")
def bitwork():
    if 'user' in session and session['user'] == True:
        data = customer.query.all()
        return render_template("bitwork.html", data=data)


@app.route("/addcustomer", methods=['GET', 'POST'])
def addcustomer():
    if 'user' in session and session['user'] == True:
        if request.method == "POST":
            name = request.form.get("name")
            gaav = request.form.get("gaav")
            p_type = request.form.get("p_type")
            count = request.form.get("count")
            dname = request.form.get("dname")
            entry = customer(name=name, gaav=gaav, ptype=p_type,
                             count=count, dname=dname, date=datetime.now())
            db.session.add(entry)
            db.session.commit()
        data = product.query.all()
        return render_template("addcustomer.html", data=data)


@app.route("/weightprice/<string:sno>", methods=["GET", "POST"])
def weightprice(sno):
    if 'user' in session and session['user'] == True:
        data = customer.query.filter_by(sno=sno).first()
        if request.method == "POST":
            data.name = request.form.get("name")
            data.ptype = request.form.get("type")
            data.count = request.form.get("count")
            data.weight = request.form.get("weight")
            data.rate = request.form.get("price")
            data.moisture = request.form.get("moisture")
            data.date = datetime.now()
            data.total = float(data.rate) * float(data.weight)
            data.labour_cost = 20 * data.weight 
            db.session.commit()
        return render_template("weightprice.html", data=data)


@app.route("/product", methods=["GET", "POST"])
def addproduct():
    if 'user' in session and session['user'] == True:
        data= product.query.all()
        if request.method == "POST":
            name = request.form.get("name")
            img = request.form.get("img_name")
            entry = product(name=name, img=img, date=datetime.now(),average =0,curr_price=0,minimum=0,maximum=0)
            db.session.add(entry)
            db.session.commit()
        return render_template("addproduct.html",data=data)


@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect("/")


@app.route("/otp_auth",methods=['GET','POST'])
def otp_auth():
    if request.method == "POST":
        otp_user = request.form.get("otp")
        if(otp_user == otp):
            session['user'] = True
            return redirect("/dashboard")
        else:
            flash('Invalid OTP')
            return redirect("/otp")
    return render_template("otp.html")


@app.route("/dashboard")
def dashboard():
    if 'user' in session and session['user'] == True:
        data = customer.query.all()
        return render_template("dash.html",data=data)


@app.route("/dailyreport")
def dailyreport():
    if 'user' in session and session['user'] == True:
        data = db.session.query(customer.ptype, db.func.sum(customer.rate)).group_by(customer.ptype).all()
        labels = [item[0] for item in data]
        values = [item[1] for item in data]

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        ax.set_title("Data by Group")
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = 'data:image/png;base64,' + urllib.parse.quote(string)
        return render_template("dailyreport.html",uri=uri)


@app.route("/showbill/<string:sno>")
def showbill(sno):
    data = customer.query.filter_by(sno=sno).first()
    finalamt=final_price(data.weight,data.rate)
    return render_template("billpdf.html",data = data,finalamt=finalamt)


@app.route("/download/<string:sno>")
def download(sno):
    if 'user' in session and session['user'] == True:
        data = customer.query.filter_by(sno=sno).first()
        finalamt=final_price(data.weight,data.rate)
        return render_template("billpdf.html",data = data,finalamt=finalamt)
        

@app.route("/dummy")
def dummy():
    names = ["Aarav", "Aditya", "Amit", "Arun", "Bhavesh", "Chirag", "Deepak", "Dhruv", "Gaurav", "Harsh", "Ishaan", "Kunal", "Mukesh", "Neha", "Nilesh", "Parth", "Prachi", "Preeti", "Rahul", "Rajesh", "Sachin", "Sagar", "Shreya", "Sneha", "Soham", "Sonali", "Sumit", "Tanvi", "Varun", "Vidhi"]
    gaavs = ["Amreli", "Bhavnagar", "Junagadh", "Kutch", "Patan", "Rajkot", "Surat", "Vadodara"]
    ptypes = ["SOYABEAN", "TOVAR", "MOONG", "CHANNA"]
    dnames = ["ABC Traders", "DEF Industries", "GHI Corporation", "JKL Ltd", "MNO Enterprises", "PQR & Sons", "STU Group", "VWX Inc", "YZ Company"]
    phone_nums = ["9876543210", "9876543211", "9876543212", "9876543213", "9876543214"]
    hamalis = [50, 100, 150, 200]
    battavs = [10, 20, 30, 40]
    moistures = [5, 10, 15, 20]
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)

    for i in range(30):
        name = random.choice(names)
        gaav = random.choice(gaavs)
        ptype = random.choice(ptypes)
        count = random.randint(1, 10)
        dname = random.choice(dnames)
        phone = random.choice(phone_nums)
        rate = random.randint(5000, 7000)
        weight = random.uniform(50, 100)
        hamali = random.choice(hamalis)
        battav = random.choice(battavs)
        moisture = random.choice(moistures)
        delta = end_date - start_date
        random_date = start_date + timedelta(days=random.randint(0, delta.days))
        random_time = datetime.min + timedelta(minutes=random.randint(0, 24*60))
        random_datetime = datetime.combine(random_date, random_time.time())
        date = random_datetime
        new_customer = customer(name=name, gaav=gaav, ptype=ptype, count=count, dname=dname, phone=phone, rate=rate, weight=weight, battav=battav, moisture=moisture,total=rate*weight,hamali=20*weight, date=date)
        db.session.add(new_customer)
    db.session.commit()
    return "Entries added Successfully"

@app.route('/push_list')
def push_list():
    data = [
    ("SOYABEAN","soyabean.jpg",0,0,0,0,datetime.today()),
    ("TOVAR","toordal.jpg",0,0,0,0,datetime.today()),
    ("CHANNA","channa.jpg",0,0,0,0,datetime.today()),
    ("MOONG","moong.jpg",0,0,0,0,datetime.today())
    ]

    for item in data:
        entry = product(
            # name img average maximum minimum curr_price date
            name=item[0],
            img=item[1],
            average=item[2],
            maximum=item[3],
            minimum=item[4],
            curr_price=item[5],
            date=item[6]
        )
        db.session.add(entry)
    db.session.commit()
    return 'List pushed successfully!'

@app.route('/push_shop')
def push_shop():
    # name mobile address bitno password date
    data = [
    ("Krishna Traders",9067377912,"Shop No 4, New Mondha",12,"Krishna@123",datetime.today()),
    ("Vedant and Retailer",7249596920,"Shop No 8 New Mondha",10,"Vedant@123",datetime.today()),
    ("Bhumika Traders",7984493732,"Shop No 6 New Mondha",25,"Bhumika@123",datetime.today()),
    ("Harshada Traders",7264823818,"Shop NO 7 New Mondha",15,"Harshada@123",datetime.today())
    ]

    for item in data:
        entry = shop(
            # name mobile address bitno password date
            name=item[0],
            mobile=item[1],
            address=item[2],
            bitno=item[3],
            password=item[4],
            date=item[5]
        )
        db.session.add(entry)
    db.session.commit()
    return 'List pushed successfully!'


@app.route('/uploader',methods = ['GET','POST'])
def upload():
	if 'user' in session and session['user'] == True:
		if (request.method == "POST"):
			f = request.files['file']
			f.save(os.path.join(app.config['UPLOAD_FILE'], secure_filename(f.filename)))
			return redirect("/product")
            

@app.route('/delete/<string:id>',methods = ['GET','POST'])
def delete(id):
	if 'user' in session and session['user'] == True:
		posts = product.query.filter_by(sno=id).first()
		db.session.delete(posts)
		db.session.commit()
	return redirect('/dashboard')


if __name__ == '__main__':
    app.run(debug=True)
