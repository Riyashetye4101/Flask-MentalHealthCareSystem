from mental.models import *
from datetime import datetime
from operator import and_
import smtplib
EMAIL_HOST_USER = 'tiffinservice944@gmail.com'
EMAIL_HOST_PASSWORD = 'R!y@4101'

def send(email,title,content):
    sub=f'Reminder for the treatment of {title}'
    mssg=f'Advice:-\n\n {content}.\n\n please check our site for the task which are schedule for your treatment'
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    s.sendmail(EMAIL_HOST_USER,email, f"Subject: {sub}\n\n{mssg}")
    s.quit()

def mail():
    t=Test.query.filter(and_(Test.end>datetime.today(),Test.senddate!=datetime.today().date()))
    for i in t:
        user=Customer.query.get(i.parent_id)
        send(user.email,i.tname,i.activity)
        i.senddate=datetime.today().date()
        db.session.add(i)
        db.session.commit()