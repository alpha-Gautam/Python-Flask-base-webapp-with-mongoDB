#!/usr/bin/env python3
"""
Firebase Authentication Test Script

This script tests the Firebase authentication integration.
Run this after setting up your Firebase configuration.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_firebase_import():
    """Test if Firebase modules can be imported"""
    try:
        import firebase_admin
        import pyrebase
        print("✅ Firebase modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import Firebase modules: {e}")
        return False

def test_firebase_config():
    """Test Firebase configuration"""
    try:
        from firebase_config import firebase_config, firebase_auth
        print("✅ Firebase configuration loaded successfully")
        
        # Check if config has required fields
        required_fields = ['apiKey', 'authDomain', 'projectId']
        missing_fields = [field for field in required_fields if not firebase_config.get(field) or firebase_config[field] == f"your-{field.lower().replace('key', '-key')}"]
        
        if missing_fields:
            print(f"⚠️  Warning: The following Firebase config fields need to be updated: {missing_fields}")
            print("   Please update firebase_config.py with your actual Firebase project details")
        else:
            print("✅ Firebase configuration appears to be properly configured")
        
        return True
    except Exception as e:
        print(f"❌ Failed to load Firebase configuration: {e}")
        return False

def test_service_account():
    """Test if service account key is available"""
    service_key_path = 'serviceAccountKey.json'
    if os.path.exists(service_key_path):
        print("✅ Service account key file found")
        return True
    else:
        print("⚠️  Service account key file (serviceAccountKey.json) not found")
        print("   Please download it from Firebase Console and place it in the project root")
        return False

def test_flask_app():
    """Test if Flask app can be imported"""
    try:
        from app import app
        print("✅ Flask app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import Flask app: {e}")
        return False

def main():
    """Run all tests"""
    print("🔥 Firebase Authentication Test Suite")
    print("=" * 50)
    
    tests = [
        ("Firebase Module Import", test_firebase_import),
        ("Firebase Configuration", test_firebase_config),
        ("Service Account Key", test_service_account),
        ("Flask App Import", test_flask_app)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Testing: {test_name}")
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    passed = sum(results)
    total = len(results)
    print(f"   ✅ Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Your Firebase setup looks good.")
        print("\nNext steps:")
        print("1. Update Firebase config with your actual project details")
        print("2. Download and place your service account key")
        print("3. Start your Flask app and test authentication")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    print("\n📖 For detailed setup instructions, see FIREBASE_SETUP.md")

if __name__ == "__main__":
    main()
