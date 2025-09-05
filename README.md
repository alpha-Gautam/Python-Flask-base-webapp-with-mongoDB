# Flask Blog Web Application with Firebase Authentication

A modern blog web application built with Flask and MongoDB, featuring Firebase authentication and secure environment variable management.

## 🔐 Security Features

This application implements proper security practices:

- **Environment Variables**: All sensitive data is stored in `.env` file
- **No Hardcoded Credentials**: Database and API keys are loaded from environment variables
- **Git Security**: Sensitive files are properly excluded from version control

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Python-Flask-base-webapp-with-mongoDB
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

**IMPORTANT**: Create your environment files from the examples:

```bash
# Copy environment example
cp .env.example .env

# Copy config example
cp confi.json.example confi.json
```

### 5. Configure Environment Variables

Edit `.env` file with your actual credentials:

```env
# Flask Secret Key (generate a secure random key)
SECRET_KEY=your_very_secure_secret_key_here

# MongoDB Connection String
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/

# Admin Credentials
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_secure_admin_password

# Firebase Configuration
FIREBASE_API_KEY=your_firebase_api_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_DATABASE_URL=https://your_project-default-rtdb.firebaseio.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_project.firebasestorage.app
FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id
FIREBASE_APP_ID=your_firebase_app_id
FIREBASE_MEASUREMENT_ID=your_measurement_id
```

### 6. Configure Personal Settings

Edit `confi.json` with your personal links:

```json
{
  "parameter": {
    "linked_url": "https://linkedin.com/in/your-profile",
    "git_url": "https://github.com/your-username?tab=repositories",
    "tw_url": "https://twitter.com/your-username",
    "no_of_post": 4,
    "session_user": false
  }
}
```

### 7. Firebase Setup

1. Create a Firebase project at https://console.firebase.google.com/
2. Enable Authentication and choose your sign-in methods
3. Enable Firestore Database
4. Get your configuration from Project Settings
5. Update the `.env` file with your Firebase credentials

### 8. MongoDB Setup

1. Create a MongoDB Atlas cluster at https://cloud.mongodb.com/
2. Create a database user
3. Get your connection string
4. Update `MONGODB_URI` in `.env` file

### 9. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 🛡️ Security Checklist

Before deploying or sharing your code, ensure:

- [ ] `.env` file is created and contains all required variables
- [ ] `.env` file is listed in `.gitignore`
- [ ] No sensitive data is hardcoded in source files
- [ ] `serviceAccountKey.json` is in `.gitignore`
- [ ] All example files (`.env.example`, `confi.json.example`) are included
- [ ] MongoDB connection string uses environment variables
- [ ] Flask secret key uses environment variables
- [ ] Firebase configuration is served from backend API

## 📁 Project Structure

```
├── app.py                  # Main Flask application
├── firebase_config.py      # Firebase authentication helper
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── confi.json.example     # Configuration template
├── .gitignore            # Git ignore rules
├── static/               # Static assets (CSS, JS, images)
├── templates/            # HTML templates
└── README.md             # This file
```

## 🔧 Environment Variables Reference

| Variable                       | Description                   | Required |
| ------------------------------ | ----------------------------- | -------- |
| `SECRET_KEY`                   | Flask secret key for sessions | Yes      |
| `MONGODB_URI`                  | MongoDB connection string     | Yes      |
| `ADMIN_USERNAME`               | Admin panel username          | Optional |
| `ADMIN_PASSWORD`               | Admin panel password          | Optional |
| `FIREBASE_API_KEY`             | Firebase API key              | Yes      |
| `FIREBASE_AUTH_DOMAIN`         | Firebase auth domain          | Yes      |
| `FIREBASE_DATABASE_URL`        | Firebase database URL         | Yes      |
| `FIREBASE_PROJECT_ID`          | Firebase project ID           | Yes      |
| `FIREBASE_STORAGE_BUCKET`      | Firebase storage bucket       | Yes      |
| `FIREBASE_MESSAGING_SENDER_ID` | Firebase messaging sender ID  | Yes      |
| `FIREBASE_APP_ID`              | Firebase app ID               | Yes      |
| `FIREBASE_MEASUREMENT_ID`      | Firebase measurement ID       | Optional |

## ⚠️ Important Notes

1. **Never commit `.env` file** to version control
2. **Always use strong passwords** for database and admin accounts
3. **Regularly rotate your secret keys** and API keys
4. **Use HTTPS in production** environments
5. **Keep Firebase rules secure** and properly configured

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
