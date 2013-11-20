#!/usr/bin/env python

import argparse, logging, nagiosplugin, boto
from datetime import datetime, timedelta

class CloudWatchMetric(nagiosplugin.Resource):

    def __init__(self, namespace, metric, dimensions, statistic, period, lag):
        self.namespace = namespace
        self.metric = metric
        self.dimensions = dimensions
        self.statistic = statistic
        self.period = int(period)
        self.lag = int(lag)

    def probe(self):
        logging.info('getting stats from cloudwatch')
        cw = boto.connect_cloudwatch()
        start_time = datetime.utcnow() - timedelta(seconds=self.period) - timedelta(seconds=self.lag)
        logging.info(start_time)
        end_time = datetime.utcnow()
        stats = []
        stats = cw.get_metric_statistics(self.period, start_time, end_time,
                                         self.metric, self.namespace, self.statistic, self.dimensions)
        if len(stats) == 0:
            return []

        stat = stats[0]
        return [nagiosplugin.Metric('cloudwatchmetric', stat[self.statistic], stat['Unit'])]

class CloudWatchRatioMetric(nagiosplugin.Resource):

    def __init__(self, dividend_namespace, dividend_metric, dividend_dimension, dividend_statistic, period, lag, divisor_namespace, divisor_metric, divisor_dimension, divisor_statistic):
        self.dividend_metric = CloudWatchMetric(dividend_namespace, dividend_metric, dividend_dimension, dividend_statistic, int(period), int(lag))
        self.divisor_metric  = CloudWatchMetric(divisor_namespace, divisor_metric, divisor_dimension, divisor_statistic, int(period), int(lag))

    def probe(self):
        dividend = self.dividend_metric.probe()[0]
        divisor = self.divisor_metric.probe()[0]

        ratio_unit = '%s / %s' % ( dividend.uom, divisor.uom)

        return [nagiosplugin.Metric('cloudwatchmetric', dividend.value / divisor.value, ratio_unit)]

class CloudWatchDeltaMetric(nagiosplugin.Resource):

    def __init__(self, namespace, metric, dimensions, statistic, period, lag, delta):
        self.namespace = namespace
        self.metric = metric
        self.dimensions = dimensions
        self.statistic = statistic
        self.period = period
        self.lag = lag
        self.delta = delta

    def probe(self):
        logging.info('getting stats from cloudwatch')
        cw = boto.connect_cloudwatch()

        datapoint1_start_time = (datetime.utcnow() - timedelta(seconds=self.period) - timedelta(seconds=self.lag)) - timedelta(seconds=self.delta)
        datapoint1_end_time = datetime.utcnow() - timedelta(seconds=self.delta)
        datapoint1_stats = cw.get_metric_statistics(self.period, datapoint1_start_time, datapoint1_end_time,
                                         self.metric, self.namespace, self.statistic, self.dimensions)

        datapoint2_start_time = datetime.utcnow() - timedelta(seconds=self.period) - timedelta(seconds=self.lag)
        datapoint2_end_time = datetime.utcnow()
        datapoint2_stats = cw.get_metric_statistics(self.period, datapoint2_start_time, datapoint2_end_time,
                                         self.metric, self.namespace, self.statistic, self.dimensions)

        if len(datapoint1_stats) == 0 or len(datapoint2_stats) == 0:
            return []

        datapoint1_stat = datapoint1_stats[0]
        datapoint2_stat = datapoint2_stats[0]
        num_delta = datapoint2_stat[self.statistic] - datapoint1_stat[self.statistic]
        per_delta = (100 / datapoint2_stat[self.statistic]) * num_delta
        return [nagiosplugin.Metric('cloudwatchmetric', per_delta, '%')]

class CloudWatchMetricSummary(nagiosplugin.Summary):

    def __init__(self, namespace, metric, dimensions, statistic):
        self.namespace = namespace
        self.metric = metric
        self.dimensions = dimensions
        self.statistic = statistic

    def ok(self, results):
        full_metric = '%s:%s' % (self.namespace, self.metric)
        return 'CloudWatch Metric %s with dimenstions %s' % (full_metric, self.dimensions)

    def problem(self, results):
        full_metric = '%s:%s' % (self.namespace, self.metric)
        return 'CloudWatch Metric %s with dimenstions %s' % (full_metric, self.dimensions)

class CloudWatchMetricRatioSummary(nagiosplugin.Summary):

    def __init__(self, dividend_namespace, dividend_metric, dividend_dimensions, dividend_statistic, divisor_namespace, divisor_metric, divisor_dimensions, divisor_statistic):
        self.dividend_namespace = dividend_namespace
        self.dividend_metric = dividend_metric
        self.dividend_dimensions = dividend_dimensions
        self.dividend_statistic = dividend_statistic
        self.divisor_namespace = divisor_namespace
        self.divisor_metric = divisor_metric
        self.divisor_dimensions = divisor_dimensions
        self.divisor_statistic = divisor_statistic

    def ok(self, results):
        dividend_full_metric = '%s:%s' % (self.dividend_namespace, self.dividend_metric)
        divisor_full_metric = '%s:%s' % (self.divisor_namespace, self.divisor_metric)
        return 'Ratio: CloudWatch Metric %s with dimenstions %s / CloudWatch Metric %s with dimenstions %s' % (dividend_full_metric, self.dividend_dimensions, divisor_full_metric, self.divisor_dimensions)

    def problem(self, results):
        dividend_full_metric = '%s:%s' % (self.dividend_namespace, self.dividend_metric)
        divisor_full_metric = '%s:%s' % (self.divisor_namespace, self.divisor_metric)
        return 'Ratio: CloudWatch Metric %s with dimenstions %s / CloudWatch Metric %s with dimenstions %s' % (dividend_full_metric, self.dividend_dimensions, divisor_full_metric, self.divisor_dimensions)

class CloudWatchDeltaMetricSummary(nagiosplugin.Summary):

    def __init__(self, namespace, metric, dimensions, statistic, delta):
        self.namespace = namespace
        self.metric = metric
        self.dimensions = dimensions
        self.statistic = statistic
        self.delta = delta

    def ok(self, results):
        full_metric = '%s:%s' % (self.namespace, self.metric)
        return 'CloudWatch %d seconds Delta %s Metric with dimenstions %s' % (self.delta, full_metric, self.dimensions)

    def problem(self, results):
        full_metric = '%s:%s' % (self.namespace, self.metric)
        return 'CloudWatch %d seconds Delta %s Metric with dimenstions %s' % (self.delta, full_metric, self.dimensions)

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
                      help='dimensions of cloudwatch metric in the format dimension=value[,dimension=value...]')
    argp.add_argument('-s', '--statistic', choices=['Average','Sum','SampleCount','Maximum','Minimum'], default='Average',
                      help='statistic used to evaluate metric')
    argp.add_argument('-p', '--period', default=60, type=int,
                      help='the period in seconds over which the statistic is applied')
    argp.add_argument('-l', '--lag', default=0,
                      help='delay in seconds to add to starting time for gathering metric. useful for ec2 basic monitoring which aggregates over 5min periods')

    argp.add_argument('-r', '--ratio', default=False, action='store_true',
                      help='this activates ratio mode')
    argp.add_argument('--divisor-namespace',
                      help='ratio mode: namespace for cloudwatch metric of the divisor')
    argp.add_argument('--divisor-metric',
                      help='ratio mode: metric name of the divisor')
    argp.add_argument('--divisor-dimensions', action=KeyValArgs,
                      help='ratio mode: dimensions of cloudwatch metric of the divisor')
    argp.add_argument('--divisor-statistic', choices=['Average','Sum','SampleCount','Maximum','Minimum'],
                      help='ratio mode: statistic used to evaluate metric of the divisor')

    argp.add_argument('--delta', type=int,
                      help='time in seconds to build a delta mesurement')

    argp.add_argument('-w', '--warning', metavar='RANGE', default=0,
                      help='warning if threshold is outside RANGE')
    argp.add_argument('-c', '--critical', metavar='RANGE', default=0,
                      help='critical if threshold is outside RANGE')
    argp.add_argument('-v', '--verbose', action='count', default=0,
                      help='increase verbosity (use up to 3 times)')

    args=argp.parse_args()

    if args.ratio:
        metric = CloudWatchRatioMetric(args.namespace, args.metric, args.dimensions, args.statistic, args.period, args.lag, args.divisor_namespace,  args.divisor_metric, args.divisor_dimensions, args.divisor_statistic)
        summary = CloudWatchMetricRatioSummary(args.namespace, args.metric, args.dimensions, args.statistic, args.divisor_namespace,  args.divisor_metric, args.divisor_dimensions, args.divisor_statistic)
    elif args.delta:
        metric = CloudWatchDeltaMetric(args.namespace, args.metric, args.dimensions, args.statistic, args.period, args.lag, args.delta)
        summary = CloudWatchDeltaMetricSummary(args.namespace, args.metric, args.dimensions, args.statistic, args.delta)
    else:
        metric = CloudWatchMetric(args.namespace, args.metric, args.dimensions, args.statistic, args.period, args.lag)
        summary = CloudWatchMetricSummary(args.namespace, args.metric, args.dimensions, args.statistic)

    check = nagiosplugin.Check(
            metric,
            nagiosplugin.ScalarContext('cloudwatchmetric', args.warning, args.critical),
            summary)
    check.main(verbose=args.verbose)

if __name__ == "__main__":
    main()