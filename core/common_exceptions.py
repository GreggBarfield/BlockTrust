class BTNException(Exception):
    """Internal exception root"""
    pass


class FriendlyException(BTNException):
    """Safe-to-export exception, intended for use even in production"""
    pass


class DebugException(BTNException):
    """Potentially hazardous exception, intended for use only in development
    (suppress in production)
    """
    pass


class ExportException(BTNException):
    """Safe-to-export exception"""
    pass
