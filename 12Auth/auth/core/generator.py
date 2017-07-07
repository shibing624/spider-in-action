#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: XuMing <shibing624@126.com>
@description:
"""

import functools
import sys
import abc
import warnings

from ..exception import UnexpectedResponseException, JSONDecodeError, TokenError, UnimplementedException
from .utils import build_obj_from_dict


class BaseGenerator:
    def __init__(self, url, session, **default_params):
        self._url = url
        self._session = session
        self._index = 0
        self._data = []
        self._up = 0
        self._next_url = self._url
        self._need_sleep = 0.5
        self._default_params = dict(default_params if default_params else {})
        self._extra_params = {}

    def _fetch_more(self):
        """
        Get next page info
        :return: 
        """
        params = dict(self._default_params)
        params.update(self._extra_params)

        if self._next_url != self._url and 'offset' in params:
            del params['offset']
        res = self._session.get(self._next_url, params=params)
        try:
            json_dict = res.json()
            if not json_dict:
                self._next_url = None
                return
            if 'error' in json_dict:
                error = json_dict['error']
                if 'name' in error:
                    if error['name'] == 'ERR_CONVERSATION_NOT_FOUND':
                        self._next_url = None
                        return
                if 'code' in error:
                    if error['code'] == 100:
                        raise TokenError(error['message'])
                raise UnexpectedResponseException(
                    self._next_url,
                    res,
                    'It is a json string, has data and paging'
                )
            self._up += len(json_dict['data'])
            self._data.extend(json_dict['data'])
            if json_dict['paging']['is_end']:
                self._next_url = None
            else:
                self._next_url = json_dict['paging']['next']
        except (JSONDecodeError, AttributeError):
            raise UnexpectedResponseException(
                self._next_url,
                res,
                'It is a json string, has data and paging'
            )

    @abc.abstractmethod
    def _build_obj(self, data):
        return None

    def __getitem__(self, item):
        """
        Override int
        :param item: 
        :return: 
        """
        if not isinstance(item, int):
            raise TypeError(f'Need an int as index, not {type(item)}')
        if item < 0:
            raise ValueError(f'Index must >=0, {item} provided.')
        while item >= self._up:
            if self._next_url is not None:
                self._fetch_more()
            else:
                raise IndexError('list index out of range')
        return self._build_obj(self._data[item])

    def __iter__(self):
        self._reset()
        return self

    def __next__(self):
        obj = None
        while obj is None:
            try:
                obj = self[self._index]
            except IndexError:
                self._index = 0
                raise StopIteration
            self._index += 1
        return obj

    next = __next__
