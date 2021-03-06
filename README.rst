===============================
Scorekeeper
===============================


.. image:: https://img.shields.io/pypi/v/scorekeeper.svg
        :target: https://pypi.python.org/pypi/scorekeeper

.. image:: https://img.shields.io/travis/dhosterman/scorekeeper.svg
        :target: https://travis-ci.org/dhosterman/scorekeeper

.. image:: https://readthedocs.org/projects/dhostermanscorekeeper/badge/?version=latest
        :target: https://dhostermanscorekeeper.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/dhosterman/scorekeeper/shield.svg
     :target: https://pyup.io/repos/github/dhosterman/scorekeeper/
     :alt: Updates


Keep score of the results of functions over time and take action based on a generated score.

Sometimes, you have a problem that requires you to look at a set of circumstances over time and weigh them
before taking action like intermittent failures in a system or calls to external APIs that may or may not respond.

For example, maybe you have an API endpoint you're monitoring and you want to do some self-healing, but only if
there are at least 5 failures in 5 minutes. You don't want to have a long-running process keeping state over 5 minutes,
so you need something that will maintain state between calls. That might look something like this:

    .. code-block:: python

        @score(ShadyAPIScorekeeper, 20, threshold=100, decay=10, callback=restart_shady_api)
        def check_shady_api():
            if shady_api_test().successful:
                return True
            else:
                return False
            
Every time check_shady_api() is called and returns False, the ShadyAPIScorekeeper will accumulate 20 points. Once the
threshold of 100 points is reached, the callback will be executed. Because you might execute this script from a cron
job or in some other intermittent fashion, the accumulated score for ShadyAPIScorekeeper is persisted on the local file
system. Finally, the (optional) decay parameter lets you set the number of seconds it takes for the accumulated score to
tick down by 1 point.

In this example, ShadyAPIScorekeeper is just a subclass of Scorekeeper and can have its own defaults set for things like
threshold, decay, and callback. This allows the decorator invocation to be much leaner. In addition, all instances of 
a given subclass of Scorekeeper use the same persisted score, so you could decorate multiple functions all with different
points based on their severity in order to generate your final score and decide whether or not to take action.

In addition to using Scorekeeper as a decorator, you can also just directly interface with the objects you've described.
For example:

    .. code-block:: python
    
        >>> score_keeper = ShadyApiScorekeeper()
        >>> score_keeper.score
        0
        >>> score_keeper(10)
        >>> score_keeper.score
        10
        >>> score_keeper(100)
        Shady API restarted!


* Free software: MIT license
* Documentation: https://scorekeeper.readthedocs.io.


Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

