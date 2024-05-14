from .app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    parent_type = db.Column(db.String(50), nullable=False)

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_type = db.Column(db.String(50), nullable=False)  # 'blog'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BlogMetadata(db.Model):
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), primary_key=True)
    tags = db.Column(db.String(200), nullable=False)
    recommended_age_range = db.Column(db.String(50), nullable=False)
