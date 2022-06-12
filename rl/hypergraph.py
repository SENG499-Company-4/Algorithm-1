from gym.spaces import MultiDiscrete
from gym import Env
import json
from datetime import date
import sys


class HyperGraphEnv(Env):
    def __init__(self, obs_shape, act_shape, preferences, ep_len):
        super(HyperGraphEnv).__init__()
        self.obs_shape = obs_shape
        self.act_shape = act_shape
        self.observation_space = MultiDiscrete(obs_shape)
        self.action_space = MultiDiscrete(act_shape)
        self._agent_location = tuple(self.observation_space.sample())
        self.preferences = preferences
        self.num_actions = 0
        self.episode_length = ep_len
        self.hyperedges = {}
        self.reward = 0
        self.output_file_name = "logs/{}-render-output.txt".format(date.today().strftime("%d_%m_%Y"))
        self.output_to_file = True

    def step(self):
        
        if self.num_actions >= self.episode_length \
                or self.isValidSchedule():
            done = True
        else: 
            done = False

        info = {}

        return self.hyperedges, self.calcReward(), done, info

    def render(self):
        with open(self.output_file_name, 'w') as f:
            file = sys.stdout
            if self.output_to_file:
                file=f
            print("Taken {} actions out of {} allowed for an episode.".format(self.num_actions, self.episode_length), file=file)
            print("Agent is visting location: {}".format(self._agent_location), file=file)
            print("Current state of hypergraph:", file=file)
            print(json.dumps(self.hyperedges, indent=4, sort_keys=False), file=file)
            print("**************************************************", file=file)

    def reset(self, seed=None):
        super().reset(seed=seed)
        self._agent_location = tuple(self.observation_space.sample())
        self.reward = 0
        self.hyperedges.clear()

    def isValidSchedule(self):
        pass

    def getReward(self):
        pass

    def _get_obs(self):
        pass

    