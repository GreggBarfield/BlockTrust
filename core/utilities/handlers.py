from flask import g, request, render_template, redirect
from werkzeug.urls import url_encode

from .crut.requirements import RequireAccountFailed, RequireUserFailed, RequireSubscriberFailed
from ..common_exceptions import ExportException, FriendlyException, DebugException

from ..renderers.dashboard import dashboard_render


def respond(code, short, exception=None):
    """Generate a response.

    Params:
        code: the numeric code
        short: the short reason
    """

    if 'api' in g:
        # Return as an api response
        return {
            'short': short,
            'code': code,
            'exception': type(exception).__name__ if exception is not None else None
        }, code

    else:
        return render_template(
            'outside/error.html',
            error_code=code,
            error_reason=short
        ), code


def attach_handlers(app):

    @app.errorhandler(RequireUserFailed)
    def handle_require_user_failed(e):
        # If g.api is not set and the request method is GET, redirect and have them sign in
        if 'api' not in g and request.method == 'GET':
            return redirect(
                "/login?" + url_encode({
                    'redirect': request.url
                })
            )
        else:
            # Else send a 401
            return respond(401, 'Not logged in')

    @app.errorhandler(RequireAccountFailed)
    def handle_require_account_failed(e):
        # If g.api is not set and the request method is GET, send them to account missing page
        if 'api' not in g and request.method == 'GET':
            return dashboard_render("errors/no-account.html")
        else:
            # Else send a 401
            return respond(401, 'No account selected', e)

    @app.errorhandler(RequireSubscriberFailed)
    def handle_require_subscription_failed(e):
        # If stripe_customer_id is not set, send them to the require subscription page
        if g.account.stripe_customer_id() == "" or g.account.stripe_customer_id() is None or g.account.stripe_paid == 0:
            return dashboard_render("errors/not-subscribed.html")

    @app.errorhandler(ExportException)
    def handle_export_exception(e):
        return respond(400, str(e), e)

    @app.errorhandler(FriendlyException)
    def handle_friendly_exception(e):
        return respond(400, str(e), e)

    @app.errorhandler(DebugException)
    def handle_debug_exception(e):
        return respond(400, str(e), e)

    @app.errorhandler(404)
    def handle_error_404(error):
        return respond(404, 'Page not found')
