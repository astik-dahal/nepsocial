from flask import render_template, url_for ,flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from blog import db
from blog.models import Post
from blog.posts.forms import AddPostForm, UpdatePostForm
from blog.users.utils import save_post_picture
posts = Blueprint('posts', __name__)


@posts.route('/post/<int:id>')
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)


@posts.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)


@posts.route('/addpost', methods=['GET', 'POST'])
@login_required
def addpost():
    form = AddPostForm()
    if form.validate_on_submit():
        form_picture = form.image_file.data
        if form_picture :
            picture_file = save_post_picture(form_picture)
            if picture_file:
                post = Post(title=form.title.data,
                            content=form.content.data,
                            image_file=picture_file,
                            category=form.category.data,
                            user_id=current_user.id)
                db.session.add(post)
                db.session.commit()
                return redirect(url_for('main.index'))
            else:
                flash("Unsupported file type. Please upload .JPG or .PNG")
                return redirect(url_for('posts.addpost'))
        post = Post(title=form.title.data,
                    content=form.content.data,
                    category=form.category.data,
                    user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('addpost.html', form=form)


@posts.route('/update/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def updatepost(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id == post.author.id:
        form = UpdatePostForm()
        if form.validate_on_submit():
            form_picture = form.image_file.data
            if form_picture:
                picture_file = save_post_picture(form_picture)
                if picture_file:
                    post.title = form.title.data
                    post.content = form.content.data
                    post.image_file = picture_file
                    post.category = form.category.data
                    db.session.commit()
                    flash("Post updated successfully", "success")
                    return redirect(url_for('posts.post', id=post_id))
                else:
                    flash("Unsupported file type. Please upload .JPG or .PNG")
                    return redirect(url_for('posts.updatepost'))
            post.title = form.title.data
            post.content = form.content.data
            post.category = form.category.data
            db.session.commit()
            flash("Post updated successfully", "success")
            return redirect(url_for('posts.post', id=post_id))
        if request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
            form.image_file.data = post.image_file
            return render_template('updatepost.html', form=form)
        else:
            return render_template('updatepost.html', form=form)
    else:
        return render_template('403.html'), 403


@posts.route('/delete/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def deletepost(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id == post.author.id:
        try:
            db.session.delete(post)
            db.session.commit()
            flash("Post deleted successfully", "success")
            return redirect(url_for('main.index'))
        except:
            flash("Error while deleting the post, try again in a moment.",
                  "error")
            return redirect(url_for('main.index'))
    else:
        return render_template('403.html'), 403
