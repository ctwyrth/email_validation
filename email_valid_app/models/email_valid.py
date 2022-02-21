from email_valid_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

DB = 'email_validation'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Email:
    def __init__(self, data):
            self.id = data['id']
            self.email = data['email']
            self.created_at = data['created_at']
            self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO emails (email) VALUES (%(email)s);"
        return connectToMySQL(DB).query_db(query,data)

    @classmethod
    def show_all(cls):
        query = "SELECT * FROM emails;"
        emails_from_db = connectToMySQL(DB).query_db(query)
        all_emails = []
        for email in emails_from_db:
            all_emails.append(cls(email))
        return all_emails

    @classmethod
    def show(cls, data):
        query = "SELECT * FROM emails WHERE id = %(id)s;"
        email_id = {
            'id': data
        }
        results = connectToMySQL(DB).query_db(query,email_id)
        email = cls(results[0])
        return email

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM emails WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query,data)

    @staticmethod
    def validate_email(email):
        isValid = True
        if not EMAIL_REGEX.match(email['email']):
            flash("Invalid email address!")
            isValid = False
        return isValid

    @staticmethod
    def validate_unique(email):
        isUnique = True
        emails_list = Email.show_all()
        for item in emails_list:
            print(item.email)
            if email['email'] == item.email:
                flash("That email was already in our database!")
                isUnique = False
        return isUnique