"""
Database models for signature storage
"""
from app import db
from datetime import datetime

class Signature(db.Model):
    """Model for storing document signatures"""
    __tablename__ = 'signatures'
    
    id = db.Column(db.Integer, primary_key=True)
    document_hash = db.Column(db.String(64), nullable=False, index=True)
    signature = db.Column(db.Text, nullable=False)
    public_key = db.Column(db.Text, nullable=False)
    param_set = db.Column(db.String(20), nullable=False)
    signature_size = db.Column(db.Integer, nullable=False)
    signing_time = db.Column(db.Float, nullable=False)  # milliseconds
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Signature {self.id} - {self.param_set} - {self.document_hash[:8]}...>'
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'document_hash': self.document_hash,
            'signature': self.signature,
            'public_key': self.public_key,
            'param_set': self.param_set,
            'signature_size': self.signature_size,
            'signing_time_ms': self.signing_time,
            'timestamp': self.timestamp.isoformat()
        }
