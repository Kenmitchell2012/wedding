from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models.user import User

db = "wedding"
class Wedding:
    def __init__(self, data):
        self.id = data['id']
        self.wedding_side = data['wedding_side']
        self.meal = data['meal']
        self.drink = data['drink']
        self.favorite_memory = data['favorite_memory']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # get all books
    @classmethod
    def get_all_weddings(cls):
        query = """
                SELECT * FROM weddings
                JOIN users on weddings.user_id = users.id;
                """
        results = connectToMySQL(db).query_db(query)
        print(results)
        weddings = []
        for row in results:
            this_wedding = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": ""
            }
            this_wedding.creator = User(user_data)
            weddings.append(this_wedding)
            print(this_wedding)
        return weddings
    
    # validate the wedding
    def validate_wedding(form_data):
        is_valid = True
        if 'wedding_side' not in form_data or form_data['wedding_side'] not in ['bride', 'groom']:
            flash("Please select a wedding side!", 'wedding')
            is_valid = False
        if 'meal' not in form_data or form_data['meal'] not in ['chicken', 'steak', 'vegan dish', 'kids meal']:
            flash("Please select a meal option!", 'wedding')
            is_valid = False
        if 'drink' not in form_data or form_data['drink'] not in ['wine', 'coke', 'bourbon', 'water', "kid's drink" ]:
            flash("Please select a drink option!", 'wedding')
            is_valid = False
        if len(form_data['favorite_memory']) < 10:
            flash("Favorite memory must be at least 10 characters.", 'wedding')
            is_valid = False
        return is_valid

    
    # save the wedding
    @classmethod
    def save_wedding(cls, data):
    
        query = """
                INSERT INTO weddings (wedding_side, meal, drink, favorite_memory, user_id, creator)
                VALUES (%(wedding_side)s, %(meal)s, %(drink)s, %(favorite_memory)s, %(user_id)s, %(creator)s);
                """
        return connectToMySQL(db).query_db(query, data)
    
    # get wedding by id
    @classmethod
    def get_wedding_by_id(cls, id):
        query = """
                SELECT * FROM weddings
                WHERE id = %(id)s;
                """
        results = connectToMySQL(db).query_db(query, {'id': id})
        return cls(results[0])
    
    # delete the wedding
    @classmethod
    def delete(cls,data):
        query = """
                DELETE FROM weddings
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)