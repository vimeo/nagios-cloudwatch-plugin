#!/usr/bin/env python

import argparse, logging, nagiosplugin, boto
from datetime import datetime, timedelta

class CloudWatchMetric(nagiosplugin.Resource):
    
    def __init__(self, namespace, metric, dimensions, statistic):
        self.namespace = namespace
        self.metric=metric
        self.dimensions = dimensions
        self.statistic = statistic
        
    def probe(self):
        logging.info('getting stats from cloudwatch')
        cw = boto.connect_cloudwatch()
        start_time = datetime.utcnow() - timedelta(minutes=1)
        end_time = datetime.utcnow()
        stats = []
        stats = cw.get_metric_statistics(60, start_time, end_time, 
                                         self.metric, self.namespace, self.statistic, self.dimensions)
        if len(stats) == 0:
            return []
        
        stat = stats[0]
        return [nagiosplugin.Metric('cloudwatchmetric', stat[self.statistic], stat['Unit'])]
        
class CloudWatchMetricSummary(nagiosplugin.Summary):
    
    def __init__(self, namespace, metric, dimensions, statistic):
        self.namespace = namespace
        self.metric=metric
        self.dimensions = dimensions
        self.statistic = statistic
        
    def ok(self, results):
        full_metric = '%s:%s' % (self.namespace, self.metric)
        return 'CloudWatch Metric %s with dimenstions %s' % (full_metric, self.dimensions)
        
    def problem(self, results):
        full_metric = '%s:%s' % (self.namespace, self.metric)
        return 'CloudWatch Metric %s with dimenstions %s' % (full_metric, self.dimensions)
    
class KeyValArgs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        kvs = {}
        for pair in values.split(','):
            kv = pair.split('=')
            kvs[kv[0]] = kv[1]
        setattr(namespace, self.dest, kvs)      

@nagiosplugin.guarded
def main():
    
    argp = argparse.ArgumentParser(description='Nagios plugin to check cloudwatch metrics')
    
    argp.add_argument('-n', '--namespace', required=True,
                      help='namespace for cloudwatch metric')
    argp.add_argument('-m', '--metric', required=True,
                      help='metric name')
    argp.add_argument('-d', '--dimensions', action=KeyValArgs,
                      help='dimensions of cloudwatch metric')
    argp.add_argument('-s', '--statistic', choices=['Average','Sum','SampleCount','Maximum','Minimum'], required=True,
                      help='statistic used to evaluate metric')
    argp.add_argument('-w', '--warning', metavar='RANGE', default=0,
                      help='warning if workers threshold is outside RANGE')
    argp.add_argument('-c', '--critical', metavar='RANGE', default=0,
                      help='critical if workers threshold is outside RANGE')
    argp.add_argument('-v', '--verbose', action='count', default=0,
                      help='increase verbosity (use up to 3 times)')
    argp.add_argument('-t', '--timeout', default=10,
                      help='abort execution after TIMEOUT seconds')
    
    args=argp.parse_args()
    
    check = nagiosplugin.Check(
            CloudWatchMetric(args.namespace, args.metric, args.dimensions, args.statistic),
            nagiosplugin.ScalarContext('cloudwatchmetric', args.warning, args.critical),
            CloudWatchMetricSummary(args.namespace, args.metric, args.dimensions, args.statistic))
    check.main(verbose=args.verbose)

if __name__ == "__main__":
    main()