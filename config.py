"""
Configuration file with hardcoded secrets
WARNING: This file intentionally contains security vulnerabilities for testing!
"""

# ==================== DATABASE CREDENTIALS ====================
DATABASE_HOST = "localhost"
DATABASE_PORT = 3306
DATABASE_NAME = "vulnerable_db"
DATABASE_USER = "root"
DATABASE_PASSWORD = "root123"  # CWE-798: Hardcoded Password
DATABASE_URL = f"mysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# MongoDB credentials
MONGODB_URI = "mongodb://admin:password123@localhost:27017/vulnerable"

# PostgreSQL credentials
POSTGRES_CONNECTION = "postgresql://postgres:postgres123@localhost:5432/mydb"

# ==================== API KEYS ====================
# AWS Credentials (CWE-798)
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION = "us-east-1"

# Google Cloud
GOOGLE_API_KEY = "AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GOOGLE_CLIENT_SECRET = "GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Azure
AZURE_SUBSCRIPTION_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
AZURE_CLIENT_SECRET = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# Stripe
STRIPE_SECRET_KEY = "sk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
STRIPE_PUBLISHABLE_KEY = "pk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
STRIPE_WEBHOOK_SECRET = "whsec_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# PayPal
PAYPAL_CLIENT_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
PAYPAL_CLIENT_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Twilio
TWILIO_ACCOUNT_SID = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# SendGrid
SENDGRID_API_KEY = "SG.xxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# GitHub
GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GITHUB_CLIENT_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Slack
SLACK_BOT_TOKEN = "xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx"
SLACK_SIGNING_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"

# Firebase
FIREBASE_API_KEY = "AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
FIREBASE_AUTH_DOMAIN = "project-id.firebaseapp.com"
FIREBASE_DATABASE_URL = "https://project-id.firebaseio.com"

# Twitter/X
TWITTER_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxx"
TWITTER_API_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# OpenAI
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# ==================== ENCRYPTION KEYS ====================
# Weak/hardcoded encryption keys (CWE-321)
SECRET_KEY = "super_secret_key_123"
JWT_SECRET = "jwt_secret_key_do_not_share"
ENCRYPTION_KEY = "1234567890abcdef"
AES_KEY = "0123456789ABCDEF0123456789ABCDEF"
RSA_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA0Z3VS5JJcds3xfn/ygWyF8PbnGy0AHB7MvXIJNRjzdPwJxXU
...(truncated for example)...
-----END RSA PRIVATE KEY-----"""

# ==================== ADMIN CREDENTIALS ====================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
ADMIN_EMAIL = "admin@vulnerable.com"

SUPER_ADMIN_PASSWORD = "SuperSecr3t!"
ROOT_PASSWORD = "toor"

# Default user credentials
DEFAULT_USERS = [
    {"username": "admin", "password": "admin123", "role": "admin"},
    {"username": "user", "password": "user123", "role": "user"},
    {"username": "test", "password": "test123", "role": "user"},
    {"username": "guest", "password": "guest", "role": "guest"},
]

# ==================== SSH/SERVER CREDENTIALS ====================
SSH_USERNAME = "deploy"
SSH_PASSWORD = "deploy123"
SSH_PRIVATE_KEY = """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAACFw...
-----END OPENSSH PRIVATE KEY-----"""

FTP_USERNAME = "ftpuser"
FTP_PASSWORD = "ftp123"

# ==================== OAUTH SECRETS ====================
OAUTH_CLIENT_ID = "xxxxxxxxxxxx.apps.googleusercontent.com"
OAUTH_CLIENT_SECRET = "GOCSPX-xxxxxxxxxxxxxxxxxxxxx"

FACEBOOK_APP_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
LINKEDIN_CLIENT_SECRET = "xxxxxxxxxxxxxxxx"

# ==================== SESSION CONFIGURATION ====================
SESSION_COOKIE_SECURE = False  # Should be True in production
SESSION_COOKIE_HTTPONLY = False  # Should be True
SESSION_COOKIE_SAMESITE = None  # Should be 'Strict' or 'Lax'

# ==================== DEBUG SETTINGS ====================
DEBUG = True  # Should be False in production
TESTING = True
DEVELOPMENT = True

# Verbose error messages (information disclosure)
PROPAGATE_EXCEPTIONS = True
TRAP_HTTP_EXCEPTIONS = True

# ==================== INSECURE CONFIGURATIONS ====================
ALLOWED_HOSTS = ["*"]  # Too permissive
CORS_ORIGINS = ["*"]  # Too permissive
UPLOAD_FOLDER = "/tmp/uploads"  # Insecure location
MAX_CONTENT_LENGTH = None  # No limit - DoS vulnerability

# SQL Alchemy with echo (logs all queries including sensitive data)
SQLALCHEMY_ECHO = True

# Disable CSRF protection
WTF_CSRF_ENABLED = False
CSRF_ENABLED = False

# ==================== INTERNAL URLS (SSRF targets) ====================
INTERNAL_API_URL = "http://internal-api.local:8080"
ADMIN_PANEL_URL = "http://admin.internal:9000"
METADATA_URL = "http://169.254.169.254/latest/meta-data/"
