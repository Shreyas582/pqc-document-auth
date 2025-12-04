"""
Cryptographic utilities for FAEST signatures
"""
import hashlib
import time
from faest import Keypair, sign, verify as faest_verify

def hash_file(file_stream):
    """
    Compute SHA-256 hash of a file
    
    Args:
        file_stream: File-like object
        
    Returns:
        str: Hex-encoded SHA-256 hash
    """
    sha256 = hashlib.sha256()
    file_stream.seek(0)
    
    # Read file in chunks to handle large files
    while chunk := file_stream.read(8192):
        sha256.update(chunk)
    
    file_stream.seek(0)
    return sha256.hexdigest()

def generate_keypair(param_set='128f'):
    """
    Generate a FAEST keypair
    
    Args:
        param_set: FAEST parameter set
        
    Returns:
        tuple: (public_key_hex, private_key_hex)
    """
    keypair = Keypair.generate(param_set)
    public_key_hex = keypair.public_key.to_bytes().hex()
    private_key_hex = keypair.private_key.to_bytes().hex()
    return public_key_hex, private_key_hex

def sign_document(file_stream, param_set, private_key_hex):
    """
    Sign a document using FAEST
    
    Args:
        file_stream: File-like object
        param_set: FAEST parameter set
        private_key_hex: Private key in hex format
        
    Returns:
        dict: {
            'signature': hex string,
            'document_hash': hex string,
            'signature_size': int,
            'signing_time_ms': float
        }
    """
    from faest import PrivateKey
    
    # Compute document hash
    document_hash = hash_file(file_stream)
    message = bytes.fromhex(document_hash)
    
    # Reconstruct private key
    private_key_bytes = bytes.fromhex(private_key_hex)
    private_key = PrivateKey(private_key_bytes, param_set)
    
    # Sign the message
    start_time = time.time()
    signature = sign(message, private_key)
    signing_time = (time.time() - start_time) * 1000  # Convert to ms
    
    signature_hex = signature.hex()
    
    return {
        'signature': signature_hex,
        'document_hash': document_hash,
        'signature_size': len(signature),
        'signing_time_ms': round(signing_time, 2)
    }

def verify_signature(file_stream, signature_hex, public_key_hex, param_set):
    """
    Verify a document signature
    
    Args:
        file_stream: File-like object
        signature_hex: Signature in hex format
        public_key_hex: Public key in hex format
        param_set: FAEST parameter set
        
    Returns:
        dict: {
            'valid': bool,
            'document_hash': hex string,
            'verification_time_ms': float
        }
    """
    from faest import PublicKey
    
    # Compute document hash
    document_hash = hash_file(file_stream)
    message = bytes.fromhex(document_hash)
    
    # Reconstruct public key and signature
    public_key_bytes = bytes.fromhex(public_key_hex)
    public_key = PublicKey(public_key_bytes, param_set)
    signature = bytes.fromhex(signature_hex)
    
    # Verify signature
    start_time = time.time()
    try:
        is_valid = faest_verify(message, signature, public_key)
        verification_time = (time.time() - start_time) * 1000
        
        return {
            'valid': is_valid,
            'document_hash': document_hash,
            'verification_time_ms': round(verification_time, 2)
        }
    except Exception as e:
        verification_time = (time.time() - start_time) * 1000
        return {
            'valid': False,
            'document_hash': document_hash,
            'verification_time_ms': round(verification_time, 2),
            'error': str(e)
        }
