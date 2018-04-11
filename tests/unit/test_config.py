# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from io import StringIO
from unittest import TestCase
from deploy_ostree.config import Config


class TestConfig(TestCase):
    def test_should_parse_config_with_url_and_ref(self):
        json = '''{
            "ostree_url": "https://example.com/ostree",
            "ref": "fedora/28/x86_64/workstation",

            "ignored key": "ignored value"
        }'''

        cfg = Config.parse_json(StringIO(json))
        self.assertEqual('https://example.com/ostree', cfg.url)
        self.assertEqual('fedora/28/x86_64/workstation', cfg.ref)
