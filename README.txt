========================
Nagios CloudWatch Plugin
========================

This plugin for checks AWS CloudWatch metrics. It uses the popular **boto**
library to gather metric values. this plugin does not currently have a means of
directly supplying AWS credentials - for this, consult the boto `docs <https://code.google.com/p/boto/wiki/BotoConfig>`_.

Setup
=====
1. pip install nagios-cloudwatch-plugin
2. /usr/local/bin/check_cloudwatch.py -h::

		usage: check_cloudwatch.py [-h] -n NAMESPACE -m METRIC [-d DIMENSIONS] -s
		                           {Average,Sum,SampleCount,Maximum,Minimum}
		                           [-w RANGE] [-c RANGE] [-v] [-t TIMEOUT]
		
		Nagios plugin to check cloudwatch metrics
		
		optional arguments:
		  -h, --help            show this help message and exit
		  -n NAMESPACE, --namespace NAMESPACE
		                        namespace for cloudwatch metric
		  -m METRIC, --metric METRIC
		                        metric name
		  -d DIMENSIONS, --dimensions DIMENSIONS
		                        dimensions of cloudwatch metric
		  -s {Average,Sum,SampleCount,Maximum,Minimum}, --statistic {Average,Sum,SampleCount,Maximum,Minimum}
		                        statistic used to evaluate metric
		  -w RANGE, --warning RANGE
		                        warning if workers threshold is outside RANGE
		  -c RANGE, --critical RANGE
		                        critical if workers threshold is outside RANGE
		  -v, --verbose         increase verbosity (use up to 3 times)
		  -t TIMEOUT, --timeout TIMEOUT
		                        abort execution after TIMEOUT seconds

Develop
=======
Fork me on `Github <https://github.com/FastSociety/nagios-cloudwatch-plugin>`_.