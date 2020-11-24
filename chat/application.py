from flask import Flask,render_template,flash,redirect,url_for,request
from forms import RegisterForm,LoginForm,CreateRoom,UploadFile
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager,login_user,current_user,logout_user
from werkzeug.utils import secure_filename
from models import User,Friend
import os
from sqlalchemy import create_engine
engine=create_engine("database url")
# this code is write for delete freiend
from sqlalchemy.orm import sessionmaker,scoped_session
session_factory=sessionmaker(bind=engine)
session1=scoped_session(session_factory)
s1=session1()
# end code
# from flask_migrate import Migrate

# instance of flask app
app=Flask(__name__)
# Secret_key
app.config['SECRET_KEY'] = 'secret key'
# Database location postgress localhost
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:@localhost:5432/de3capulkm5v8k"
app.config['SQLALCHEMY_DATABASE_URI'] = "database url"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# ininlize db(connection with database)
db = SQLAlchemy(app)



# migrate = Migrate(app, db)
# User Table Model
# configure flask_login
# Email send
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
s = URLSafeTimedSerializer("Thisisasecret!")

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'user email',
    MAIL_PASSWORD = 'email password',
))

mail = Mail(app)

# code for flask socketio
from flask_socketio import SocketIO,join_room, leave_room,emit
socketio = SocketIO(app)

login=LoginManager(app)
# initlize login app
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/register", methods=["GET","POST"])
def register():
   form = RegisterForm()  
   if form.validate_on_submit():  
       username=form.name.data 
       email=form.email.data
       password=form.password.data
       sendmessage=[username,email,password]
       token = s.dumps(sendmessage, salt='email-confirm')
       msg = Message('Confirm Email chatapp', sender='email id with send  ', recipients=[email]) 
       link = url_for('confirm_Email', token=token, _external=True)
       msg.body = 'Your link is {} Please click confirmation '.format(link)
       mail.send(msg)
       flash("Please check email")
       return redirect(url_for('register'))    
   return render_template("register.html",form=form)

@app.route('/confirm_Email/<token>')
def confirm_Email(token):
    try:
        getmessage = s.loads(token, salt='email-confirm', max_age=8600)
        print(getmessage)
    except SignatureExpired:
        flash("Session Expire of tokrn please try again","danger")
        return redirect(url_for('register'))
    print(getmessage[2],getmessage[0],getmessage[1])    
    hash_password=pbkdf2_sha256.hash(getmessage[2])
    user=User(username=getmessage[0],email=getmessage[1],password=hash_password)
    db.session.add(user)
    db.session.commit()
    db.session.close()    
    flash("Your account is Successfully created please login")   
    return redirect(url_for('login'))

@app.route('/login',methods=["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user_obj=User.query.filter_by(email=form.email.data).first()
        login_user(user_obj)
        return redirect(url_for('chat'))
    return render_template("login.html",form=form)

@app.route('/chat')
def chat():
   if not current_user.is_authenticated:
       flash("Please login ","danger")
       return redirect(url_for('login'))
   all_friend=Friend.query.filter((Friend.send==current_user.get_id())| (Friend.receive==current_user.get_id())).all()    
   return render_template("Chatt.html",all_friend=all_friend)  


@app.route('/dashbord',methods=["GET","POST"])
def dashbord():
   if current_user.is_authenticated: 

        form1=CreateRoom()
        form2=UploadFile()
        all_user=User.query.filter(User.id!=current_user.get_id()).all()
        print(current_user.get_id())
        all_friend=Friend.query.filter((Friend.send==current_user.get_id())| (Friend.receive==current_user.get_id())).all()
        l=[]
        for i in all_friend:
            if i.send == current_user.id :
                l.append(User.query.get(i.receive))
            else:
                l.append(User.query.get(i.send))    

        print(all_friend,l)
        if form1.validate_on_submit():
            user_obj=User.query.get(current_user.get_id())
            if user_obj.room is None :
                user_obj.room=form1.room.data
                db.session.merge(user_obj)
                db.session.commit()
                db.session.close()
                flash("Your room is successfully created")
            else:
                flash("You are already create room ","danger")       
        elif form2.validate_on_submit():
            print("success")
            uploaded_file = form2.file.data
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join('static/image',filename))
            print(filename)
            user_obj=User.query.get(current_user.get_id())
            print(current_user.get_id())
            print(user_obj.image_name)
            name=user_obj.image_name
            if name is None :
                user_obj.image_name=filename
                db.session.merge(user_obj)
                db.session.commit()
                db.session.close()
                flash("Your file is successfully uploaded")
            else:
                flash("you are already upload image","danger")
                
            return redirect(url_for('dashbord'))
        
        return render_template("dashbord.html",form1=form1,form2=form2,all_user=all_user,all_friend=all_friend,userobject=l)  
   else:
        return redirect(url_for('login'))

              
   

@app.route('/send/<int:id1>/<int:id2>/<string:room>')
def send(id1,id2,room):
   print(room)
   if room == "None" :
       flash("Please create own room then send","danger")
       return redirect(url_for("dashbord"))  
   else :
       fcheck=Friend.query.filter((Friend.send==id1) & (Friend.receive==id2)).first()
       if fcheck :
           flash("You are already send request","danger")
       else:
            F=Friend(send=id1,receive=id2,room_name=room)
            db.session.add(F)
            db.session.commit()
            db.session.close()
            flash("Your request successfully send")
       return redirect(url_for("dashbord"))    

@app.route('/unfriend/<int:id1>/<int:id2>')
def unfriend(id1,id2):
    print(id1,id2)
    user_obj=s1.query(Friend).filter((Friend.send==id1) & (Friend.receive==id2)).first()
    s1.delete(user_obj)
    s1.commit()
    s1.close()
    flash("Your Freiend successfully unfriend","danger")
    
    return redirect(url_for('dashbord'))

@app.route('/logout')
def logout():
   logout_user()
   flash("You are logged out",'danger')
   return redirect(url_for('login'))



# Flask socket
@socketio.on('message')
def handle_message(message):
    if message["room"]=="NO":
        socketio.send(message)
    else:
        socketio.send(message,room=message["room"])    

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    socketio.send({'msg':"has join the room.",'username':username},room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    socketio.emit('leave',{'msg':"has leave the room.",'username':username} )      


# run flask code....
if __name__=="__main__":
    socketio.run(app, debug=True)
