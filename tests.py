import os
from datetime import datetime, timezone, timedelta

from app.enums.gender_enums import GenderEnum

os.environ['DATABASE_URL'] = 'sqlite://'

import unittest
from app import app, db
from app.models import User, Post


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        user = User(username='anuzpandey', email='anuzpandey@gmail.com')
        user.set_password('Batman')
        self.assertFalse(user.check_password('Superman'))
        self.assertTrue(user.check_password('Batman'))

    def test_avatar(self):
        user = User(username='anuzpandey', email='anuzpandey@gmail.com', gender=GenderEnum.MALE.value)
        self.assertEqual(user.avatar(), 'https://avatar.iran.liara.run/public/boy?username=anuzpandey')

    def test_follow(self):
        user1 = User(username='anuzpandey', email='anuzpandey@gmail.com')
        user2 = User(username='batman', email='batman@gmail.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        following = db.session.scalars(user1.following.select()).all()
        followers = db.session.scalars(user2.followers.select()).all()
        self.assertEqual(following, [])
        self.assertEqual(followers, [])

        user1.follow(user2)
        db.session.commit()
        self.assertTrue(user1.is_following(user2))
        self.assertEqual(user1.following_count(), 1)
        self.assertEqual(user2.followers_count(), 1)
        user1_following = db.session.scalars(user1.following.select()).all()
        user2_followers = db.session.scalars(user2.followers.select()).all()
        self.assertEqual(user1_following[0].username, 'batman')
        self.assertEqual(user2_followers[0].username, 'anuzpandey')

        user1.unfollow(user2)
        db.session.commit()
        self.assertFalse(user1.is_following(user2))
        self.assertEqual(user1.following_count(), 0)
        self.assertEqual(user2.followers_count(), 0)

    def test_follow_post(self):
        user1 = User(username='anuzpandey', email='anuzpandey@gmail.com')
        user2 = User(username='batman', email='batman@gmail.com')
        user3 = User(username='superman', email='superman@gmail.com')
        user4 = User(username='spiderman', email='spiderman@gmail.com')
        db.session.add_all([user1, user2, user3, user4])

        # Create four posts
        now = datetime.now(timezone.utc)
        post1 = Post(title="Post #1 - anuzpandey", body="Post from anuzpandey", author=user1, created_at=now + timedelta(seconds=1))
        post2 = Post(title="Post #1 - batman", body="Post from batman", author=user2, created_at=now + timedelta(seconds=4))
        post3 = Post(title="Post #1 - superman", body="Post from superman", author=user3, created_at=now + timedelta(seconds=3))
        post4 = Post(title="Post #1 - spiderman", body="Post from spiderman", author=user4, created_at=now + timedelta(seconds=2))
        db.session.add_all([post1, post2, post3, post4])
        db.session.commit()

        # Set up followers
        user1.follow(user2)
        user1.follow(user4)
        user2.follow(user3)
        user3.follow(user4)
        db.session.commit()

        # Check the following posts of each user
        following_post1 = db.session.scalars(user1.following_posts()).all()
        following_post2 = db.session.scalars(user2.following_posts()).all()
        following_post3 = db.session.scalars(user3.following_posts()).all()
        following_post4 = db.session.scalars(user4.following_posts()).all()
        self.assertEqual(following_post1, [post2, post4, post1])
        self.assertEqual(following_post2, [post2, post3])
        self.assertEqual(following_post3, [post3, post4])
        self.assertEqual(following_post4, [post4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
