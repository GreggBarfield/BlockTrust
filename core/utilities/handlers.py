from flask import g, request, render_template, redirect
from werkzeug.urls import url_encode

from .crut.requirements import (
    RequireNonPartnerAccountFailed,
    RequireUserOrEmployeeFailed,
    RequireUserFailed,
    RequirePaidAccountFailed,
    RequirePartnerFailed
)
from ..common_exceptions import ExportException, FriendlyException, DebugException

from ..renderers.dashboard import dashboard_render
from ..renderers.partner import partner_render
from flask_wtf.csrf import CSRFError


def respond(code, short, exception=None):
    """Generate a response.

    Params:
        code: the numeric code
        short: the short reason
    """

    if 'api' in g:
        # Return as an api response
        return {
            'error': short,
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
        if request.method == 'GET':
            return redirect(
                "/login?" + url_encode({
                    'redirect': request.url
                })
            )
        else:
            # Else send a 401
            return respond(401, 'Not logged in')

    @app.errorhandler(RequireNonPartnerAccountFailed)
    def handle_require_account_failed(e):
        if request.method == 'GET':
            if "account" in g and g.account.is_partner():
                return partner_render("errors/no-access.html")
            else:
                return dashboard_render("errors/no-account.html")
        else:
            # Else send a 401
            return respond(401, 'No account selected', e)

    @app.errorhandler(RequirePaidAccountFailed)
    def handle_require_paid_account_failed(e):
        if request.method == 'GET':
            return dashboard_render("errors/no-paid-account.html")
        else:
            # Else send a 401
            return respond(401, 'No active subscription', e)

    @app.errorhandler(RequireUserOrEmployeeFailed)
    def handle_require_account_or_employee_failed(e):
        return respond(401, "Not authorized", e)

    @app.errorhandler(RequirePartnerFailed)
    def handle_require_partner_failed(e):
        if request.method == 'GET':
            return dashboard_render("errors/no-access.html")
        else:
            return respond(401, 'No access', e)

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

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return respond(400, e.description, e)