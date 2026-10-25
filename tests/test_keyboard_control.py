import argparse
import unittest
from unittest.mock import patch

import examples
from examples import configure_keyboard_control
from examples import default_on_press
from examples import disable_keyboard_control
from examples import enable_keyboard_control
from examples import is_keyboard_control_enabled
from examples import parse_run_args
from examples import runner
from examples import start_keyboard_listener
from examples import stop_keyboard_listener
from test_share.test_func import common_test_setup


class StubListener:
    """ Stands in for pynput's keyboard.Listener so that tests never start a real (OS-level) keyboard listener. """
    instances: list['StubListener'] = []

    def __init__(self, on_press=None, **_kwargs):
        self.on_press = on_press
        self.n_starts = 0
        self.n_stops = 0

        StubListener.instances.append(self)

    def start(self) -> None:
        self.n_starts += 1

    def stop(self) -> None:
        self.n_stops += 1


def run_stub(**kwargs) -> dict:
    return kwargs


class TestKeyboardControl(unittest.TestCase):
    def setUp(self) -> None:
        common_test_setup()

        # reset the process-wide listener state (before patching, so any real listener is stopped for real)
        stop_keyboard_listener()
        enable_keyboard_control()

        StubListener.instances = []
        self.listener_patcher = patch.object(examples.keyboard, 'Listener', StubListener)
        self.listener_patcher.start()

    def tearDown(self) -> None:
        stop_keyboard_listener()
        enable_keyboard_control()

        self.listener_patcher.stop()

    def test_one_listener_shared_across_episodes(self):
        run = runner(run_stub)

        # test: running many episodes SHOULD start exactly one listener, with the runner's on_press callback
        for episode in range(5):
            self.assertDictEqual({'episode': episode}, run(episode=episode))

        self.assertEqual(1, len(StubListener.instances))

        listener = StubListener.instances[0]
        self.assertEqual(1, listener.n_starts)
        self.assertEqual(0, listener.n_stops)
        self.assertIs(default_on_press, listener.on_press)

    def test_start_keyboard_listener_is_idempotent(self):
        # test: repeated starts SHOULD reuse the running listener
        start_keyboard_listener(on_press=default_on_press)
        start_keyboard_listener(on_press=default_on_press)

        self.assertEqual(1, len(StubListener.instances))
        self.assertEqual(1, StubListener.instances[0].n_starts)

    def test_stop_keyboard_listener(self):
        run = runner(run_stub)
        run()

        # test: stopping SHOULD stop the shared listener exactly once (including when called repeatedly)
        stop_keyboard_listener()
        stop_keyboard_listener()

        self.assertEqual(1, StubListener.instances[0].n_stops)

        # test: a later episode SHOULD start a new listener
        run()

        self.assertEqual(2, len(StubListener.instances))
        self.assertEqual(1, StubListener.instances[1].n_starts)

    def test_disabled_keyboard_control_starts_no_listener(self):
        disable_keyboard_control()
        self.assertFalse(is_keyboard_control_enabled())

        # test: no listener SHOULD be created while keyboard control is disabled
        run = runner(run_stub)
        for episode in range(3):
            run(episode=episode)

        self.assertEqual(0, len(StubListener.instances))

    def test_disable_keyboard_control_stops_running_listener(self):
        runner(run_stub)()
        self.assertEqual(0, StubListener.instances[0].n_stops)

        # test: disabling keyboard control SHOULD stop an already-running listener
        disable_keyboard_control()
        self.assertEqual(1, StubListener.instances[0].n_stops)

    def test_configure_keyboard_control(self):
        # test: interactive runs (neither --optimize nor --no_keyboard) SHOULD keep keyboard control enabled
        configure_keyboard_control(argparse.Namespace(optimize=False, no_keyboard=False))
        self.assertTrue(is_keyboard_control_enabled())

        # test: arguments without either attribute (e.g., scripts that don't define them) SHOULD keep it enabled
        configure_keyboard_control(argparse.Namespace())
        self.assertTrue(is_keyboard_control_enabled())

        # test: --optimize SHOULD disable keyboard control
        configure_keyboard_control(argparse.Namespace(optimize=True, no_keyboard=False))
        self.assertFalse(is_keyboard_control_enabled())

        enable_keyboard_control()

        # test: --no_keyboard SHOULD disable keyboard control
        configure_keyboard_control(argparse.Namespace(optimize=False, no_keyboard=True))
        self.assertFalse(is_keyboard_control_enabled())

    def test_no_keyboard_cli_flag(self):
        parser = parse_run_args(argparse.ArgumentParser())

        # test: keyboard control SHOULD be on by default, and --no_keyboard SHOULD turn it off
        self.assertFalse(parser.parse_args([]).no_keyboard)
        self.assertTrue(parser.parse_args(['--no_keyboard']).no_keyboard)
