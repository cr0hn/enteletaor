# -*- coding: utf-8 -*-


class Singleton(object):
    def __new__(cls,*args,**kwargs):
        if '_inst' not in vars(cls):
            cls._inst = super(Singleton,cls).__new__(cls)
        return cls._inst