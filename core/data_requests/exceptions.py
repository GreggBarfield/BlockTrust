from ..common_exceptions import ExportException


class DataRequestException(ExportException):
    """Generic data request exception."""
    pass


class DataRequestMalformedException(DataRequestException):
    pass


class DataRequestTypeUnknownException(DataRequestException):
    pass
