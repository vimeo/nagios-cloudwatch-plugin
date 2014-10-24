========================
Nagios CloudWatch Plugin
========================

This plugin for checks AWS CloudWatch metrics. It uses the popular **boto**
library to gather metric values. This plugin does not currently have a means of
directly supplying AWS credentials - for this, consult the boto `docs <https://code.google.com/p/boto/wiki/BotoConfig>`_.

Setup
=====
1. pip install nagios-cloudwatch-plugin
2. /usr/local/bin/check_cloudwatch.py -h::

		usage: check_cloudwatch.py [-h] -n NAMESPACE -m METRIC [-d DIMENSIONS]
		                           [-s {Average,Sum,SampleCount,Maximum,Minimum}]
		                           [-p PERIOD] [-l LAG] [-r]
		                           [--divisor-namespace DIVISOR_NAMESPACE]
		                           [--divisor-metric DIVISOR_METRIC]
		                           [--divisor-dimensions DIVISOR_DIMENSIONS]
		                           [--divisor-statistic {Average,Sum,SampleCount,Maximum,Minimum}]
		                           [--delta DELTA] [-w RANGE] [-c RANGE] [-v]
		                           [-R REGION]
		
		Nagios plugin to check cloudwatch metrics
		
		optional arguments:
		  -h, --help            show this help message and exit
		  -n NAMESPACE, --namespace NAMESPACE
		                        namespace for cloudwatch metric
		  -m METRIC, --metric METRIC
		                        metric name
		  -d DIMENSIONS, --dimensions DIMENSIONS
		                        dimensions of cloudwatch metric in the format
		                        dimension=value[,dimension=value...]
		  -s {Average,Sum,SampleCount,Maximum,Minimum}, --statistic {Average,Sum,SampleCount,Maximum,Minimum}
		                        statistic used to evaluate metric
		  -p PERIOD, --period PERIOD
		                        the period in seconds over which the statistic is
		                        applied
		  -l LAG, --lag LAG     delay in seconds to add to starting time for gathering
		                        metric. useful for ec2 basic monitoring which
		                        aggregates over 5min periods
		  -r, --ratio           this activates ratio mode
		  --divisor-namespace DIVISOR_NAMESPACE
		                        ratio mode: namespace for cloudwatch metric of the
		                        divisor
		  --divisor-metric DIVISOR_METRIC
		                        ratio mode: metric name of the divisor
		  --divisor-dimensions DIVISOR_DIMENSIONS
		                        ratio mode: dimensions of cloudwatch metric of the
		                        divisor
		  --divisor-statistic {Average,Sum,SampleCount,Maximum,Minimum}
		                        ratio mode: statistic used to evaluate metric of the
		                        divisor
		  --delta DELTA         time in seconds to build a delta mesurement
		  -w RANGE, --warning RANGE
		                        warning if threshold is outside RANGE
		  -c RANGE, --critical RANGE
		                        critical if threshold is outside RANGE
		  -v, --verbose         increase verbosity (use up to 3 times)
		  -R REGION, --region REGION
		                        The AWS region to read metrics from

Usage
=====
Cloudwatch metrics
------------------
For information on how CloudWatch stores metrics check this `doc <http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/CW_Support_For_AWS.html>`_ out.

- Simple EC2 CPU Utilization check, with warning and critical threshold ranges::

	check_cloudwatch.py -R us-west-2 -n AWS/EC2 -m CPUUtilization -p 600 -d InstanceId=i-abcd1234 -w 0:75 -c 0:90

Releases
========
0.2.5 - Sep 09, 2014: Support passing region as an argument, defaulting to boto default. Thanks grahamlyons!

0.2.4 - Nov 20, 2013: Added support for delta monitoring of a single metric. Thanks nesQuick & s0enke!

0.2.3 - Nov 20, 2013: Added support for monitoring ratio between two metrics. Thanks nesQuick & s0enke!


Develop
=======
Fork me on `Github <https://github.com/FastSociety/nagios-cloudwatch-plugin>`_.