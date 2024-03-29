from flask import flash, redirect, url_for
from flask_login import logout_user

from .. import blueprint


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Logged out.', category='success')
    return redirect(url_for('auth.login'))
