# -*- coding: utf-8 -*-

import datetime
import pkg_resources
import shelve

__all__ = ["Scorekeeper", "score"]


class _ScorekeeperSharedState(object):
    _shared_state = {}

    def __init__(self):
        self.__dict__ = _ScorekeeperSharedState._shared_state.setdefault(type(self), {})


class Scorekeeper(_ScorekeeperSharedState):
    def __init__(self):
        _ScorekeeperSharedState.__init__(self)
        self.score = self._get_score()[1]

    def __call__(self, score, threshold=100, decay=None, callback=None):
        return_value = None
        self.score = self._get_score()[1]
        if decay:
            self._decay(decay)
        self.score += score
        if self.score > threshold:
            self.reset_score()
            return_value = self.default_callback() if not callback else callback()
        self._set_score()
        return return_value

    def default_callback(self):
        raise ScoreExceededError("Score has been exceeded!")

    def reset_score(self):
        self.score = 0
        self._set_score()

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
        last_time = self._get_score()[0]
        if not last_time:
            return 0
        else:
            return (datetime.datetime.now() - last_time).seconds


class ScoreExceededError(Exception):
    pass


def score(scorekeeper_obj, points, **kwargs):

    def decorator(func):

        def wrapper(*args):
            if not func():
                obj = scorekeeper_obj()
                obj(points, **kwargs)

        return wrapper

    return decorator
