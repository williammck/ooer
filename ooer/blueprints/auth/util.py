from urlparse import urlparse, urljoin

from flask import redirect, request

from ooer.models.user import User


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(next_url=None):
    if not next_url:
        next_url = request.args.get('next', '/')

    if is_safe_url(next_url):
        return redirect(next_url)
    else:
        return redirect('/')


def authenticate_user(redditor):
    user = User.objects(username__iexact=redditor.name).first()

    if user is None:
        user = User(username=redditor.name)
        user.save()

    return user
