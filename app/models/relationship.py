import datetime
from app import db

class Relationship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    related_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    relationship_type = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.UTC)

    __table_args__ = (
        db.Index('ix_user_related_user', 'user_id', 'related_user_id'),
        db.Index('ix_relationship_type', 'relationship_type')
    )
