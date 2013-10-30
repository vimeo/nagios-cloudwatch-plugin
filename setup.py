#!/usr/bin/env python

from distutils.core import setup

setup(name='nagios-cloudwatch-plugin',
        version='0.2.1',
        author='William Hutson',
        author_email='wilrnh@gmail.com',
        license="MIT",
        keywords="nagios cloudwatch plugin",
        url='https://github.com/FastSociety/nagios-cloudwatch-plugin',
        description='Nagios plugin to check AWS CloudWatch metrics',
        long_description=open('README.txt').read(),
        install_requires=["argparse","nagiosplugin","boto"],
        
        scripts=["check_cloudwatch.py"]
)