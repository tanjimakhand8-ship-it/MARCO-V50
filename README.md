# MARCO V50 - Secure AI Assistant

A production-ready Flask application with integrated Google Gemini and OpenAI APIs, featuring advanced security, rate limiting, and comprehensive error handling.

## ✨ Features

- 🔐 **Secure**: Environment-based configuration, no hardcoded secrets
- ⚡ **Rate Limited**: 5 requests per minute to prevent abuse
- 🛡️ **Protected**: Input validation, XSS protection, security headers
- 🎤 **Voice Control**: Speech recognition with voice commands
- 🤖 **AI Powered**: Dual AI (OpenAI GPT-4o + Google Gemini 2.0)
- 📊 **Production Ready**: Comprehensive logging and error handling
- 🐳 **Containerized**: Docker and Docker Compose support

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker (optional)
- API keys for Google Gemini and OpenAI

### Local Installation

```bash
# Clone the repository
git clone https://github.com/tanjimakhand8-ship-it/MARCO-V50.git
cd MARCO-V50

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
nano .env  # Edit with your API keys

# Run the application
python app.py
```

Access the application at `http://localhost:5000`

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t marco-v50 .
docker run -p 5000:5000 --env-file .env marco-v50
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# API Keys (obtain from respective platforms)
GEMINI_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key

# System
MASTER_NAME=Your Name
PORT=5000
```

## 📡 API Endpoints

### GET /
Serves the web interface.

**Response**: HTML interface

### POST /ask
Process a user query through AI models.

**Rate Limit**: 5 requests per minute

**Request**:
```json
{
  "prompt": "Your question here"
}
```

**Response**:
```json
{
  "reply": "AI generated response"
}
```

**Error Responses**:
- `400`: Invalid request or input too long (>5000 chars)
- `429`: Rate limit exceeded
- `500`: Internal server error

## 🔐 Security Features

### Input Validation
- Maximum input length: 5000 characters
- XSS protection with HTML escaping
- Rate limiting: 5 requests/minute per IP

### Security Headers
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Strict-Transport-Security: max-age=31536000

### Secure Configuration
- All secrets via environment variables
- No sensitive data in logs
- Secure session cookies (HttpOnly, SameSite)
- HTTPS-ready configuration

## 📊 Production Deployment

### Checklist

- [ ] All API keys rotated and added to `.env`
- [ ] `.env` added to `.gitignore`
- [ ] `FLASK_ENV=production` set
- [ ] `SECRET_KEY` changed from default
- [ ] HTTPS/TLS enabled (use reverse proxy)
- [ ] Rate limiting tuned for your use case
- [ ] Monitoring and logging configured
- [ ] Database backups scheduled
- [ ] Security headers verified
- [ ] CORS policies configured

### Deployment Options

#### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Using Docker
```bash
docker-compose -f docker-compose.yml up -d
```

#### Using Kubernetes
```bash
kubectl create deployment marco --image=marco-v50:latest
kubectl expose deployment marco --type=LoadBalancer --port=80 --target-port=5000
```

## 🐛 Troubleshooting

### API Keys Not Working
1. Verify keys are set in `.env` file
2. Check API key validity on respective platforms
3. Ensure keys have proper permissions
4. Review application logs: `tail -f app.log`

### Rate Limit Exceeded
- Application enforces 5 requests per minute
- Wait 60 seconds before making another request
- Adjust limit in `app.py` if needed

### Port Already in Use
```bash
# Change port via environment variable
export PORT=5001
python app.py

# Or in .env
PORT=5001
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## 🔒 Security Best Practices

### For Developers
1. Never commit `.env` files
2. Use `.env.example` as template
3. Rotate API keys quarterly
4. Review logs for suspicious activity
5. Use strong, unique API keys
6. Enable 2FA on all API platforms

### For Deployment
1. Use HTTPS/TLS in production
2. Implement authentication layer
3. Use API key IP whitelisting
4. Set up monitoring and alerts
5. Regular security audits
6. Keep dependencies updated

## 📝 License

This project is provided as-is for educational and professional use.

## 🆘 Support

For issues, security concerns, or questions:
1. Check the troubleshooting section
2. Review GitHub Issues
3. See SECURITY.md for security-related concerns

## 🎯 Roadmap

- [ ] Database integration
- [ ] User authentication system
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] API key rotation automation
- [ ] Advanced rate limiting strategies
- [ ] WebSocket support for real-time updates

---

**Last Updated**: May 8, 2026  
**Version**: 1.0.0 - Production Ready
