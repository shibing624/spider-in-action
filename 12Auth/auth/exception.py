#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: XuMing <shibing624@126.com>
@description:Exception
"""


class AppException(Exception):
    pass


class UnexpectedResponseException(AppException):
    def __init__(self, url, res, expect):
        self.url = url
        self.res = res
        self.expect = expect

    def __repr__(self):
        return "Unexpected response when visit url [{self.url}]," \
               " we expect [{self.expect}], but the response body " \
               "is [{self.res.text}]".format(self=self)

    __str__ = __repr__


class UnimplementedException(AppException):
    def __init__(self, condition):
        self.condition = condition

    def __repr__(self):
        return "There is an unimplemented condition:{self.condition}. Please send it to developer to get help.".format(
            self=self)

    __str__ = __repr__


class DataErrorException(UnexpectedResponseException):
    def __init__(self, url, res, expect):
        super(DataErrorException, self).__init__(url, res, expect)
        self.reason = res.json()['error']['message']

    def __repr__(self):
        return "There is an error happend when get data: {0}".format(self.reason)

    __str__ = __repr__


class TokenError(AppException):
    def __init__(self, msg):
        self._msg = msg

    def __repr__(self):
        return self._msg


class NeedCaptchaException(AppException):
    def __init__(self):
        pass

    def __repr__(self):
        return "Need a captcha to login, please catch this exception " \
               "and use client.get_captcha() to get it."

    __str__ = __repr__


class NeedLoginException(AppException):
    def __init__(self, condition):
        self.condition = condition

    def __repr__(self):
        return "Need login to use the [{self.condition}] method.".format(self=self)

    __str__ = __repr__


class IdTypeErrorException(AppException):
    def __init__(self, func):
        self.func = func.__name__

    def __repr__(self):
        return "Must provide an integer id to use function: {self.func}".format(self=self)

    __str__ = __repr__


class AppWarning(UserWarning):
    def __init__(self, msg, *args, **kwargs):
        super(AppWarning, self).__init__(*args)
        self._msg = msg

    def __str__(self):
        return str(self._msg)

    __repr__ = __str__


class IgnoreErrorDataWarning(AppWarning):
    def __init__(self, msg, *args, **kwargs):
        super(IgnoreErrorDataWarning, self).__init__(msg, *args, **kwargs)


class CantGetTicketsWarning(AppWarning):
    def __init__(self, msg, *args, **kwargs):
        super(CantGetTicketsWarning, self).__init__(msg, *args, **kwargs)
