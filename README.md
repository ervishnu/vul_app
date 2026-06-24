# 🔓 Vulnerable Web Application for Security Testing

> ⚠️ **WARNING**: This application contains **intentional security vulnerabilities**. It is designed for educational purposes, security training, and testing SAST/DAST tools. **DO NOT deploy in production or expose to the internet!!**

## 📋 Overview

This is a deliberately vulnerable Flask web application similar to DVWA, WebGoat, or OWASP Juice Shop. It's designed to help security professionals and developers:

- Learn about common web vulnerabilities
- Practice penetration testing techniques
- Test Static Application Security Testing (SAST) tools
- Test Dynamic Application Security Testing (DAST) tools
- Understand secure coding practices by seeing what NOT to do

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t vulnerable-app .
docker run -p 5000:5000 vulnerable-app
```

### Running Locally

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Access the application at: **http://localhost:5000**

## 🔴 Vulnerability Categories

### 1. Injection Vulnerabilities

| Vulnerability | Endpoint | CWE |
|--------------|----------|-----|
| SQL Injection | `/sql-injection` | CWE-89 |
| Command Injection | `/command-injection` | CWE-78 |
| NoSQL Injection | `/nosql` | CWE-943 |
| SSTI (Template Injection) | `/ssti` | CWE-1336 |
| XXE Injection | `/xxe` | CWE-611 |

### 2. Cross-Site Scripting (XSS)

| Type | Endpoint | CWE |
|------|----------|-----|
| Reflected XSS | `/xss?search=<payload>` | CWE-79 |
| Stored XSS | `/xss` (comment form) | CWE-79 |
| DOM-based XSS | `/xss#<payload>` | CWE-79 |
| CSS Injection | `/css-injection` | CWE-79 |

### 3. Code Execution

| Vulnerability | Endpoint | CWE |
|--------------|----------|-----|
| Remote Code Execution (eval) | `/rce` | CWE-94 |
| Insecure Deserialization | `/deserialize` | CWE-502 |
| Remote File Inclusion | `/rfi` | CWE-98 |
| Local File Inclusion | `/lfi` | CWE-22 |

### 4. Authentication & Session

| Vulnerability | Endpoint | CWE |
|--------------|----------|-----|
| SQL Injection Login Bypass | `/login` | CWE-89 |
| Weak Session Management | `/login` | CWE-384 |
| Insecure Cookies | All authenticated pages | CWE-614 |
| CSRF | `/csrf`, `/transfer` | CWE-352 |

### 5. Access Control

| Vulnerability | Endpoint | CWE |
|--------------|----------|-----|
| IDOR | `/user/<id>` | CWE-639 |
| Broken Access Control | `/admin` | CWE-284 |
| Mass Assignment | `/register` | CWE-915 |

### 6. Security Misconfiguration

| Vulnerability | Location | CWE |
|--------------|----------|-----|
| Debug Mode Enabled | `app.py` | CWE-489 |
| Hardcoded Credentials | `config.py`, `.env` | CWE-798 |
| Information Disclosure | `/debug` | CWE-200 |
| Insecure File Upload | `/upload` | CWE-434 |
| Open Redirect | `/redirect` | CWE-601 |

### 7. Cryptographic Issues

| Vulnerability | Location | CWE |
|--------------|----------|-----|
| Weak Hashing (MD5) | `/crypto` | CWE-327 |
| Hardcoded Encryption Keys | `config.py` | CWE-321 |
| Base64 as "Encryption" | `/crypto` | CWE-327 |

## 🧪 Testing Payloads

### SQL Injection
```sql
' OR '1'='1
' OR '1'='1' --
admin'--
' UNION SELECT * FROM users --
```

### XSS
```html
<script>alert('XSS')</script>
<img src=x onerror="alert('XSS')">
<svg onload="alert('XSS')">
```

### Command Injection
```bash
; ls -la
| cat /etc/passwd
`whoami`
$(id)
```

### SSTI (Jinja2)
```python
{{ 7*7 }}
{{ config }}
{{ ''.__class__.__mro__[1].__subclasses__() }}
```

### LFI/Path Traversal
```
../../../etc/passwd
....//....//....//etc/passwd
/proc/self/environ
```

## 🔍 SAST Tool Testing

This application should trigger findings for:

- **Hardcoded Secrets**: AWS keys, API keys, passwords in `config.py`, `.env`, `app.py`
- **SQL Injection**: String concatenation in SQL queries
- **Command Injection**: `subprocess` with `shell=True`
- **Insecure Deserialization**: `pickle.loads()` on user input
- **Code Injection**: Use of `eval()` on user input
- **Weak Cryptography**: MD5 hashing, hardcoded keys
- **Debug Mode**: `app.run(debug=True)`
- **Missing CSRF Protection**: Forms without tokens

### Recommended SAST Tools
- Semgrep
- Bandit (Python)
- SonarQube
- Checkmarx
- Snyk Code
- GitHub CodeQL

## 🌐 DAST Tool Testing

This application is ideal for testing:

- **OWASP ZAP**
- **Burp Suite**
- **Nikto**
- **SQLMap**
- **Nuclei**
- **Acunetix**

### DAST Testing Tips

1. **Spider/Crawl** the application first
2. **Authenticate** at `/login` (admin:admin123)
3. **Fuzz** all input parameters
4. Check for **CORS misconfigurations**
5. Test **rate limiting** (there is none!)

## 📁 Project Structure

```
Vul_App/
├── app.py              # Main Flask application
├── config.py           # Hardcoded secrets
├── .env                # Environment variables with secrets
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
├── README.md           # This file
├── templates/          # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── sql_injection.html
│   ├── xss.html
│   ├── command_injection.html
│   ├── rce.html
│   ├── rfi.html
│   ├── lfi.html
│   ├── csrf.html
│   ├── css_injection.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── admin.html
│   ├── xxe.html
│   ├── ssti.html
│   ├── upload.html
│   ├── crypto.html
│   └── nosql.html
└── static/
    └── uploads/        # Insecure upload directory
```

## 🛡️ Secure Alternatives

For each vulnerability, here's what you SHOULD do:

| Vulnerability | Secure Practice |
|--------------|-----------------|
| SQL Injection | Use parameterized queries / ORM |
| XSS | Escape output, use CSP headers |
| Command Injection | Avoid shell=True, use subprocess.run with list |
| CSRF | Implement CSRF tokens (Flask-WTF) |
| Hardcoded Secrets | Use environment variables, secret managers |
| File Upload | Validate type, size, sanitize filename |
| Weak Crypto | Use bcrypt/scrypt for passwords, AES-256 for encryption |

## ⚠️ Disclaimer

This application is provided for **educational and testing purposes only**. The authors are not responsible for any misuse or damage caused by this software. Always obtain proper authorization before testing security tools against any system.

## 📜 License

MIT License - Use freely for learning and testing purposes.

---

**Happy Hacking! 🎯**

*Remember: With great power comes great responsibility. Use this knowledge ethically!*
