# -*- coding: utf-8 -*-

import datetime
import pkg_resources
import shelve


class _Borg(object):
    _shared_state = {}

    def __init__(self):
        self.__dict__ = _Borg._shared_state.setdefault(type(self), {"score": 0})


class Scorekeeper(_Borg):
    def __init__(self):
        _Borg.__init__(self)

    def __call__(self, score, threshold=100, decay=None, callback=None):
        self.score = self._get_score()[1]
        if decay:
            self._decay(decay)
        self.score += score
        if self.score > threshold:
            self.reset_score()
            self.default_callback() if not callback else callback()
        self._set_score()

    def default_callback(self):
        raise ScorekeeperError("Score has been exceeded!")

    def reset_score(self):
        self.score = 0

    def seconds_since_last_score(self):
        return 10

    def _get_score(self):
        with shelve.open(self._shelve_path()) as db:
            key = type(self).__name__
            result = db.get(key) or {}
        return result.get("datetime"), result.get("score", 0)

    def _set_score(self):
        with shelve.open(self._shelve_path()) as db:
            key = type(self).__name__
            db[key] = {"datetime": datetime.datetime.now(), "score": self.score}

    def _shelve_path(self):
        return pkg_resources.resource_filename('scorekeeper', 'data/scores')


    def _decay(self, rate):
        time = self._seconds_since_last_score()
        decay = int(time / rate)
        self.score =  max(0, self.score - decay)

    def _seconds_since_last_score(self):
        return (datetime.datetime.now() - self._get_score()[0]).seconds

class ScorekeeperError(Exception):
    pass
