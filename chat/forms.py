from flask_wtf import Form  
from wtforms import TextField,StringField, SubmitField ,PasswordField
from flask_wtf.file import FileField
from wtforms.validators import InputRequired, Length,ValidationError,Email
from passlib.hash import pbkdf2_sha256
from models import User
import os

def invalid_credentials(form,field):
   """Username and password Chaker"""
   email_enter=form.email.data
   password_enter=field.data
   user_object=User.query.filter_by(email=email_enter).first()
   if user_object is None:
      raise ValidationError("Email is not match our database")
   elif not pbkdf2_sha256.verify(password_enter,user_object.password ):
      raise ValidationError("Please enter correct password")
   

class RegisterForm(Form):  
   name = StringField("Name",validators=[InputRequired("Please enter your name."),Length(min=4,max=10,message="User name must be above 4 and maximum 10 character")])    
   email = StringField("Email",validators=[InputRequired("Please enter your email address."),Email("Please Fill Correct email")])  
   password=PasswordField("Password", validators=[InputRequired("Plrase Enter Password"),Length(min=4,max=8,message="Password must be minimum 4 and maximum 8 character")])
   Register = SubmitField("Register")  

   def validate_email(self,email):
      if User.query.filter_by(email=email.data).first():
         raise ValidationError("User already exists please enter another user")

class LoginForm(Form):
    email=StringField("Email",validators=[InputRequired("Please enter your email address"),Email("Please fill correct Email address")])
    password=PasswordField("Password",validators=[InputRequired("Please enter your password"),Length(min=4,max=8,message="Password must be minimum 4 and maximum 8 character"), invalid_credentials])
    Login = SubmitField("Login")

class CreateRoom(Form):
   room=StringField("Room",validators=[InputRequired("Please enter room name"),Length(min=3,message="Room name must be above 3 character")]) 
   Submit = SubmitField("Submit")   

   # def check_Unique_Room(self,room):
   #    if User.query.filter_by(room=room.data).first():
   #       raise ValidationError("Room name already exists please enter another room")

class UploadFile(Form):
      file = FileField('File',validators=[InputRequired("Please upload file")])
      Upload = SubmitField('Upload')   

      def validate_file(self,file):
         uploaded_file = file.data 
         if uploaded_file.filename != '':
            filename = uploaded_file.filename
            file_ext = os.path.splitext(filename)[1]
            print(file_ext)
            if file_ext not in ['.jpg', '.png','.JPG','.PNG']:
               raise ValidationError("Please chosse jpg or png format image")
         else:
            raise ValidationError("please not upload without name file")   