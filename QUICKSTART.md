# Quick Start Guide

## Setup (5 minutes)

```bash
# Navigate to project
cd pqc-document-auth

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows WSL: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

Open browser to: http://localhost:5000

## Usage

### 1. Sign a Document

1. Go to "Sign Document" page
2. Click "Generate New Keypair" (select parameter set first)
3. Copy and save your public and private keys
4. Upload a document (PDF, image, text file)
5. The private key will be auto-filled
6. Click "Sign Document"
7. Copy or download the signature

### 2. Verify a Signature

1. Go to "Verify Signature" page
2. Upload the same document
3. Select the same parameter set used for signing
4. Paste the public key
5. Paste the signature
6. Click "Verify Signature"

## API Examples

### Generate Keypair
```bash
curl -X POST http://localhost:5000/api/keypair \
  -H "Content-Type: application/json" \
  -d '{"param_set": "128f"}'
```

### Sign Document
```bash
curl -X POST http://localhost:5000/api/sign \
  -F "file=@document.pdf" \
  -F "param_set=128f" \
  -F "private_key=YOUR_PRIVATE_KEY_HEX"
```

### Verify Signature
```bash
curl -X POST http://localhost:5000/api/verify \
  -F "file=@document.pdf" \
  -F "param_set=128f" \
  -F "public_key=YOUR_PUBLIC_KEY_HEX" \
  -F "signature=YOUR_SIGNATURE_HEX"
```

## Troubleshooting

**Import errors?**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Database errors?**
```bash
rm -rf instance/
python run.py init-db
```

**Port already in use?**
Edit run.py and change port 5000 to another port.

## Next Steps

- Try different FAEST parameter sets (128f, 128s, 192f, etc.)
- Compare signature sizes and performance
- Test with different file types
- Modify a signed document and verify (should fail)
- Use the API to integrate with other applications
