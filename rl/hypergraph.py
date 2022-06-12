from gym.spaces import MultiDiscrete
from gym import Env


class HyperGraphEnv(Env):
    def __init__(self, obs_shape, act_shape, preferences, ep_len):
        super(HyperGraphEnv).__init__()
        self.obs_shape = obs_shape
        self.act_shape = act_shape
        self.observation_space = MultiDiscrete(obs_shape)
        self.action_space = MultiDiscrete(act_shape)
        self.preferences = preferences
        self.num_actions = 0
        self.episode_length = ep_len
        self.hyperedges = {}
        self.reward = 0

    def step(self):
        
        if self.num_actions >= self.episode_length \
                or self.isValidSchedule():
            done = True
        else: 
            done = False

        info = {}

        return self.hyperedges, self.calcReward(), done, info

    def render(self):
        print(self.hyperedges)

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

    