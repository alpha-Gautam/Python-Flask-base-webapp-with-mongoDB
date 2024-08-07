from flask import Flask, render_template, request
import pymongo
from datetime import datetime
import json


with open("confi.json", "r") as c:
    data=json.load(c)
params=data["parameter"]

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb+srv://gautammauryamail:R44GrJoMauAjN2yS@cluster0.hk9okct.mongodb.net/")
db = myclient["mydatabase"]

contact_db = db.contacts
post_db = db.posts

# def insert_contacts():
#     contact_db.insert()






@app.route("/")
@app.route("/index")
def index_html():
    posts=post_db.find()[:params["no_of_post"]]
    return render_template("index.html", params=params,posts=posts)


@app.route("/post/<string:post_slug>", methods=["GET"])
def post_route(post_slug):
    # slug=post_slug
    post=post_db.find_one({"slug":post_slug})
    return render_template("post.html",params=params,post=post)











@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        uname= request.form.get("uname")
        password=request.form.get("p_word")
        if uname==params["admin_uname"] and password==params["admin_password"]:
            posts=post_db.find()
            return render_template("dasboard.html",params=params,posts=posts)
        elif uname!=params["admin_uname"] or password!=params["admin_password"]:
            error_mess="username or password is not correct!"
            return render_template("login.html",mess=error_mess, params=params)
        else:
            return render_template("login.html", params=params)
    
        # return render_template("login.html", params=params)

    else:
        return render_template("login.html", params=params)


@app.route("/about")
def about():
    return render_template("about.html",params=params)



# @app.route("/post")
# @app.route("/post/<string:post_slug>",methods=['GET'])
# def post_route(post_slug):
#     post = Posts.query.filter_by(slug=post_slug).first()
#     return render_template("post.html", params=params, post=post )


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
def dasboard():
    posts=post_db.find()
    return render_template("dasboard.html",params=params,posts=posts)


# app.run(debug = True)