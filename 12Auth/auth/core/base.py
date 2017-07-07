#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: XuMing <shibing624@126.com>
@description:
"""

import abc
from .normal import normal_attr
from .utils import INT_ID_KEY
from ..exception import DataErrorException, JSONDecodeError

__all__ = ['Base']


class Base:
    def __init__(self, obj_id, cache, session):
        self._id = obj_id
        self._cache = cache
        self._session = session
        self._data = None
        self._refresh_times = 0

    @property
    @normal_attr()
    def id(self):
        return getattr(self, '_id', None)

    def _get_data(self):
        if self._data is None:
            url = self._build_url()
            res = self._session.request(
                self._method(),
                url=url,
                params=self._build_params(),
                data=self._build_data(),
            )
            e = DataErrorException(url,
                                   res,
                                   'There is a valid {0} JSON data'.format(self.__class__.__name__),
                                   )
            try:
                json_dict = res.json()
                if 'error' in json_dict:
                    raise e
                id_field = getattr(self, 'ID_FIELD_NAME', 'id')
                if hasattr(self, INT_ID_KEY) and id_field in json_dict:
                    json_dict.update({id_field: int(json_dict[id_field])})
                self._data = json_dict
            except JSONDecodeError:
                raise e

    @abc.abstractmethod
    def _build_url(self):
        return ''

    def _build_params(self):
        return None

    def _build_data(self):
        return None

    def _method(self):
        return "GET"

    def refresh(self):
        self._data = self._cache = None
        self._refresh_times += 1

    @property
    def pure_data(self):
        if not self._cache:
            self._get_data()
        return {
            'cache': self._cache,
            'data': self._data,
        }
