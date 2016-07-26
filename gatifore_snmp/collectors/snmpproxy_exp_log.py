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

        self.log.debug(
                'Collecting raw SNMP statistics from device \'{0}\''.format(device)
        )
        elog.debug('Collecting raw SNMP statistics from device \'{0}\''.format(device))

        dev_config = self.config['devices'][device]
        if 'oids' in dev_config:
            for oid, metricName in dev_config['oids'].items():

                if (device, oid) in self.skip_list:
                    self.log.debug(
                            'Skipping OID \'{0}\' ({1}) on device \'{2}\''.format(
                                    oid, metricName, device))
                    elog.debug('Skipping OID \'{0}\' ({1}) on device \'{2}\''.format(oid, metricName, device))
                    continue

                timestamp = time.time()
                value = self._get_value(device, oid, host, port, community)
                if value is None:
                    continue

                self.log.debug(
                        '\'{0}\' ({1}) on device \'{2}\' - value=[{3}]'.format(
                                oid, metricName, device, value))
                elog.debug('\'{0}\' ({1}) on device \'{2}\' - value=[{3}]'.format(oid, metricName, device, value))

                device_path = '{}.{}.{}'.format(dev_config['node_id'],device,dev_config['node_instance_id'])
                path = '.'.join([self.config['path_prefix'], device_path,
                                 self.config['path_suffix'], metricName])
                metric = Metric(path=path, value=value, timestamp=timestamp,
                                precision=self._precision(value),
                                host=device_path, metric_type='GAUGE')
                self.publish_metric(metric)

