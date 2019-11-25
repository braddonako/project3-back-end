import models

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict


post = Blueprint('posts', 'post')

## show all posts
@post.route('/', methods=["GET"])
def get_all_posts():
    print('current user: ', current_user)

    all_posts = [model_to_dict(post, max_depth=1) for post in models.Post.select()]
    return jsonify(data=all_posts, status={'code': 200, 'message': 'Success'})


# create route
@post.route('/', methods=["POST"])
# @login_required
def create_posts():
    ## see request payload anagolous to req.body in express
    payload = request.get_json()
    print(type(payload), 'payload')
    payload['user'] = current_user.id
    post = models.Post.create(**payload) # this could be a session to get the user id -> use current_user
    ## see the object
    print(post.__dict__)
    ## Look at all the methods
    print(dir(post))
    # Change the model to a dict
    print(model_to_dict(post), 'model to dict')
    post_dict = model_to_dict(post)
    return jsonify(data=post_dict, status={"code": 201, "message": "Success"})

## show route
@post.route('/<id>', methods=["GET"])
def get_one_post(id):
    print(id, 'yeeet')
    post = models.Post.get_by_id(id)
    print(post.__dict__)
    return jsonify(data=model_to_dict(post), status={"code": 200, "message": "Success"})

## update route
@post.route('/<id>', methods=["PUT"])
# @login_required
def update_post(id):
    print('UPDATINGGG')
    print(id)
    payload = request.get_json()
    print(payload)
    payload['user'] = payload['user']['id']
    query = models.Post.update(**payload).where(models.Post.id==id)
    print(query)
    query.execute()
    # print(model_to_dict(models.Post.get_by_id(id)))
    return jsonify(data=model_to_dict(models.Post.get_by_id(id)), status={"code": 200, "message": "resource updated successfully"})

@post.route('/<id>', methods=["Delete"])
# @login_required
def delete_post(id):
    query = models.Post.delete().where(models.Post.id==id)
    print(models.Post.id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})
