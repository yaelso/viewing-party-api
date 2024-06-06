from app import db, bcrypt
from app.models.relationship import Relationship

class User(db.Model):
    """
    A class to represent a single user.

    Attributes:
        id (int): Primary key identifier
        username (str): User's uniquely identifying username
        email (str): User's email
        password_hash (str): Hash of user's password
        created_at (datetime): Timestamp for data integrity, audit trail, and analytics
        friendships (relationship): Collection of user friendships
        blocked_users (relationship): Collection of user blocks

    Methods:
        _optional_serialization_keys: Mixin for specifying model-unique attributes that should be included when serializing.

        set_password: Generates a password hash based on a user's provided password.
        check_password: Checks password hash against provided password.
        update_password: Updates password hash.
        update_email: Updates email.

        is_friend: Checks if a given user is currently a friend.
        add_friend: Adds a user as a friend.
        remove_friend: Removes target user from friends list.
        is_blocked: Checks if a given user is currently blocked.
        block_user: Blocks a user.
        unblock_user: Removes target user from blocked list.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=None)
    friendships = db.relationship("Relationship", foreign_keys="Relationship.user_id", backref=db.backref("user", lazy="joined"), lazy="dynamic")
    blocked_users = db.relationship("Relationship", foreign_keys="Relationship.user_id", backref=db.backref("blocked_by", lazy="joined"), lazy="dynamic")

    _serialization_keys = ["id", "username", "email", "password_hash"]
    _deserialization_keys = ["username", "email"]

    __table_args__ = (
        db.Index("ix_username", "username"),
        db.Index("ix_email", "email")
    )

    @classmethod
    def _optional_serialization_keys(cls):
        return ["created_at", "friendships", "blocked_users"]

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def update_password(self, new_password):
        self.password_hash = bcrypt.generate_password_hash(new_password).decode("utf8")
        db.session.commit()

    def update_email(self, new_email):
        self.email = new_email
        db.session.commit()

    def is_friend(self, user):
        return self.friendships.filter_by(related_user_id=user.id, relationship_type="friend").first() is not None

    def add_friend(self, friend):
        if not self.is_friend(friend):
            friendship = Relationship(user_id=self.id, related_user_id=friend.id, relationship_type="friend")
            db.session.add(friendship)
            db.session.commit()

    def remove_friend(self, friend):
        friendship = self.friendships.filter_by(related_user_id=friend.id).first()
        if friendship:
            db.session.delete(friendship)
            db.session.commit()

    def is_blocked(self, user):
        return self.blocked_users.filter_by(related_user_id=user.id, relationship_type="blocked").first() is not None

    def block_user(self, user):
        if not self.is_blocked(user):
            block = Relationship(user_id=self.id, related_user_id=user.id, relationship_type="blocked")
            db.session.add(block)
            db.session.commit()

    def unblock_user(self, user):
        block = self.blocked_users.filter_by(related_user_id=user.id).first()
        if block:
            db.session.delete(block)
            db.session.commit()
