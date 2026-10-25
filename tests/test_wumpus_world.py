"""Focused Wumpus checks authored by Codex at the researcher's request.

The original seven checks were authored by Codex. Hazel adapted the observation
test with guidance to verify distinct current-cell and forward-cell labels.
These cover selected deterministic cases, not learning performance or all
world layouts.

"""

import unittest


from examples.environments.wumpus_world import get_agent_observation
from examples.environments.wumpus_world import MOVE_FORWARD
from examples.environments.wumpus_world import TURN_RIGHT
from examples.environments.wumpus_world import USE_EXIT
from examples.environments.wumpus_world import WumpusWorldAgent
from examples.environments.wumpus_world import WumpusWorldMdp


class TestWumpusWorld(unittest.TestCase):
    # Grid indexing is (row, column). The exit at (1, 2) has a wall east of it.
    WORLD_MAP = """wwwww
                   w.eww
                   w...w
                   wwwww"""  # Class attribute, like a static field

    def make_env(self, position=(1, 1), direction='E') -> WumpusWorldMdp:
        env = WumpusWorldMdp(
            world_id='test-wumpus',
            world_map=self.WORLD_MAP,
            agent=WumpusWorldAgent(position, direction),
            randomized_start=False,
        )
        env.reset()
        return env

    def test_right_turn_changes_direction_not_position(self):
        env = self.make_env(position=(1, 1), direction='E')
        state, terminal = env.step(TURN_RIGHT)

        self.assertEqual(env.agent.position, (1, 1))
        self.assertEqual(env.agent.direction, 'S')
        self.assertIn('AGENT.DIR=S', state)
        self.assertFalse(terminal)

    def test_forward_move_into_free_cell(self):
        env = self.make_env(position=(1, 1), direction='S')

        _, terminal = env.step(MOVE_FORWARD)

        self.assertEqual(env.agent.position, (2, 1))
        self.assertFalse(terminal)

    def test_wall_blocks_forward_move(self):
        env = self.make_env(position=(1, 2), direction='E')
        env.step(MOVE_FORWARD)

        self.assertEqual(env.agent.position, (1, 2))
        self.assertEqual(env.env.cells[env.agent.position], 'e')

    def test_facing_exit_does_not_escape(self):
        env = self.make_env(position=(1, 1), direction='E')
        _, terminal = env.step(USE_EXIT)

        self.assertFalse(env.agent.has_escaped)
        self.assertFalse(terminal)

    def test_using_exit_terminates_and_rejects_further_steps(self):
        env = self.make_env(position=(1, 2), direction='E')
        state, terminal = env.step(USE_EXIT)

        self.assertTrue(terminal)
        self.assertIn('EVENT[AGENT ESCAPED]', state)
        with self.assertRaises(ValueError):
            env.step(TURN_RIGHT)

    def test_reset_restores_agent_after_escape(self):
        env = self.make_env(position=(1, 2), direction='E')
        env.step(USE_EXIT)
        _, terminal = env.reset()

        self.assertFalse(terminal)
        self.assertFalse(env.agent.has_escaped)
        self.assertEqual(env.episode_summary.steps, 0)

    def test_observation_distinguishes_current_and_forward_cells(self):
        #Arrange
        env = self.make_env(position=(1, 2), direction='E')

        #Act
        observation = get_agent_observation(env.env, env.agent, env.wumpus) # No Wumpus in the test

        #Assert: check whether observation contain what I predicted
        self.assertIn('IN_CELL_WITH_AGENT=e', observation) # Must be present
        self.assertIn('IN_FRONT_OF_AGENT=w', observation)  # Must be present
        self.assertNotIn('IN_CELL_WITH_AGENT=w', observation) # Must be absent

if __name__ == '__main__':
    unittest.main()
