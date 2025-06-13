from models import User
from utils import gen_hash,check_hash
import peewee

def signup_db(name, email, username, password):
    # correct method
    try:
        H_pass = gen_hash(password)
        User.create(name=name, email=email, username=username, password=H_pass)
        message,category,status = "Signup is successful.",'success',True
        return message,category,status
    except peewee.IntegrityError:
        message,category,status = "username or email already in use try different",'danger',False
        return message,category,status
    

def login_db(username,password):
    user = User.get_or_none(User.username == username)
    if check_hash(user.password,password):
        message,category,status = "Login is successful.",'success',True
        return message,category,status,user
    else:
        message,category,status = "Login Failed",'danger',False
        return message,category,status,None