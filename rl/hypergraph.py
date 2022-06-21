from gym.spaces import MultiDiscrete
from gym import Env
import json
from datetime import date
import sys
from action import Action
from numpy import int16, array, zeros, tanh, median, sum, count_nonzero

MAX_COURSES_PER_TEACHER = 3
MAX_TEACHERS_PER_COURSE = 1
MIN_TEACHERS_PER_COURSE = 1


class HyperGraphEnv(Env):
    def __init__(self, obs_dict, act_dict, preferences, P, ep_len):
        super(HyperGraphEnv).__init__()
        self.dtype = int16
        self.obs_dict = obs_dict
        self.act_dict = act_dict
        self.observation_space = MultiDiscrete(tuple(obs_dict.values()))
        self.action_space = MultiDiscrete(tuple(act_dict.values()))
        self.P = P
        self.preferences = preferences
        self.num_actions = 0
        self.episode_length = ep_len
        self.reward = 0
        self.hyperedges = {}
        self.output_file_name = "logs/{}-render-output.txt".format(date.today().strftime("%d_%m_%Y"))
        self.output_to_file = True

    def step(self, action):
        self.updateState(action)
        valid_sched = self.isValidSchedule()
        done = self.isEndState(valid_sched)
        self.calcReward(valid_sched)
        observation = self._get_obs()
        info = {}

        return observation, self.reward, done, info

    def render(self):
        pass

    def reset(self, seed=None, return_info=None):
        super().reset(seed=seed)
        self.num_actions = 0
        self.reward = 0
        self.hyperedges.clear()
        observation = self._get_obs()
        info = self._get_info()
        return (observation, info) if return_info else observation

    def updateState(self, action):
        location = action.location
        connection = action.connection

        if connection == 1:
            self.hyperedges[location] = 1

        elif location in self.hyperedges \
                and connection == 0:
            del self.hyperedges[location]

        self.num_actions += 1

    def isEndState(self, valid_sched):
        if self.num_actions >= self.episode_length \
                or valid_sched:
            return True
        return False

    def isValidSchedule(self):
        state = self.sparseToDense()
        num_courses_per_teacher = count_nonzero(state, axis=1)
        num_teachers_per_course = count_nonzero(state, axis=0)
        
        if num_teachers_per_course[num_teachers_per_course < MIN_TEACHERS_PER_COURSE].size > 0:
            return False
        
        if num_teachers_per_course[num_teachers_per_course > MAX_TEACHERS_PER_COURSE].size > 0:
            return False

        if num_courses_per_teacher[num_courses_per_teacher > MAX_COURSES_PER_TEACHER].size > 0:
            return False
        
        return True

    def calcReward(self, valid_sched):
        r0 = 1
        ri = 1 
        card_c = self.obs_dict["courses"]

        tc_pairs = [(loc[0], loc[1]) for loc in self.hyperedges.keys()]
        p_hat = array([self.preferences[i, j] for i, j in tc_pairs], dtype=self.dtype)

        R = sum(tanh(p_hat - median(self.P)))

        if valid_sched:
            R += r0 * card_c

        self.reward = R

    def sparseToDense(self):
        teachers, courses = self.obs_dict["teachers"], self.obs_dict["courses"]
        state = zeros((teachers, courses), dtype=self.dtype)

        for loc, conn in self.hyperedges.items():
            state[loc[0], loc[1]] = conn
        
        return state

    def _get_obs(self):
        state = self.sparseToDense()
        shape = (2, state.shape[0], state.shape[1])
        observation = zeros(shape, dtype=self.dtype)
        observation[0, :, :] = state
        observation[-1, :, :] = self.preferences 
        
        return observation

    def _get_info(self):
        return {}
        