from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE,app
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id=data["id"]
        self.first_name=data["user_name"]
        self.email=data["email"]
        self.password=data["password"]
        self.type_user=data["type_user"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]

    @classmethod
    def add_one(cls,data):
        query="insert into users (user_name, email, password, type_user) values (%(user_name)s, %(email)s, %(password)s, 0);"
        result=connectToMySQL(DATABASE).query_db(query,data)
        return result

    

        
    @staticmethod
    def validate(data):
        first_name=data["user_name"]
        email=data["email"]
        password=data["password"]
        is_valid=True
        if len(data["user_name"])<2:
            is_valid=False
            flash("user Name needs to have at least 3 characters","user_name_validation")
        if not EMAIL_REGEX.match(data["email"]): 
            flash("Invalid email address!","email_validation")
            is_valid = False
        elif User.get_by_email({"email":data["email"]}):
            flash("email already in database","email")
            is_valid = False
        if len(data["password"])<8:
            is_valid=False
            flash("Password not strong enough","password_validation")
        return is_valid
        
                
    @classmethod
    def get_one(cls,data):
        query="select * from users where id=%(id)s;"
        result=connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def get_by_email(cls,data):
        query="select * from users where email=%(email)s;"
        result=connectToMySQL(DATABASE).query_db(query,data)
        if len(result)==0:
            flash("user email not in the database","email_validation_login")
            return None
        else:
            return cls(result[0])