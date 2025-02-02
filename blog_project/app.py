# from flask import Flask, request, jsonify
# from werkzeug.utils import secure_filename
# import os
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# # Setup the database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' 
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # Setup the upload folder and allowed extensions
# UPLOAD_FOLDER = 'static/uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# # Blog Post model
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     image = db.Column(db.String(200), nullable=True)  # Optional image field

# # Helper function to check if the file is an allowed type
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# # Route to handle post submission
# @app.route('/posts', methods=['POST'])
# def create_post():
#     title = request.form.get('title')
#     content = request.form.get('content')

#     # Handle the image upload (if any)
#     image_filename = None
#     if 'image' in request.files:
#         image = request.files['image']
#         if image and allowed_file(image.filename):
#             image_filename = secure_filename(image.filename)
#             image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
#             image.save(image_path)

#     # Create the new post
#     new_post = Post(title=title, content=content, image=image_filename)
#     db.session.add(new_post)
#     db.session.commit()

#     return jsonify({"message": "Post created successfully!"}), 201

# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Setup the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Setup the upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Blog Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=True)  # Optional image field

# Helper function to check if the file is an allowed type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route to handle post submission (POST request)
@app.route('/posts', methods=['POST'])
def create_post():
    title = request.form.get('title')
    content = request.form.get('content')

    # Handle the image upload (if any)
    image_filename = None
    if 'image' in request.files:
        image = request.files['image']
        if image and allowed_file(image.filename):
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)

    # Create the new post
    new_post = Post(title=title, content=content, image=image_filename)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "Post created successfully!"}), 201

# Route to get all posts (GET request)
@app.route('/posts', methods=['GET'])  # Corrected to use GET for fetching posts
def get_posts():
    try:
        posts = Post.query.all()  # Fetch all posts from the database
        posts_data = [{"title": post.title, "content": post.content, "image": post.image} for post in posts]
        return jsonify(posts_data)  # Returning the list of posts as JSON
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return jsonify({"message": "Error fetching posts"}), 500

# Route to check if the app is working
@app.route('/')
def home():
    return "Blog App is running!"

if __name__ == '__main__':
    # Create the database tables if they don't exist yet
    with app.app_context():
        db.create_all()  # This ensures the database schema is created
    app.run(debug=True)
