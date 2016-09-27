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


@pytest.fixture
def scorekeeper_obj(tmpdir):
    class ScorekeeperObj(Scorekeeper):
        def _shelve_path(self):
            global tmp_path
            if not tmp_path:
                tmp_path = str(tmpdir.mkdir("data").join("/scores"))

            return tmp_path

    yield ScorekeeperObj()
    tmp_path = None


@pytest.mark.parametrize("points, expected", [(10, 10), (20, 30), (30, 60)])
def test_scorekeeper_increments(scorekeeper_obj, points, expected):
    scorekeeper_obj(points)
    assert scorekeeper_obj.score == expected
