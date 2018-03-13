#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

from control.sphinx_search import SearchCtrl

class Ctrl(object):

    def __init__(self):
        self.search = SearchCtrl()

    def __del__(self):
        self.close()

    def close(self):
        pass

    @staticmethod
    def instance():
        name = 'singleton'
        if not hasattr(Ctrl, name):
            setattr(Ctrl, name, Ctrl())
        return getattr(Ctrl, name)

# global, called by handler
ctrl = Ctrl.instance()
