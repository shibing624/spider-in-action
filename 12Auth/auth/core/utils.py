#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: XuMing <shibing624@126.com>
@description:
"""
import functools
import importlib
import os

from .urls import RE_TYPE_MAP
from ..exception import (IdTypeErrorException, UnimplementedException)

NOT_INT_ID_CLS_NAME = {'colunm', 'people', 'me'}
INT_ID_KEY = '_id_is_int'


def int_id(func):
    """
    强制类型检查
    :param func: 
    :return: 
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            some_id = args[0]
        except IndexError:
            some_id = None
        if not isinstance(some_id, int):
            raise IdTypeErrorException(self.__class__)
        setattr(self, INT_ID_KEY, True)
        return func(self, *args, **kwargs)

    return wrapper


def get_class_from_name(name, module_file_name=None):
    cls_name = name.capitalize() if name.islower() else name
    file_name = module_file_name or cls_name.lower()
    try:
        imported_module = importlib.import_module('.' + file_name, 'auth.core')
        return getattr(imported_module, cls_name)
    except(ImportError, AttributeError):
        raise UnimplementedException('Unknown obj type [{}]'.format(name))


def build_obj_from_dict(data, session, use_cache=True, type_name=None,
                        file_name=None, cls=None, id_key='id', type_key='type'):
    obj_cls = cls or get_class_from_name(type_name or data[type_key], file_name)
    obj_id = data[id_key]
    if obj_cls.__name__.lower() not in NOT_INT_ID_CLS_NAME:
        obj_cls = int(obj_id)
        data.update({id_key: obj_id})
    return obj_cls(obj_id, data if use_cache else None, session)


def obj_url_parse(url):
    for pattern, obj_type in RE_TYPE_MAP.items():
        match = pattern.match(url)
        if match:
            need_int = obj_type not in NOT_INT_ID_CLS_NAME
            obj_id = match.group(1)
            if need_int:
                obj_id = int(obj_id)
            return obj_id, obj_type
    return None, None


def can_get_from(name, data):
    return name in data and not isinstance(data[name], (dict, list))


DEFAULT_INVALID_CHARS = {':', '*', '?', '"', '<', '>', '|', '\r', '\n'}
EXTRA_CHAR_FOR_FILENAME = {'/', '\\'}


def remove_invalid_char(dirty_data, invalid_chars=None, for_path=False):
    if invalid_chars is None:
        invalid_chars = set(DEFAULT_INVALID_CHARS)
    else:
        invalid_chars = set(invalid_chars)
        invalid_chars.update(DEFAULT_INVALID_CHARS)
    if not for_path:
        invalid_chars.update(EXTRA_CHAR_FOR_FILENAME)

    return ''.join([c for c in dirty_data if c not in invalid_chars]).strip()


def add_serial_number(file_path, suffix):
    full_path = file_path + suffix
    if not os.path.isfile(full_path):
        return full_path
    num = 1
    while os.path.isfile(full_path):
        serial = str(num)
        full_path = file_path + ' - ' + serial.rjust(3, '0') + '.' + suffix
        num += 1
    return full_path
