from flask import render_template, request, Blueprint
from flask_login import login_required, current_user
from blog.models import Post, User

main = Blueprint('main', __name__)



@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(
            page=page, per_page=10)
        return render_template("newsfeed.html", posts=posts)
    else:
        return render_template('index.html')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query')
    if query is '':
        return render_template('search.html', users=None, posts=None)
    posts = Post.query.msearch(query, fields=['title', 'content'])
    users = User.query.msearch(query, fields=['username'])
    return render_template('search.html', users=users, posts=posts)


