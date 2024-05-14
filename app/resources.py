from flask_restful import Resource, reqparse
from .models import db, User, Child, Blog, BlogMetadata
from datetime import datetime
from flask import jsonify

# Parser for User data
user_parser = reqparse.RequestParser()
user_parser.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_parser.add_argument('email', type=str, required=True, help="Email cannot be blank")
user_parser.add_argument('parent_type', type=str, required=True, help="Parent type cannot be blank")

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id is None:
            users = User.query.all()
            return [{
                'id': user.id, 
                'name': user.name, 
                'email': user.email, 
                'parent_type': user.parent_type
            } for user in users], 200
        else:
            # Return specific user
            user = User.query.get(user_id)
            if user:
                return {
                    'id': user.id, 
                    'name': user.name, 
                    'email': user.email, 
                    'parent_type': user.parent_type
                }
            else:
                return {'message': 'User not found'}, 404

    def post(self):
        args = user_parser.parse_args()
        user = User(name=args['name'], email=args['email'], parent_type=args['parent_type'])
        db.session.add(user)
        db.session.commit()
        return {'id': user.id, 'message': 'User created successfully.'}, 201

    def put(self, user_id):
        args = user_parser.parse_args()
        user = User.query.get(user_id)
        if user:
            user.name = args['name']
            user.email = args['email']
            user.parent_type = args['parent_type']
            db.session.commit()
            return {'message': 'User updated successfully.'}
        else:
            return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully.'}
        else:
            return {'message': 'User not found'}, 404
        

# Parser for Child data
child_parser = reqparse.RequestParser()
child_parser.add_argument('parent_id', type=int, required=True, help="Parent ID cannot be blank")
child_parser.add_argument('name', type=str, required=True, help="Name cannot be blank")
child_parser.add_argument('date_of_birth', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), required=True, help="Date of Birth cannot be blank")
child_parser.add_argument('gender', type=str, required=True, help="Gender cannot be blank")

class ChildResource(Resource):
    def get(self, child_id=None):
        if child_id is None:
            children = Child.query.all()
            children_list = [{
                'id': child.id, 
                'parent_id': child.parent_id, 
                'name': child.name, 
                'date_of_birth': child.date_of_birth.strftime('%Y-%m-%d'), 
                'gender': child.gender
            } for child in children]
            return children_list, 200
        else:
            child = Child.query.get(child_id)
            if child:
                child_data = {
                    'id': child.id, 
                    'parent_id': child.parent_id, 
                    'name': child.name, 
                    'date_of_birth': child.date_of_birth.strftime('%Y-%m-%d'), 
                    'gender': child.gender
                }
                return child_data, 200
            else:
                return {'message': 'Child not found'}, 404

    def post(self):
        args = child_parser.parse_args()
        child = Child(
            parent_id=args['parent_id'], 
            name=args['name'], 
            date_of_birth=args['date_of_birth'], 
            gender=args['gender']
        )
        db.session.add(child)
        db.session.commit()
        return {'id': child.id, 'message': 'Child created successfully.'}, 201

    def put(self, child_id):
        child = Child.query.get(child_id)
        if child:
            args = child_parser.parse_args()
            child.parent_id = args['parent_id']
            child.name = args['name']
            child.date_of_birth = args['date_of_birth']
            child.gender = args['gender']
            db.session.commit()
            return {'message': 'Child updated successfully.'}, 200
        return {'message': 'Child not found'}, 404

    def delete(self, child_id):
        child = Child.query.get(child_id)
        if child:
            db.session.delete(child)
            db.session.commit()
            return {'message': 'Child deleted successfully.'}, 204
        return {'message': 'Child not found'}, 404
    

# Parser for Blog data
blog_parser = reqparse.RequestParser()
blog_parser.add_argument('title', type=str, required=True, help="Title cannot be blank")
blog_parser.add_argument('content', type=str, required=True, help="Content cannot be blank")
blog_parser.add_argument('content_type', type=str, required=True, help="Content Type cannot be blank")

class BlogResource(Resource):
    def get(self, blog_id=None):
        if blog_id is None:
            blogs = Blog.query.all()
            blog_data = [{
                'id': blog.id, 
                'title': blog.title, 
                'content': blog.content, 
                'content_type': blog.content_type, 
                'created_at': blog.created_at.strftime('%Y-%m-%d %H:%M:%S')
            } for blog in blogs]
            return blog_data, 200
        else:
            blog = Blog.query.get(blog_id)
            if blog:
                return {
                    'id': blog.id, 
                    'title': blog.title, 
                    'content': blog.content, 
                    'content_type': blog.content_type, 
                    'created_at': blog.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }, 200
            return {'message': 'Blog not found'}, 404

    def post(self):
        args = blog_parser.parse_args()
        blog = Blog(
            title=args['title'], 
            content=args['content'], 
            content_type=args['content_type']
        )
        db.session.add(blog)
        db.session.commit()
        return {'id': blog.id, 'message': 'Blog created successfully.'}, 201

    def put(self, blog_id):
        blog = Blog.query.get(blog_id)
        if blog:
            args = blog_parser.parse_args()
            blog.title = args['title']
            blog.content = args['content']
            blog.content_type = args['content_type']
            db.session.commit()
            return {'message': 'Blog updated successfully.'}, 200
        return {'message': 'Blog not found'}, 404

    def delete(self, blog_id):
        blog = Blog.query.get(blog_id)
        if blog:
            db.session.delete(blog)
            db.session.commit()
            return {'message': 'Blog deleted successfully.'}, 204
        return {'message': 'Blog not found'}, 404

class HomeFeedResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        children = Child.query.filter_by(parent_id=user_id)
        feeds = []
        for child in children:
            age = (datetime.now().date() - child.date_of_birth).days // 365
            relevant_blogs = Blog.query.join(BlogMetadata).filter(BlogMetadata.recommended_age_range.contains(str(age)))
            for blog in relevant_blogs:
                feeds.append({'title': blog.title, 'content': blog.content, 'content_type': blog.content_type})
        return jsonify(feeds)


