#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_scorekeeper
----------------------------------

Tests for `scorekeeper` module.
"""

import pytest

from scorekeeper.scorekeeper import Scorekeeper

tmp_path = None
current_test = None


@pytest.fixture(autouse=True)
def mock_shelve_path(request, tmpdir, monkeypatch):
    global tmp_path
    global current_test

    if not current_test or current_test != request.function.__name__:
        current_test = request.function.__name__
        tmp_path = str(tmpdir.mkdir("data").join("/{0}".format(request.function.__name__)))


    def mocked_func(*args):
        global tmp_path

        return tmp_path

    monkeypatch.setattr(Scorekeeper, "_shelve_path", mocked_func)


class ScorekeeperObj(Scorekeeper):
    pass


class DifferentScorekeeperObj(Scorekeeper):
    pass


@pytest.mark.parametrize("points, expected", [(10, 10), (20, 30), (30, 60)])
def test_scorekeeper_increments(points, expected):
    scorekeeper_obj = ScorekeeperObj()
    scorekeeper_obj(points)
    assert scorekeeper_obj.score == expected


def test_scorekeeper_objects_of_same_type_share_scores():
    a = ScorekeeperObj()
    b = ScorekeeperObj()
    c = DifferentScorekeeperObj()
    a(10)

    assert a.score == b.score
    assert a is not b
    assert c.score == 0


@pytest.mark.parametrize("points, expected", [(10, None), (20, None), (50, True)])
def test_callback_when_threshold_exceeded(points, expected):
    threshold = 50
    callback = lambda: True

    scorekeeper_obj = ScorekeeperObj()
    assert scorekeeper_obj(points, threshold=threshold, callback=callback) == expected
