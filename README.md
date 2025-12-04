# PQC Document Authentication Service

A web-based document authentication system using **FAEST** post-quantum digital signatures via the PyFAEST library.

## Features

- 📄 **Document Signing** - Upload and sign documents with FAEST post-quantum signatures
- ✅ **Signature Verification** - Verify document authenticity without login
- 🔐 **Multiple Parameter Sets** - Choose from 12 FAEST variants (128f, 128s, 192f, etc.)
- 📊 **Performance Metrics** - Real-time signing and verification timing
- 🗄️ **Audit Trail** - SQLite database tracks all signatures
- 🎨 **Modern UI** - Responsive Bootstrap interface
- 🔄 **REST API** - Programmatic access to signing/verification

## Tech Stack

- **Backend**: Flask (Python 3.8+)
- **Cryptography**: PyFAEST (FAEST post-quantum signatures)
- **Database**: SQLite
- **Frontend**: HTML/CSS/JavaScript with Bootstrap 5
- **Hashing**: SHA-256 for document fingerprints

## Project Structure

```
pqc-document-auth/
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── routes.py             # API endpoints
│   ├── models.py             # Database models
│   ├── crypto_utils.py       # FAEST signing/verification
│   ├── templates/
│   │   ├── base.html         # Base template
│   │   ├── index.html        # Home page
│   │   ├── sign.html         # Document signing page
│   │   └── verify.html       # Verification page
│   └── static/
│       └── css/
│           └── style.css     # Custom styles
├── uploads/                   # Temporary document storage
├── keys/                      # Generated keypairs
├── instance/                  # SQLite database (auto-created)
├── config.py                  # Configuration
├── run.py                     # Application entry point
├── requirements.txt           # Python dependencies
├── .gitignore
└── README.md
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Linux (native or WSL), or macOS
- pip and venv

### Setup

```bash
# Clone or navigate to project directory
cd pqc-document-auth

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows WSL: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python run.py init-db

# Run the application
python run.py
```

The application will start at `http://localhost:5000`

## Usage

### Web Interface

1. **Home Page** (`/`)
   - Overview and features
   - Quick links to sign/verify

2. **Sign Document** (`/sign`)
   - Upload a file (PDF, image, text, etc.)
   - Select FAEST parameter set (128f, 128s, 192f, etc.)
   - Generate or use existing keypair
   - Download signature file
   - View performance metrics

3. **Verify Signature** (`/verify`)
   - Upload document and signature file
   - Provide public key
   - See verification result
   - View signature details

### API Endpoints

#### Generate Keypair
```bash
POST /api/keypair
Content-Type: application/json

{
  "param_set": "128f"
}

Response:
{
  "public_key": "hex_encoded_key",
  "private_key": "hex_encoded_key",
  "param_set": "128f"
}
```

#### Sign Document
```bash
POST /api/sign
Content-Type: multipart/form-data

Fields:
- file: document file
- param_set: "128f" | "128s" | "192f" | ...
- private_key: hex encoded private key

Response:
{
  "signature": "hex_encoded_signature",
  "document_hash": "sha256_hash",
  "signature_size": 5924,
  "signing_time_ms": 5.2,
  "param_set": "128f"
}
```

#### Verify Signature
```bash
POST /api/verify
Content-Type: multipart/form-data

Fields:
- file: document file
- signature: hex encoded signature
- public_key: hex encoded public key

Response:
{
  "valid": true,
  "document_hash": "sha256_hash",
  "verification_time_ms": 4.8,
  "param_set": "128f"
}
```

## FAEST Parameter Sets

| Parameter Set | Security Level | Signature Size | Speed |
|--------------|----------------|----------------|-------|
| `128f`       | NIST Level 1  | 5,924 bytes    | Fast  |
| `128s`       | NIST Level 1  | 4,506 bytes    | Small |
| `192f`       | NIST Level 3  | 14,948 bytes   | Fast  |
| `192s`       | NIST Level 3  | 11,260 bytes   | Small |
| `256f`       | NIST Level 5  | 26,548 bytes   | Fast  |
| `256s`       | NIST Level 5  | 20,696 bytes   | Small |
| `em_128f`    | NIST Level 1  | 5,060 bytes    | Fast  |
| `em_128s`    | NIST Level 1  | 3,906 bytes    | Small |
| `em_192f`    | NIST Level 3  | 12,380 bytes   | Fast  |
| `em_192s`    | NIST Level 3  | 9,340 bytes    | Small |
| `em_256f`    | NIST Level 5  | 23,476 bytes   | Fast  |
| `em_256s`    | NIST Level 5  | 17,984 bytes   | Small |

## Database Schema

### `signatures` table
- `id` - Auto-incrementing primary key
- `document_hash` - SHA-256 hash of document
- `signature` - FAEST signature (hex)
- `public_key` - Public key (hex)
- `param_set` - FAEST parameter set used
- `signature_size` - Size in bytes
- `signing_time` - Time taken to sign (ms)
- `timestamp` - Creation timestamp

## Security Considerations

⚠️ **Important Notes:**

- This is a **demonstration/research project** for academic purposes
- FAEST is still under NIST evaluation (not yet standardized)
- The reference implementation is not optimized for production
- Private keys are stored temporarily - use secure storage for production
- No authentication system - anyone can access the service
- Uploaded files are stored temporarily and should be cleaned periodically

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Adding New Features
- See `CONTRIBUTING.md` for contribution guidelines
- Follow Flask best practices
- Add tests for new functionality

## Use Cases

- **Research**: Compare FAEST with classical signature schemes
- **Education**: Demonstrate post-quantum cryptography
- **Prototyping**: Test FAEST in document workflows
- **Benchmarking**: Measure signature sizes and performance

## Troubleshooting

**"Module not found: pyfaest"**
```bash
pip install pyfaest
```

**"Database not found"**
```bash
python run.py init-db
```

**"Permission denied" on uploads**
```bash
chmod 755 uploads/
```

## References

- [PyFAEST](https://github.com/Shreyas582/pyfaest) - Python bindings for FAEST
- [FAEST Specification](https://faest.info/faest-spec-v2.0.pdf)
- [NIST PQC Project](https://csrc.nist.gov/projects/post-quantum-cryptography)

## License

MIT License - See LICENSE file

## Author

Created for NYU Post-Quantum Cryptography Course (Fall 2025)

## Acknowledgments

Built on top of PyFAEST and the FAEST reference implementation.
