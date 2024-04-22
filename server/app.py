#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from models import db, Article

# Initialize Flask app
app = Flask(__name__)

# Set secret key for session management
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'

# Configure SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Route to clear session data
@app.route('/clear')
def clear_session():
    # Reset page_views counter to 0
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

# Route to get all articles
@app.route('/articles')
def index_articles():
    # Query all articles from the database and convert them to dictionary format
    articles = [article.to_dict() for article in Article.query.all()]
    # Return JSON response with the list of articles
    return make_response(jsonify(articles), 200)

# Route to show a specific article
@app.route('/articles/<int:id>')
def show_article(id):
    # Set initial value of session['page_views'] to 0 if it's the user's first request
    session['page_views'] = session.get('page_views', 0)
    # Increment the value of session['page_views'] by 1 for each request
    session['page_views'] += 1

    # Check if the user has viewed 3 or fewer pages
    if session['page_views'] <= 3:
        # Query the article with the specified id from the database and convert it to dictionary format
        article = Article.query.filter(Article.id == id).first().to_dict()
        # Return JSON response with the article data
        return article, 200
    else:
        # Return JSON response with error message and status code 401 if maximum pageview limit reached
        return {'message': 'Maximum pageview limit reached'}, 401

if __name__ == '__main__':
    # Run the Flask app
    app.run(port=5555)
