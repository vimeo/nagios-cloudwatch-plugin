#!/usr/bin/env python

from distutils.core import setup

setup(name='nagios-cloudwatch-plugin',
        version='0.2',
        description='Nagios Plugin for AWS Cloudwatch Metrics',
        author='William Hutson',
        author_email='wilrnh@gmail.com',
        license="MIT",
        keywords="nagios cloudwatch plugin",
        url='https://github.com/FastSociety/nagios-cloudwatch-plugin',
        install_requires=["argparse","nagiosplugin","boto"],
        
        scripts=["check_cloudwatch.py"]
)