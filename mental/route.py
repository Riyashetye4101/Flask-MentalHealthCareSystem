from mental import app
from flask import render_template,json,url_for,request,redirect,flash
import os
from mental.forms import *
from mental.models import *
from mental import db
from flask_login import login_user,logout_user,current_user
from datetime import datetime, timedelta
from mental import sendemail


@app.route('/chatbot')
def chatbot():
    return render_template('chat.html')

@app.route('/profile')
def profile():
    check=None
    test=Test.query.filter(Test.parent_id==current_user.id,Test.end<datetime.today())
    for i in test:
        if(i!=None):
            check=True
            break
        else:
            check=False
            break
    return render_template('profile.html',test=test)

@app.route('/schedule')
def schedule():
    if current_user.is_authenticated:
        test=Test.query.filter(Test.parent_id==current_user.id,Test.end>=datetime.today())
        return render_template('schedule.html',list=test)
    flash('first login, then enjoy the survices',category='Successfully')
    return redirect(url_for('signup'))

@app.route('/<s>/<age>/evolve',methods=['GET', 'POST'])
def evolve(s,age):
    if age<='18':
        temp='recommendation/relation(below).html'
    elif s=='m' or s=='r':
        temp='recommendation/married.html'
    elif s=='d' or s=='w':
        temp='recommendation/widowed.html'
    else:
        temp='recommendation/relation(18-30).html'
    return render_template(temp)

@app.route('/<l>/<category>/task',methods=['GET', 'POST'])
def task(l,category):
    if category=='Anxiety':
        if l=='low':
            temp='recommendation/low anxiety.html'
        elif l=='medium':
            temp='recommendation/medium anxiety.html'
        else:
            temp='recommendation/high anxiety.html'
    elif category=='stress':
        if l=='low':
            temp='recommendation/low stress.html'
        elif l=='medium':
            temp='recommendation/med anxiety.html'
        else:
            temp='recommendation/High stress.html'
    elif category=='Drepression':
        if l=='low':
            temp='recommendation/depression/lowdepress.html'
        elif l=='medium':
            temp='recommendation/depression/medium depression.html'
        else:
            temp='recommendation/depression/high depression.html'
    elif category=='Loneliness':
        if l=='low':
            temp='recommendation/low loneliness.html'
        elif l=='medium':
            temp='recommendation/medium loneliness.html'
        else:
            temp='recommendation/high loneliness.html'
    elif category=='selfesteem':
        if l=='low':
            temp='recommendation/selfesteem/lowse.html'
        elif l=='medium':
            temp='recommendation/selfesteem/highse.html'
        else:
            temp='recommendation/selfesteem/mediumse.html'
    else:
        temp='profile.html'
    return render_template(temp)



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/anxiety')
def anxietytest():
    return render_template('anxietytest.html')

@app.route('/mcq',methods=['POST'])
def mcq():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/json", "anxiety.json")
    data = json.load(open(json_url))
    lst=list()
    test='Anxiety'
    sum=0
    level='empty'
    for i in range(0,20):
        s='q'+str(i+1)
        sum=sum+int(request.form[s])
    if 0<sum and sum<=20:
        suggestion=data["1"]+' '+data['2']+' '+data['3']+' '+data['4']+' '+data['5']
        level='low'
    elif 20<sum and sum<=40:
        suggestion=data['4']+' '+data["6"]+' '+data['7']+' '+data['8']+' '+data['9']+' '+data['5']
        level='medium'
    elif 40<sum and sum<=60:
        suggestion=data["6"]+' '+data['7']+' '+data['8']+' '+data['9']+' '+data['10']+' '+data['11']+' '+data["12"]
        level='high'
    else:
        suggestion=None
    if current_user.is_authenticated:
        present=Test.query.filter(Test.parent_id==current_user.id,Test.tname==test,Test.end>=datetime.today()).first()
        if present!=None:
            if sum==0:
                db.session.delete(present)
                db.session.commit()
            else:
                present.result=str(sum)
                present.date=datetime.now()
                present.activity=suggestion
                present.level=level
                db.session.commit()
        else:
            if sum!=0:
                t=Test(tname=test,result=sum,date=datetime.now(),activity=suggestion,
                end= datetime.now() + timedelta(days=30),level=level,senddate=datetime.today().date()-timedelta(days=1),parent_id=current_user.id)
                db.session.add(t)
                db.session.commit()
                sendemail.mail()
    return render_template('mcq.html',total=60-sum,sum=sum,test=test,recom=suggestion,level=level)

@app.route('/stress')
def stresstest():
    return render_template('stress.html')
@app.route('/resultofstress',methods=['POST'])
def stest():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/json", "stress.json")
    data = json.load(open(json_url))
    sum=0
    test='stress'
    level='empty'
    for i in range(0,10):
        s='q'+str(i+1)
        sum=sum+int(request.form[s])
    if 0<sum and sum<=10:
        level='low'
        suggestion=data["1"]+' '+data['2']+' '+data['3']
    elif 10<sum and sum<=20:
        level='low'
        suggestion=data['2']+' '+data["3"]+' '+data['4']+' '+data['5']+' '+data['6']
    elif 20<sum and sum<=30:
        level='medium'
        suggestion=data['4']+' '+data['5']+' '+data["6"]+' '+data['7']+' '+data['8']+' '+data['9']
    elif 30<sum<=40:
        level='high'
        suggestion=data['1']+' '+data['2']+' '+data["6"]+' '+data['10']+' '+data['11']+' '+data['12']
    else:
        suggestion=None
    if current_user.is_authenticated:
        present=Test.query.filter(Test.parent_id==current_user.id,Test.tname==test,Test.end>=datetime.today()).first()
        if present!=None:
            if sum==0:
                db.session.delete(present)
                db.session.commit()
            else:
                present.result=str(sum)
                present.date=datetime.now()
                present.activity=suggestion
                present.level=level
                db.session.commit()
        else:
           if sum!=0:
                t=Test(tname=test,result=sum,date=datetime.now(),activity=suggestion,
                end= datetime.now() + timedelta(days=30),level=level,senddate=datetime.today().date()-timedelta(days=1),parent_id=current_user.id)
                db.session.add(t)
                db.session.commit()
                sendemail.mail()
    return render_template('mcq.html',sum=sum, test=test,total=40-sum,recom=suggestion,level=level)


@app.route('/depression')
def depressiontest():
    return render_template('depression.html')
@app.route('/resultofdepression',methods=['POST'])
def dtest():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/json", "depress.json")
    data = json.load(open(json_url))
    lst=list()
    sum=0
    test='Drepression'
    level='empty'
    for i in range(0,18):
        s='q'+str(i+1)
        sum=sum+int(request.form[s])
    if 0<sum and sum<=18:
        level='low'
        suggestion=data["1"]+' '+data['2']+' '+data['3']+' '+data['4']
    elif 18<sum and sum<=36:
        level='medium'
        suggestion=data['3']+' '+data["4"]+' '+data['5']+' '+data['6']
    elif 36<sum and sum<=54:
        level='high'
        suggestion=data["6"]+' '+data['7']+' '+data['8']+' '+data['9']
    else:
        suggestion=None
    if current_user.is_authenticated:
        present=Test.query.filter(Test.parent_id==current_user.id,Test.tname==test,Test.end>=datetime.today()).first()
        if present!=None:
            if sum==0:
                db.session.delete(present)
                db.session.commit()
            else:
                present.result=str(sum)
                present.date=datetime.now()
                present.activity=suggestion
                present.level=level
                db.session.commit()
        else:
            if sum!=0:
                t=Test(tname=test,result=sum,date=datetime.now(),activity=suggestion,
                end= datetime.now() + timedelta(days=30),level=level,senddate=datetime.today().date()-timedelta(days=1),parent_id=current_user.id)
                db.session.add(t)
                db.session.commit()
                sendemail.mail()
    return render_template('mcq.html',sum=sum, test=test,total=(18*3)-sum,recom=suggestion,level=level)

@app.route('/loneliness')
def lonelinesstest():
    return render_template('loneliness.html')
@app.route('/resultofloneliness',methods=['POST'])
def ltest():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/json", "lonely.json")
    data = json.load(open(json_url))
    lst=list()
    sum=0
    test='Loneliness'
    level='empty'
    for i in range(0,20):
        s='q'+str(i+1)
        sum=sum+int(request.form[s])
    if 0<sum and sum<=20:
        level='low'
        suggestion=data["1"]+' '+data['2']+' '+data['3']+' '+data['4']
    elif 20<sum and sum<=40:
        level='medium'
        suggestion=data['3']+' '+data["4"]+' '+data['5']+' '+data['6']+' '+data['8']+' '+data['9']
    elif 40<sum and sum<=60:
        level='high'
        suggestion=data['5']+' '+data["6"]+' '+data['7']+' '+data['8']+' '+data['9']+' '+data['10']
    else:
        suggestion=None
    if current_user.is_authenticated:
        present=Test.query.filter(Test.parent_id==current_user.id,Test.tname==test,Test.end>=datetime.today()).first()
        if present!=None:
            if sum==0:
                db.session.delete(present)
                db.session.commit()
            else:
                present.result=str(sum)
                present.date=datetime.now()
                present.activity=suggestion
                present.level=level
                db.session.commit()
        else:
            if sum!=0:
                t=Test(tname=test,result=sum,date=datetime.now(),activity=suggestion,
                end= datetime.now() + timedelta(days=30),level=level,senddate=datetime.today().date()-timedelta(days=1),parent_id=current_user.id)
                db.session.add(t)
                db.session.commit()
                sendemail.mail()
    return render_template('mcq.html',sum=sum, test=test,total=60-sum,recom=suggestion,level=level)


@app.route('/relationshiptest')
def relationshiptest():
    return render_template('relationship.html')
@app.route('/resultofrelationship',methods=['POST'])
def rtest():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/json", "relationship.json")
    data = json.load(open(json_url))
    dic={}
    sum=0
    test='relation Analysis'
    for i in range(0,12):
        s='q'+str(i+1)
        sum=sum+int(request.form[s])
    dic['gender']=request.form['q13']
    dic['age']=request.form['q14']
    dic['status']=request.form['q15']
    dic['year']=request.form['q16']
    total=36-sum
    if 0<=sum<15:
        if sum==0:
            sum=None
        suggestion=data['2']+data['6']+data['7']+data['8']+data['4']+data['5']+data['10']
    elif 15<=sum<25:
        suggestion=data['1']+data['6']+data['7']+data['8']+data['4']
    elif 25<=sum<30:
        suggestion=data['3']+data['6']+data['7']+data['8']
    elif sum==36 and (dic['status']!='s' or dic['status']!='d'):
        suggestion="you clear your relationship test where you not only love you'r partner but also trust him/her and rely on him/her"
        total=0
    else:
        suggestion='Are you sure you are in relationship with your partner still!'
    return render_template('mcq.html',sum=sum, test=test,recom=suggestion,total=total,status=dic['status'],age=dic['age'])

@app.route('/selfesteem')
def selfesteemtest():
    return render_template('selfesteem.html')
@app.route('/resultofselfesteem',methods=['POST'])
def selftest():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/json", "self-esteem.json")
    data = json.load(open(json_url))
    lst=list()
    sum=0
    test='selfesteem'
    level='empty'
    for i in range(0,10):
        s='q'+str(i+1)
        sum=sum+int(request.form[s])
    if 0<sum and sum<=10:
        level='low'
        suggestion=data["1"]+' '+data['2']+' '+data['3']
    elif 10<sum and sum<=20:
        level='medium'
        suggestion=data['2']+' '+data["3"]+' '+data['4']+' '+data['5']+' '+data['6']
    elif 20<sum and sum<=30:
        level='medium'
        suggestion=data['4']+' '+data['5']+' '+data["6"]+' '+data['7']+' '+data['8']+' '+data['9']
    elif 30<sum<=40:
        level='high'
        suggestion=data['1']+' '+data['2']+' '+data["6"]+' '+data['10']+' '+data['11']
    else:
        suggestion=None
    if current_user.is_authenticated:
        present=Test.query.filter(Test.parent_id==current_user.id,Test.tname==test,Test.end>=datetime.today()).first()
        if present!=None:
            if sum==0:
                db.session.delete(present)
                db.session.commit()
            else:
                present.result=str(sum)
                present.date=datetime.now()
                present.activity=suggestion
                present.level=level
                db.session.commit()
        else:
            if sum!=0:
                t=Test(tname=test,result=sum,date=datetime.now(),activity=suggestion,
                end= datetime.now() + timedelta(days=30),level=level,senddate=datetime.today().date()-timedelta(days=1),parent_id=current_user.id)
                db.session.add(t)
                db.session.commit()
                sendemail.mail()
    return render_template('mcq.html',sum=sum, test=test,total=40-sum,recom=suggestion,level=level)

@app.route('/signup',methods=['GET','POST'])
def signup():
    form=Registeration()
    if form.validate_on_submit():
        User_create=Customer(username=form.username.data,name=form.name.data,email=form.email_address.data,password=form.password.data,mobile=form.mobile.data,age=form.age.data)
        db.session.add(User_create)
        db.session.commit()
        flash('Successfully registered, now login',category='Successfully')
        return redirect(url_for('signup'))
    if form.errors != {} :
        for error_mgs in form.errors.values():
            flash(error_mgs,category='danger')
    return render_template('sign.html',form=form)

@app.route('/signin',methods=['GET','POST'])
def signin():
    user=request.form['username']
    pswd=request.form['pswd']
    if user!='' and pswd!='':
        attempted_user=Customer.query.filter_by(username=user).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=pswd):
            login_user(attempted_user)
            return redirect(url_for('home'))
        else:
            flash('Username and password doesnot match please try again')
    return redirect(url_for('signup'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
