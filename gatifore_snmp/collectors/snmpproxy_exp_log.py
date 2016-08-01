# coding=utf-8

import time
import logging
from snmpraw import SNMPRawCollector
from diamond.metric import Metric

global elog
elog = logging.getLogger('snmp')
hdlr = logging.FileHandler('/tmp/snmp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
elog.addHandler(hdlr)
elog.setLevel(logging.DEBUG)



class SNMPProxyCollector(SNMPRawCollector):

    def collect_snmp(self, device, host, port, community):
        """
        Collect SNMP interface data from device
        """

        self.log.info("Collecting raw SNMP statistics from device '{0}'".format(device))
        elog.info("Collecting raw SNMP statistics from device '{0}'".format(device))

        #for k,v in self.skip_list:
        #    self.log.info(" Skip list {0}:{1}".format(k, v))
        #    elog.info(" Skip list {0}:{1}".format(k, v))

        dev_config = self.config['devices'][device]
        if 'oids' in dev_config:
            for oid, metricName in dev_config['oids'].items():
                self.log.info("Checking {0}:{1} for device {2}".format(oid, metricName, device))
                elog.info("Checking {0}:{1} for device {2}".format(oid, metricName, device))
                if 1 == 2 and (device, oid) in self.skip_list:
                    self.log.info(
                            "Skipping OID '{0}' ({1}) on device '{2}'".format(
                                    oid, metricName, device))
                    elog.info('Skipping OID \'{0}\' ({1}) on device \'{2}\''.format(oid, metricName, device))
                    continue

                timestamp = time.time()
                self.log.info("_get_value device:{0}, oid:{1}, host:{2}, port:{3}, community:{4} ...".format(device, oid, host, port, community))
                elog.info("_get_value device:{0}, oid:{1}, host:{2}, port:{3}, community:{4} ...".format(device, oid, host, port, community))
                value = self._get_value(device, oid, host, port, community)
                if value is None:
                    self.log.info("Value is None for device:{0}, oid:{1}, host:{2}, port:{3}, community:{4}".format(device, oid, host, port, community))
                    elog.info("Value is None for device:{0}, oid:{1}, host:{2}, port:{3}, community:{4}".format(device, oid, host, port, community))
                    continue

                self.log.info("'{0}' ({1}) on device '{2}' - value=[{3}]".format(oid, metricName, device, value))
                elog.info("'{0}' ({1}) on device '{2}' - value=[{3}]".format(oid, metricName, device, value))

                device_path = '{}.{}.{}'.format(dev_config['node_id'], device, dev_config['node_instance_id'])
                self.log.info("device '{0}' , device_path {1}, value {2}".format(device, device_path, value))
                elog.info("device '{0}' , device_path {1}, value {2}".format(device, device_path, value))

                path = '.'.join([self.config['path_prefix'], device_path,
                                 self.config['path_suffix'], metricName])

                self.log.info("path '{0}' , device_path {1}, metricName {2}".format(path, device_path, metricName))
                elog.info("path '{0}' , device_path {1}, metricName {2}".format(path, device_path, metricName))

                metric = Metric(path=path, value=value, timestamp=timestamp,
                                precision=self._precision(value),
                                host=device_path, metric_type='GAUGE')
                self.publish_metric(metric)

