"""
Flask routes and API endpoints
"""
from flask import Blueprint, render_template, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
from app import db
from app.models import Signature
from app.crypto_utils import generate_keypair, sign_document, verify_signature
import os

bp = Blueprint('main', __name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@bp.route('/sign')
def sign_page():
    """Document signing page"""
    param_sets = current_app.config['PARAM_SETS']
    param_set_info = current_app.config['PARAM_SET_INFO']
    return render_template('sign.html', param_sets=param_sets, param_set_info=param_set_info)

@bp.route('/verify')
def verify_page():
    """Signature verification page"""
    param_sets = current_app.config['PARAM_SETS']
    return render_template('verify.html', param_sets=param_sets)

@bp.route('/api/keypair', methods=['POST'])
def api_generate_keypair():
    """Generate a new FAEST keypair"""
    data = request.get_json()
    param_set = data.get('param_set', '128f')
    
    if param_set not in current_app.config['PARAM_SETS']:
        return jsonify({'error': 'Invalid parameter set'}), 400
    
    try:
        public_key_hex, private_key_hex = generate_keypair(param_set)
        return jsonify({
            'public_key': public_key_hex,
            'private_key': private_key_hex,
            'param_set': param_set
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/sign', methods=['POST'])
def api_sign():
    """Sign a document"""
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    # Get parameters
    param_set = request.form.get('param_set', '128f')
    private_key_hex = request.form.get('private_key')
    
    if not private_key_hex:
        return jsonify({'error': 'Private key required'}), 400
    
    if param_set not in current_app.config['PARAM_SETS']:
        return jsonify({'error': 'Invalid parameter set'}), 400
    
    try:
        # Sign the document
        result = sign_document(file.stream, param_set, private_key_hex)
        
        # Get public key (for storage)
        public_key_hex = request.form.get('public_key', '')
        
        # Store in database
        signature_record = Signature(
            document_hash=result['document_hash'],
            signature=result['signature'],
            public_key=public_key_hex,
            param_set=param_set,
            signature_size=result['signature_size'],
            signing_time=result['signing_time_ms']
        )
        db.session.add(signature_record)
        db.session.commit()
        
        result['id'] = signature_record.id
        result['param_set'] = param_set
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/verify', methods=['POST'])
def api_verify():
    """Verify a document signature"""
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Get parameters
    signature_hex = request.form.get('signature')
    public_key_hex = request.form.get('public_key')
    param_set = request.form.get('param_set', '128f')
    
    if not signature_hex or not public_key_hex:
        return jsonify({'error': 'Signature and public key required'}), 400
    
    if param_set not in current_app.config['PARAM_SETS']:
        return jsonify({'error': 'Invalid parameter set'}), 400
    
    try:
        result = verify_signature(file.stream, signature_hex, public_key_hex, param_set)
        result['param_set'] = param_set
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/signatures')
def api_list_signatures():
    """List recent signatures"""
    limit = request.args.get('limit', 10, type=int)
    signatures = Signature.query.order_by(Signature.timestamp.desc()).limit(limit).all()
    return jsonify([sig.to_dict() for sig in signatures])

@bp.route('/api/signatures/<int:sig_id>')
def api_get_signature(sig_id):
    """Get signature details"""
    signature = Signature.query.get_or_404(sig_id)
    return jsonify(signature.to_dict())
