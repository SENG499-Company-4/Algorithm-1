from gym.spaces import Dict, MultiDiscrete
from gym import Env


class HyperGraphEnv(Env):
    def __init__(self, obs_shape, act_shape, preferences, ep_len):
        super(HyperGraphEnv).__init__()
        self.obs_shape = obs_shape
        self.act_shape = act_shape
        self.observation_space = MultiDiscrete(obs_shape)
        self.action_space = MultiDiscrete(act_shape)
        self.preferences = preferences
        self.episode_length = ep_len
        self.hyperedges = {}
        self.reward = 0

    def step(self):
        pass

    def render(self):
        pass

    def reset(self, seed=None):
        super().reset(seed=seed)

        self._agent_location = self.observation_space.sample() #outputs array not tuple

    def isValidSchedule(self):
        pass

    def getReward(self):
        pass

    def _get_obs(self):
        pass

    