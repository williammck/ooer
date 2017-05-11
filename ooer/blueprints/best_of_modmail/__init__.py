import itertools

import praw
from flask import Blueprint, current_app, render_template

blueprint = Blueprint('best_of_modmail', __name__, url_prefix='/modmail')

reddit = praw.Reddit(client_id=current_app.config.get('REDDIT_BOT_CLIENT_ID'),
                     client_secret=current_app.config.get('REDDIT_BOT_CLIENT_SECRET'),
                     user_agent='script:ooer.lol:v1 by /u/williammck',
                     username=current_app.config.get('REDDIT_BOT_USERNAME'),
                     password=current_app.config.get('REDDIT_BOT_PASSWORD'))


@blueprint.route('/')
def index():
    subreddit = reddit.subreddit('Ooer')

    conversations = itertools.chain(
        subreddit.modmail.conversations(limit=2000),
        subreddit.modmail.conversations(limit=2000, state='mod'),
        subreddit.modmail.conversations(limit=2000, state='archived')
    )

    messages = subreddit.mod.inbox(limit=10)
    moderators = subreddit.moderator()

    return render_template('modmail/index.html', conversations=conversations, messages=messages, moderators=moderators)


@blueprint.route('/old/<string:message_id>')
def view_message(message_id):
    subreddit = reddit.subreddit('Ooer')

    message = reddit.inbox.message(message_id)
    moderators = subreddit.moderator()

    return render_template('modmail/view_message.html', message=message, moderators=moderators)


@blueprint.route('/new/<string:conversation_id>')
def view_conversation(conversation_id):
    subreddit = reddit.subreddit('Ooer')
    conversation = subreddit.modmail(conversation_id)

    return render_template('modmail/view_conversation.html', conversation=conversation)
