import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///signatures.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'txt', 'doc', 'docx'}
    
    # Keys folder
    KEYS_FOLDER = 'keys'
    
    # FAEST parameter sets
    PARAM_SETS = [
        '128f', '128s',
        '192f', '192s',
        '256f', '256s',
        'em_128f', 'em_128s',
        'em_192f', 'em_192s',
        'em_256f', 'em_256s'
    ]
    
    PARAM_SET_INFO = {
        '128f': {'security': 'NIST Level 1', 'sig_size': 5924, 'type': 'Fast'},
        '128s': {'security': 'NIST Level 1', 'sig_size': 4506, 'type': 'Small'},
        '192f': {'security': 'NIST Level 3', 'sig_size': 14948, 'type': 'Fast'},
        '192s': {'security': 'NIST Level 3', 'sig_size': 11260, 'type': 'Small'},
        '256f': {'security': 'NIST Level 5', 'sig_size': 26548, 'type': 'Fast'},
        '256s': {'security': 'NIST Level 5', 'sig_size': 20696, 'type': 'Small'},
        'em_128f': {'security': 'NIST Level 1 (EM)', 'sig_size': 5060, 'type': 'Fast'},
        'em_128s': {'security': 'NIST Level 1 (EM)', 'sig_size': 3906, 'type': 'Small'},
        'em_192f': {'security': 'NIST Level 3 (EM)', 'sig_size': 12380, 'type': 'Fast'},
        'em_192s': {'security': 'NIST Level 3 (EM)', 'sig_size': 9340, 'type': 'Small'},
        'em_256f': {'security': 'NIST Level 5 (EM)', 'sig_size': 23476, 'type': 'Fast'},
        'em_256s': {'security': 'NIST Level 5 (EM)', 'sig_size': 17984, 'type': 'Small'},
    }
