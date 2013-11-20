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
		                           [-w RANGE] [-c RANGE] [-v]
		
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
		  -w RANGE, --warning RANGE
		                        warning if threshold is outside RANGE
		  -c RANGE, --critical RANGE
		                        critical if threshold is outside RANGE
		  -v, --verbose         increase verbosity (use up to 3 times)

Releases
========
0.2.3 - Nov 20, 2013: Added support for monitoring ratio between two metrics. Thanks s0enke!

Develop
=======
Fork me on `Github <https://github.com/FastSociety/nagios-cloudwatch-plugin>`_.