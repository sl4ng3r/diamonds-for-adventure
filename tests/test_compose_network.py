import ipaddress
import json
import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ComposeNetworkTests(unittest.TestCase):
    def config(self, subnet):
        env = dict(os.environ, BEDROCK_NETWORK_SUBNET=subnet)
        output = subprocess.check_output(
            ['docker', 'compose', 'config', '--format', 'json'],
            cwd=ROOT, env=env, text=True,
        )
        return json.loads(output)

    def test_network_is_configurable_and_does_not_overlap_home(self):
        subnet = '10.254.251.0/24'
        config = self.config(subnet)
        actual = config['networks']['default']['ipam']['config'][0]['subnet']
        self.assertEqual(actual, subnet)
        self.assertFalse(ipaddress.ip_network(actual).overlaps(ipaddress.ip_network('192.168.1.0/24')))

    def test_subnet_can_be_changed(self):
        config = self.config('10.253.42.0/24')
        self.assertEqual(config['networks']['default']['ipam']['config'][0]['subnet'], '10.253.42.0/24')
