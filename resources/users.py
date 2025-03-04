import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user')

@user.route('/register', methods=['POST'])

def register():
    print('are we hitting route')
    """ Accepts a post request with new user's email and password """
    payload = request.get_json()
    print(payload)
    if not payload['email'] or not payload['password']:
        return jsonify(status=400)
    
    try:
        # Won't throw an exception if email already in DB
        models.User.get(models.User.email ** payload['email']) 
        return jsonify(data={}, status={'code': 400, 'message': 'A user with that email already exists.'}) 
    except models.DoesNotExist: 
        print(payload) 
        payload['password'] = generate_password_hash(payload['password']) # Hash user's password
        new_user = models.User.create(**payload)
        # profile = models.Profile.create(user=new_user)
        # Start a new session with the new user
        print(new_user)
        login_user(new_user)
        user_dict = model_to_dict(new_user)
        print(user_dict)
        print(type(user_dict))
        # delete the password before sending user dict back to the client/browser
        del user_dict['password']
        return jsonify(data=user_dict, status={'code': 201, 'message': 'User created'})

@user.route('/login', methods=['POST'])

def login():
    print('We are hitting the login route')
    payload = request.get_json()
    print(payload)        
    try:
        user = models.User.get(models.User.email ** payload['email'])
        user_dict = model_to_dict(user)
        user_id = user_dict["id"]
        print(user_id)
        # check_password_hash(<hash_password>, <plainttext_pw_to_compare>)
        if (check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user) # Setup for the session
            print('User is:', user_dict)
            return jsonify(data=user_dict,  status={'code': 200, 'message': 'User authenticated', 'id': user_id, })
        return jsonify(data={}, status={'code': 401, 'message': "Email or password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': "Email or password is incorrect"})


# @user.route('/logout', methods=['GET'])
# # closely following the docs here: https://flask-login.readthedocs.io/en/latest/#login-example
# def logout():
#   # for fun lets get the user's email from current_user to make a nice msg
#   email = model_to_dict(current_user)['email']
#   logout_user()
#   return jsonify(data={}, status={
#       'code': 200,
#       'message': "Successfully logged out {}".format(email)
#   })
