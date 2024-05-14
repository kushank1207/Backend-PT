import os
import sys
from faker import Faker
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from app.app import app, db
from app.models import User, Child, Blog, BlogMetadata

fake = Faker()

def add_users(num_users=100):
    for _ in range(num_users):
        user = User(
            name=fake.name(),
            email=fake.email(),
            parent_type=random.choice(['first-time', 'experienced'])
        )
        db.session.add(user)
    db.session.commit()

def add_children(num_children_per_user=3):
    users = User.query.all()
    for user in users:
        for _ in range(random.randint(1, num_children_per_user)):
            child = Child(
                parent_id=user.id,
                name=fake.name(),
                date_of_birth=fake.date_of_birth(minimum_age=0, maximum_age=12),
                gender=random.choice(['male', 'female', 'other'])
            )
            db.session.add(child)
    db.session.commit()

def add_blogs(num_blogs_per_user=5):
    age_ranges = ['0-1', '1-3', '3-7', '7-11', '11-16']
    tags_options = ['education', 'parenting', 'health', 'activities', 'nutrition', 'development', 'first-time', 'experienced', 'baby-care', 'special-needs', 'reviews', 'behaviour', 'child-safety', 'environment']

    users = User.query.all()
    for user in users:
        for _ in range(random.randint(1, num_blogs_per_user)):
            blog = Blog(
                title=fake.sentence(),
                content=fake.text(max_nb_chars=2000),
                content_type=random.choice(['blog', 'vlog'])
            )
            db.session.add(blog)
            db.session.flush()

            metadata = BlogMetadata(
                blog_id=blog.id,
                tags=','.join(random.sample(tags_options, k=random.randint(1, 3))),
                recommended_age_range=random.choice(age_ranges)
            )
            db.session.add(metadata)
    db.session.commit()

if __name__ == '__main__':
    try:
        with app.app_context():
            add_users(10)
            add_children(8)
            add_blogs(20)
    except Exception as e:
        print(f"An error occurred: {e}")
