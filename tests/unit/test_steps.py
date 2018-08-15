# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from unittest import TestCase, mock
from deploy_ostree.config import Config
from deploy_ostree.steps import DeploySteps, get_deploy_steps


def mock_teststep(relevant: bool, n_steps: int = 1) -> mock.Mock:
    teststep = mock.Mock()
    teststep.is_relevant.return_value = relevant
    teststep.get_steps.return_value = [teststep] * n_steps
    teststep.title = 'test step'
    return teststep


def verify_relevant(teststep: mock.Mock, cfg: Config, n_calls: int = 1) -> None:
    teststep.is_relevant.assert_called_once_with(cfg)
    teststep.get_steps.assert_called_once_with(cfg)
    teststep.run.assert_has_calls([mock.call()] * n_calls)


def verify_irrelevant(teststep: mock.Mock, cfg: Config) -> None:
    teststep.is_relevant.assert_called_once_with(cfg)
    teststep.get_steps.assert_not_called()
    teststep.run.assert_not_called()


class TestDeploySteps(TestCase):
    cfg = mock.Mock()

    def test_should_run_steps_that_are_relevant(self):
        teststep = mock_teststep(True)

        deploy_steps = DeploySteps(self.cfg, [teststep])
        deploy_steps.run()

        verify_relevant(teststep, self.cfg)

    def test_should_not_run_steps_that_are_not_relevant(self):
        teststep1 = mock_teststep(True)
        teststep2 = mock_teststep(False)

        deploy_steps = DeploySteps(self.cfg, [teststep1, teststep2])
        deploy_steps.run()

        verify_relevant(teststep1, self.cfg)
        verify_irrelevant(teststep2, self.cfg)

    def test_should_not_run_steps_that_return_empty_lists(self):
        teststep = mock_teststep(True, 0)

        deploy_steps = DeploySteps(self.cfg, [teststep])
        deploy_steps.run()

        teststep.is_relevant.assert_called_once_with(self.cfg)
        teststep.get_steps.assert_called_once_with(self.cfg)
        teststep.run.assert_not_called()

    def test_should_run_multiple_returned_steps(self):
        teststep = mock_teststep(True, 4)

        deploy_steps = DeploySteps(self.cfg, [teststep])
        deploy_steps.run()

        verify_relevant(teststep, self.cfg, 4)

    def test_should_cleanup_all_steps_in_reverse_order(self):
        mgr = mock.Mock()
        teststep1 = mock_teststep(True, 1)
        teststep2 = mock_teststep(True, 1)
        teststep3 = mock_teststep(True, 1)
        mgr.attach_mock(teststep1, 't1')
        mgr.attach_mock(teststep2, 't2')
        mgr.attach_mock(teststep3, 't3')

        deploy_steps = DeploySteps(self.cfg, [teststep1, teststep2, teststep3])
        deploy_steps.run()
        deploy_steps.cleanup()

        self.assertEqual(mgr.mock_calls[6:], [
            mock.call.t1.run(),
            mock.call.t2.run(),
            mock.call.t3.run(),
            mock.call.t3.cleanup(),
            mock.call.t2.cleanup(),
            mock.call.t1.cleanup(),
        ])


class TestGetDeploySteps(TestCase):
    cfg = mock.Mock()

    @mock.patch('deploy_ostree.steps.DeploySteps')
    def test_should_pass_all_deploy_steps(self, mock_deploysteps):
        mocks = [(clsname, mock.Mock()) for clsname in [
            'HttpRemote',
            'FileRemote',
            'PullRef',
            'CreateStateroot',
            'Deploy',
            'MountVar',
            'DefaultProvisioner',
        ]]

        with mock.patch.multiple('deploy_ostree.steps', **{clsname: mock for clsname, mock in mocks}):
            result = get_deploy_steps(self.cfg)

        self.assertIs(result, mock_deploysteps.return_value)
        mock_deploysteps.assert_called_once_with(self.cfg, [mock for clsname, mock in mocks])
