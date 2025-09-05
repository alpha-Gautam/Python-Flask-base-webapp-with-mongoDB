from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import pymongo
from datetime import datetime
import json
import os
import requests
from dotenv import load_dotenv
from firebase_config import verify_firebase_token, get_user_info
from functools import wraps
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()


def myfunc():
    # res=requests.get("http://127.0.0.1:5000/hello")
    requests.get("https://flask-web-xlni.onrender.com/hello")
    print("scheduler is running....")
    # print(res.json())
    return "ok"
job = scheduler.add_job(myfunc, 'interval', minutes=2)
scheduler.start()

# Load environment variables from .env file
load_dotenv()

with open("confi.json", "r") as c:
    data=json.load(c)
params=data["parameter"]

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key')

myclient = pymongo.MongoClient(os.getenv('MONGODB_URI'))
db = myclient["mydatabase"]

contact_db = db.contacts
post_db = db.posts
users_db = db.users

def login_required(f):
    """
    Decorator to require authentication for certain routes
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def save_user_to_db(user_info):
    """
    Save or update user information in the database
    """
    user_data = {
        "uid": user_info['uid'],
        "email": user_info['email'],
        "display_name": user_info.get('display_name'),
        "email_verified": user_info.get('email_verified', False),
        "last_login": datetime.now()
    }
    
    # Update if user exists, otherwise insert
    users_db.update_one(
        {"uid": user_info['uid']},
        {
            "$set": user_data, 
            "$setOnInsert": {"created_at": datetime.now()}
        },
        upsert=True
    )
    return user_data


@app.route("/hello")
def hello():
    # print("hello")
    
    return f"Hi, I am doing good, now the time is:- {datetime.now()}"
@app.route("/")
@app.route("/home")
def home_html():
    start=datetime.now()
    posts=post_db.find()[:params["no_of_post"]]
    print("time different:-",datetime.now()-start)
    print("time start:-",start)
    print("time later:-",datetime.now())
    print("server url:-", request.url)
    
    return render_template("home.html", params=params,posts=posts)


@app.route("/post/<string:post_slug>", methods=["GET"])
def post_detail(post_slug):
    # slug=post_slug
    post=post_db.find_one({"slug":post_slug})
    return render_template("postdetail.html",params=params,post=post)




@app.route("/login", methods=["GET","POST"])
def login():
    if("user" in session):
        posts=post_db.find()
        return render_template("dasboard.html",params=params,posts=posts)
        
    elif request.method == "POST":
        # Handle Firebase token verification
        if request.is_json:
            data = request.get_json()
            id_token = data.get('idToken')
            
            if id_token:
                # Verify Firebase token
                decoded_token = verify_firebase_token(id_token)
                if decoded_token:
                    uid = decoded_token['uid']
                    user_info = get_user_info(uid)
                    
                    if user_info:
                        # Save user to database
                        saved_user = save_user_to_db(user_info)
                        
                        # Set session
                        session["user"] = user_info['email']
                        session["uid"] = uid
                        session["display_name"] = user_info.get('display_name', user_info['email'])
                        params["session_user"] = True
                        
                        return jsonify({"success": True, "redirect": "/dasboard"})
                    else:
                        return jsonify({"success": False, "error": "Failed to get user info"})
                else:
                    return jsonify({"success": False, "error": "Invalid token"})
            else:
                return jsonify({"success": False, "error": "No token provided"})
        
        # If not JSON request, redirect to login page
        return redirect(url_for('login'))

    else:
        return render_template("login.html", params=params)


@app.route("/about")
def about():
    return render_template("about.html",params=params)



@app.route("/post")
def post_route():
    posts=post_db.find()[:params["no_of_post"]]
    return render_template("post.html", params=params,posts=posts)
    


@app.route("/contact", methods=['GET', 'POST'])
def contact():

    if request.method == "POST":
        #  entry message to database
        '''first (name) is to store data ,second ("name") is comes from web page'''
        clint_data={
            "name": request.form.get("name"),
            "phone" : request.form.get("phone"),
            "email" : request.form.get("email"),
            "message" : request.form.get("message"),
            "time" : datetime.now()
            }
        contact_db.insert_one(clint_data)

    return render_template("contact.html", params=params)






@app.route("/dasboard")
@login_required
def dasboard():
    posts=post_db.find()
    return render_template("dasboard.html",params=params,posts=posts)




@app.route("/logout")
def logout():
    # Remove all user-related keys from the session
    session.pop("user", None)
    session.pop("uid", None)
    session.pop("display_name", None)
    params["session_user"]=False
    
    # Redirect to home page
    return redirect(url_for('home_html'))


@app.route("/api", methods=["GET"])
def api():
    filter={"_id":0, "s_no":1,"title":1,"name":1,"slug":1,"content":1,"date":1, "tagline":1}
    posts = post_db.find({},filter)
    
    post_data = [post for post in posts]
    print("post data...", len(post_data))
    print("post data...", type(post_data))
    return jsonify(post_data)


@app.route("/api/auth-status", methods=["GET"])
def auth_status():
    """
    API endpoint to check authentication status
    """
    if 'user' in session:
        return jsonify({
            "authenticated": True,
            "user": session.get('user'),
            "display_name": session.get('display_name'),
            "uid": session.get('uid')
        })
    else:
        return jsonify({"authenticated": False})


@app.route("/api/firebase-config", methods=["GET"])
def firebase_config():
    """
    API endpoint to provide Firebase configuration
    """
    return jsonify({
        "apiKey": os.getenv('FIREBASE_API_KEY'),
        "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
        "databaseURL": os.getenv('FIREBASE_DATABASE_URL'),
        "projectId": os.getenv('FIREBASE_PROJECT_ID'),
        "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
        "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
        "appId": os.getenv('FIREBASE_APP_ID')
    })


@app.route("/api/users", methods=["GET"])
@login_required
def get_users():
    """
    API endpoint to get all registered users (admin only)
    """
    try:
        users = list(users_db.find({}, {"_id": 0}))
        return jsonify({"success": True, "users": users})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})



@app.route("/add_post", methods=["POST"])
def add_post():
    if request.method == "POST":
        #  entry message to database
        '''first (name) is to store data ,second ("name") is comes from web page'''
        post_data={
            "name": request.form.get("name"),
            "phone" : request.form.get("phone"),
            "email" : request.form.get("email"),
            "message" : request.form.get("message"),
            "time" : datetime.now()
            }
        response = post_db.insert_one(post_data)
        return jsonify({"success": True, "id": str(response.inserted_id)})
    
    return jsonify({"success": False, "error": "Invalid request method"})
       
    
    
    
    


if __name__ == "__main__":
    app.run(debug=True)
    