# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages


setup(
    name='django_model_factory',
    version='0.0.1',
    author=u'Vitaly Babiy',
    author_email='vbabiy86@gmail.com',
    packages=find_packages(),
    url='http://howsthe.com/projects/django_model_factory',
    license='BSD licence, see LICENCE.txt',
    description='A package to replace fixtures in Django, by providing a easy way to build objects using a factory.',
    long_description=open('README.rst').read(),
    zip_safe=True,
)
