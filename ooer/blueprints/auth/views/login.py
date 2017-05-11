import praw
from flask import current_app, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_user
from flask_wtf.csrf import generate_csrf, validate_csrf
from itsdangerous import BadData, URLSafeTimedSerializer

from .. import blueprint
from ..util import is_safe_url, redirect_back, authenticate_user

reddit = praw.Reddit(client_id=current_app.config.get('REDDIT_CLIENT_ID'),
                     client_secret=current_app.config.get('REDDIT_CLIENT_SECRET'),
                     user_agent='web:ooer.lol:v1 by /u/williammck',
                     redirect_uri=current_app.config.get('REDDIT_REDIRECT_URI'))

s = URLSafeTimedSerializer(current_app.secret_key, salt='ohmaniamnotgoodwithcomputerplstohelp')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect_back()

    state_data = {'csrf': generate_csrf()}

    next_url = request.args.get('next')
    if is_safe_url(next_url):
        state_data['next'] = next_url

    state = s.dumps(state_data)

    url = reddit.auth.url(['identity'], state, 'permanent')

    return render_template('auth/login.html', url=url, title='Log in')


@blueprint.route('/login/callback')
def login_callback():
    if current_user.is_authenticated:
        return redirect_back()

    try:
        state_data = s.loads(request.args.get('state'), max_age=300)
        validate_csrf(state_data.get('csrf'))
    except BadData:
        flash("Couldn't log you in due to an invalid state.", category='danger')
        return redirect(url_for('.login'))

    next_url = state_data.get('next')

    if 'error' in request.args:
        reasons = {
            'access_denied': 'you not granting us permission to access your account'
        }

        flash(
            "Couldn't log you in due to %s." % reasons.get(request.args['error'], 'an unknown error'),
            category='danger'
        )

        if is_safe_url(next_url):
            return redirect(url_for('.login', next=next_url))
        else:
            return redirect(url_for('.login'))

    if 'code' not in request.args:
        flash("Couldn't log you in due to an unknown error.", category='danger')

        if is_safe_url(next_url):
            return redirect(url_for('.login', next=next_url))
        else:
            return redirect(url_for('.login'))

    refresh_token = reddit.auth.authorize(request.args.get('code'))

    user = authenticate_user(reddit.user.me())

    if login_user(user, remember=True):
        flash('Logged in!', category='success')
        return redirect_back(next_url)

    flash("Couldn't log you in due to an unknown error.", category='danger')

    if is_safe_url(next_url):
        return redirect(url_for('.login', next=next_url))
    else:
        return redirect(url_for('.login'))
