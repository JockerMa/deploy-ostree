# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from unittest import TestCase
from unittest import mock
from unittest.mock import Mock
from deploy_ostree.config import Config
from deploy_ostree.steps import DeploySteps


def mock_teststep(relevant: bool, n_steps: int = 1) -> Mock:
    teststep = Mock()
    teststep.is_relevant.return_value = relevant
    teststep.get_steps.return_value = [teststep] * n_steps
    teststep.title = 'test step'
    return teststep


def verify_relevant(teststep: Mock, cfg: Config, n_calls: int = 1) -> None:
    teststep.is_relevant.assert_called_once_with(cfg)
    teststep.get_steps.assert_called_once_with(cfg)
    teststep.run.assert_has_calls([mock.call()] * n_calls)


def verify_irrelevant(teststep: Mock, cfg: Config) -> None:
    teststep.is_relevant.assert_called_once_with(cfg)
    teststep.get_steps.assert_not_called()
    teststep.run.assert_not_called()


class TestDeploySteps(TestCase):
    cfg = Mock()

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
