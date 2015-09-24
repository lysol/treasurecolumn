#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import setuptools

setuptools.setup(name='treasurecolumn',
                 version='666.666.666',
                 description=u'𝔗𝔯𝔢𝔞𝔰𝔲𝔯𝔢 ℭ𝔬𝔩𝔲𝔪𝔫',
                 long_description=open('README.md').read().strip(),
                 author='Derek Arnold',
                 author_email='derek@derekarnold.net',
                 url='http://github.com/lysol/treasure-column',
                 packages=setuptools.find_packages(),
                 scripts=[
                    'treasurecolumn/scripts/linize.sh',
                    'treasurecolumn/scripts/linize2.sh',
                    'treasurecolumn/scripts/linize3.sh',
                    'treasurecolumn/scripts/linize4.sh',
                    'treasurecolumn/scripts/mangleaudio.sh',
                 ],
                 install_requires=[
                    'google-api-python-client',
                    'requests',
                    'oauth2client',
                    'wordnik',
                    'requests>=2.7.0'
                 ],
                 include_package_data=True,
                 license='MIT License')
