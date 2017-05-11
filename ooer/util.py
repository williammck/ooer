import arrow
from flask import request, session, url_for


def init_utils(application):
    @application.before_request
    def before_request():
        if request.args.get('css') in ['enable', 'disable']:
            session['css_disabled'] = request.args.get('css') == 'disable'

    @application.context_processor
    def utility_processor():
        def url_for_css(disabled):
            args = request.view_args.copy()
            args['css'] = 'enable' if disabled else 'disable'

            return url_for(request.endpoint, **args)

        return {'url_for_css': url_for_css}

    @application.template_filter('humanize')
    def humanize(timestamp):
        return arrow.get(timestamp).humanize()

    @application.template_filter('unique')
    def unique(a):
        c = []
        for x in a:
            if x not in c:
                c.append(x)

        return c
