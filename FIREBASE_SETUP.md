# Firebase Authentication Setup Guide

This guide will help you set up Firebase Authentication for your Flask web application.

## Step 1: Create a Firebase Project

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or "Add project"
3. Enter your project name (e.g., "my-blog-app")
4. Follow the setup wizard (you can disable Google Analytics if not needed)

## Step 2: Enable Authentication

1. In your Firebase project console, click on "Authentication" in the left sidebar
2. Click "Get started"
3. Go to the "Sign-in method" tab
4. Enable the following sign-in providers:
   - **Email/Password**: Click and toggle "Enable"
   - **Google**: Click, toggle "Enable", and provide a project support email

## Step 3: Get Firebase Configuration

1. Click on the gear icon (Project settings) in the left sidebar
2. Go to the "General" tab
3. Scroll down to "Your apps" section
4. Click "Add app" and select the web icon (</>)
5. Register your app with a nickname (e.g., "Blog Web App")
6. Copy the Firebase configuration object

Your config will look like this:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  authDomain: "your-project-id.firebaseapp.com",
  databaseURL: "https://your-project-id-default-rtdb.firebaseio.com",
  projectId: "your-project-id",
  storageBucket: "your-project-id.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdefghijklmnop",
};
```

## Step 4: Get Service Account Key (for Backend Verification)

1. In Firebase Console, go to Project Settings > Service accounts
2. Click "Generate new private key"
3. Download the JSON file
4. Rename it to `serviceAccountKey.json`
5. Place it in your project root directory
6. **Important**: Add `serviceAccountKey.json` to your `.gitignore` file to keep it secure

## Step 5: Update Configuration Files

### Update `firebase_config.py`

Replace the placeholder `firebase_config` with your actual Firebase configuration:

```python
firebase_config = {
    "apiKey": "your-actual-api-key",
    "authDomain": "your-project-id.firebaseapp.com",
    "databaseURL": "https://your-project-id-default-rtdb.firebaseio.com",
    "projectId": "your-project-id",
    "storageBucket": "your-project-id.appspot.com",
    "messagingSenderId": "your-sender-id",
    "appId": "your-app-id"
}
```

### Update `login_firebase.html`

Replace the placeholder `firebaseConfig` in the JavaScript section with your actual Firebase configuration.

## Step 6: Set Up Environment Variables (Recommended)

For security, consider using environment variables:

1. Create a `.env` file in your project root:

```
FIREBASE_API_KEY=your-api-key
FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
FIREBASE_DATABASE_URL=https://your-project-id-default-rtdb.firebaseio.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your-sender-id
FIREBASE_APP_ID=your-app-id
```

2. Install python-dotenv:

```bash
pip install python-dotenv
```

3. Update your `firebase_config.py` to use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID")
}
```

## Step 7: Add Security Rules (Optional)

Configure Firebase Security Rules for your database if you plan to use Firestore or Realtime Database.

## Step 8: Test the Implementation

1. Start your Flask application
2. Navigate to `/login`
3. Try both authentication methods:
   - Firebase Google Sign-in
   - Firebase Email/Password
   - Traditional login (fallback)

## Troubleshooting

### Common Issues:

1. **Firebase not initialized**: Make sure you've replaced the placeholder config with your actual Firebase config
2. **Service account key not found**: Ensure `serviceAccountKey.json` is in the project root
3. **CORS errors**: Make sure your domain is added to Firebase's authorized domains in Authentication > Settings
4. **Token verification fails**: Check that your service account key is valid and has the correct permissions

### Firebase Console Authorized Domains:

Add your development and production domains to:
Authentication > Settings > Authorized domains

For local development, `localhost` should already be included.

## Security Notes

1. Never commit your `serviceAccountKey.json` to version control
2. Use environment variables for sensitive configuration
3. Regularly rotate your service account keys
4. Monitor authentication usage in Firebase Console
5. Set up proper Firebase Security Rules if using Firestore/Realtime Database

## Features Implemented

- ✅ Google Sign-in
- ✅ Email/Password authentication
- ✅ User registration
- ✅ Token verification on backend
- ✅ Session management
- ✅ Fallback to traditional login
- ✅ Protected routes with decorator
- ✅ User logout functionality

Your Firebase Authentication is now ready to use!
