#!/usr/bin/env python

from distutils.core import setup
# http://pypi.python.org/pypi?%3Aaction=list_classifiers
setup(name='bzr-flakes',
      description='pylakes plugin for Bazaar',
      keywords='plugin bzr pyflakes python undefined checker',
      version='0.2b',
      license='BSD',
      #url='', # home page for the package
      #download_url='',
      author='Mateusz `matee` Pawlik',
      author_email='matee@matee.net',
      long_description='''
      Notification before commit about undefined names using pyflakes.
      ''',
      requires=['pyflakes (>=0.1.7)', 'bzr (>=1.3.1)'],
#      install_requires=['pyflakes>=0.1.7', 'bzr>=1.3.1'],
      package_dir={'bzrlib.plugins.flakes':''},
      packages=['bzrlib.plugins.flakes'],
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Quality Assurance',
      ],)
