from datetime import datetime
from app import db
from app.models import User, Post
from app.main.forms import EditProfileForm, PostForm
from flask_login import current_user, login_required
from flask import request, session, redirect, url_for, abort, \
    render_template, flash, current_app
from guess_language import guess_language
from app.main import bp


@bp.route('/user/<username>')
@login_required
def user(username):
    user_ = User.query.filter_by(username=username).first_or_404()
    page_ = request.args.get('page', 1, type=int)
    posts_ = user_.posts.order_by(Post.timestamp.desc()).paginate(
        page_, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user_.username, page=posts_.next_num) if posts_.has_next else None
    prev_url = url_for('user', username=user_.username, page=posts_.prev_num) if posts_.has_prev else None

    return render_template('user.html', user=user_, posts=posts_.items,
                           next_url=next_url, prev_url=prev_url)


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''

        post_ = Post(body=form.post.data, author=current_user)
        db.session.add(post_)
        db.session.commit()
        flash('Your post is now live!')
        # this is a standard. Respond to a POST request of a web form submission with a redirect
        redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None

    return render_template('index.html', title='Home Page', form=form, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user_ = User.query.filter_by(username=username).first()
    if user_ is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user_ == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user_)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user_ = User.query.filter_by(username=username).first()
    if user_ is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user_ is current_user:
        flash('You cannot unfollow yourself')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user_)
    db.session.commit()
    flash('You are not following {}'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None

    return render_template('index.html', title="Explore", posts=posts.items,
                           prev_url=prev_url, next_url=next_url)

