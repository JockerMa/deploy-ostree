# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from typing import Tuple
from unittest import TestCase, mock
from deploy_ostree.steps import DeploySteps


def mock_teststep(n_steps: int = 1) -> Tuple[mock.Mock, mock.Mock]:
    teststep = mock.Mock()
    provider = mock.Mock()
    provider.return_value = [teststep] * n_steps
    teststep.title = 'test step'
    return provider, teststep


class TestDeploySteps(TestCase):
    cfg = mock.Mock()

    def test_should_run_steps(self):
        provider, teststep = mock_teststep()

        deploy_steps = DeploySteps(self.cfg, [provider])
        deploy_steps.run()

        provider.assert_called_once_with(self.cfg)
        teststep.run.assert_called_once_with()

    def test_should_run_multiple_returned_steps(self):
        provider, teststep = mock_teststep(4)

        deploy_steps = DeploySteps(self.cfg, [provider])
        deploy_steps.run()

        provider.assert_called_once_with(self.cfg)
        teststep.run.assert_has_calls([mock.call()] * 4)

    def test_should_call_multiple_steps_providers(self):
        provider1, _ = mock_teststep()
        provider2, _ = mock_teststep()
        mgr = mock.Mock()
        mgr.attach_mock(provider1, 'p1')
        mgr.attach_mock(provider2, 'p2')

        deploy_steps = DeploySteps(self.cfg, [provider1, provider2])
        deploy_steps.run()

        self.assertEqual(mgr.mock_calls, [
            mock.call.p1(self.cfg),
            mock.call.p2(self.cfg),
        ])

    def test_should_cleanup_all_steps_in_reverse_order(self):
        provider1, teststep1 = mock_teststep()
        provider2, teststep2 = mock_teststep()
        provider3, teststep3 = mock_teststep()
        mgr = mock.Mock()
        mgr.attach_mock(teststep1, 't1')
        mgr.attach_mock(teststep2, 't2')
        mgr.attach_mock(teststep3, 't3')

        deploy_steps = DeploySteps(self.cfg, [provider1, provider2, provider3])
        deploy_steps.run()
        deploy_steps.cleanup()

        self.assertEqual(mgr.mock_calls[-6:], [
            mock.call.t1.run(),
            mock.call.t2.run(),
            mock.call.t3.run(),
            mock.call.t3.cleanup(),
            mock.call.t2.cleanup(),
            mock.call.t1.cleanup(),
        ])

    def test_should_ignore_exceptions_in_cleanup(self):
        provider, teststep = mock_teststep()
        teststep.cleanup.side_effect = Exception('cleanup error')

        deploy_steps = DeploySteps(self.cfg, [provider])
        deploy_steps.run()
        deploy_steps.cleanup()
