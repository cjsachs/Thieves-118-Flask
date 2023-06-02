from flask import request, flash, redirect, url_for, render_template
from flask_login import current_user, login_required
from . import posts
from .forms import PostForm
from app.models import Post, User
from app import db

@posts.route('/create_post', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():

        # This data is coming from the post form
        post_data = {
            'img_url': form.img_url.data,
            'title': form.title.data,
            'caption': form.caption.data,
            'user_id': current_user.id
        }

        # Create Post Instance
        new_post = Post()

        # Set post_data to our Post attributes
        new_post.from_dict(post_data)

        # save to database
        db.session.add(new_post)
        db.session.commit()

        flash('Successfully created post!', 'success')
        return redirect(url_for('main.home'))
    else:
        return render_template('create_post.html', form=form)
    
# Update a post
@posts.route('/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    form = PostForm()
    post = Post.query.get(post_id)
    if request.method == 'POST' and form.validate_on_submit():

        # This data is coming from the post form
        post_data = {
            'img_url': form.img_url.data,
            'title': form.title.data,
            'caption': form.caption.data,
            'user_id': current_user.id
        }

        # Set post_data to our Post attributes
        post.from_dict(post_data)

        # update to database
        db.session.commit()

        flash(f'Successfully updated post {post.title}!', 'success')
        return redirect(url_for('main.home'))
    return render_template('update_post.html', form=form)

# Delete a post
@posts.route('/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user.id == post.user_id:
        db.session.delete(post)
        db.session.commit()
        flash(f'Successfully deleted {post.title}!', 'success')
        return redirect(url_for('main.home'))
    else:
        flash("You cannot delete someone else's post 🐍!", 'danger')
        return redirect(url_for('main.home'))
    

# Follow Route
@posts.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    if user:
        current_user.followed.append(user)
        db.session.commit()
        flash(f'Successfully followed {user.first_name}!', 'success')
        return redirect(url_for('main.contacts'))
    else:
        flash('That user does not exist!', 'warning')
        return redirect(url_for('main.contacts'))

# Unfollow Route
@posts.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
    user = User.query.get(user_id)
    if user:
        current_user.followed.remove(user)
        db.session.commit()
        flash(f'You unfollowed {user.first_name}!', 'warning')
        return redirect(url_for('main.contacts'))
    else:
        flash("You cannot unfollow a user you're not following!", 'danger')
        return redirect(url_for('main.contacts'))