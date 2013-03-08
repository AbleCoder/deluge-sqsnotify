#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.abspath("/media/psf/Projects/ablecoder/deluge"))

# support setuptools or distutils
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


# import ourselves for version info
import sqsnotify


PATH = os.path.dirname(__file__)

packages = [
    'sqsnotify',
]

requires = [
    "boto==2.8.0",
]


setup(
    name=sqsnotify.__title__,
    version=sqsnotify.__version__,
    author='AbleCoder',
    author_email='coder@able.cd',
    license='MIT',
    description='Deluge notify plugin that sends messages to AWS SQS.',
    long_description=open(os.path.join(PATH, 'README')).read() + '\n\n' +
                     open(os.path.join(PATH, 'HISTORY.rst')).read(),
    url='http://github.com/AbleCoder/deluge-sqsnotify',
    packages=packages,
    package_data={sqsnotify.__title__.lower(): ["data/*"]},
    install_requires=requires,

    entry_points="""
    [deluge.plugin.core]
    %s = %s:CorePlugin
    [deluge.plugin.gtkui]
    %s = %s:GtkUIPlugin
    [deluge.plugin.web]
    %s = %s:WebUIPlugin
    """ % ((sqsnotify.__title__, sqsnotify.__title__.lower())*3)
)
