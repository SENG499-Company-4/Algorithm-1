from gym.spaces import Box, Discrete, Dict, MultiDiscrete
from gym import Env
from action import Action
from numpy import int8, float32, array, zeros, ones, prod, tanh, median, sum, count_nonzero
from itertools import product
import numpy as np
from scipy.sparse import random

MAX_COURSES_PER_TEACHER = 3
MAX_TEACHERS_PER_COURSE = 1
MIN_TEACHERS_PER_COURSE = 1


class HyperGraphEnv(Env):
    def __init__(self, obs_dict, act_dict, preferences, P, ep_len):
        super(HyperGraphEnv).__init__()
        self.dtype = int8
        self.obs_dict = obs_dict
        self.act_dict = act_dict
        self.obs_shape = tuple(obs_dict.values())
        self.act_shape = tuple(act_dict.values())
        act_var = [range(var) for var in self.act_shape]
        cart_prod = list(product(act_var[0], act_var[1], act_var[2]))
        self.disc_to_multidisc = {idx : cart_prod[idx] for idx in range(len(cart_prod))}
        self.observation_space = Dict(
            {
                "obs": Box(low=0, high=1, shape=self.obs_shape, dtype=self.dtype),
                "action_mask": Box(low=0, high=1, shape=self.obs_shape, dtype=self.dtype)

            }
        )
        self.action_space = Discrete(prod(self.act_shape))
        self.P = P
        self.preferences = preferences
        self.num_actions = 0
        self.max_episode_steps = ep_len
        self.reward = 0.0
        self.hyperedges = {}

    def step(self, action):
        self.set_state(action)
        valid_sched = self.isValidSchedule()
        done = self.isEndState(valid_sched)
        self.calcReward(valid_sched)
        observation = self.get_state()
        info = self._get_info()

        return observation, self.reward, done, info

    def render(self):
        pass

    def reset(self, seed=None, return_info=None):
        super().reset(seed=seed)
        self.num_actions = 0
        self.reward = 0.0
        self.hyperedges.clear()
        self.preferences = self._randomize_matrix(self.obs_dict["courses"],self.obs_dict["teachers"])
        observation = self.get_state()
        info = self._get_info()

        return (observation, info) if return_info else observation

    def _randomize_matrix(self, size_x, size_y) -> np.ndarray:
        """
        Creates a Preference matrix with randomized sparse values

        size_x: num of courses (x-axis)
        size_y: num of teachers (y-axis)
        """
        matrix = np.zeros(shape=(size_x, size_y), dtype=np.int8)
        mask = random(size_x,size_y, density=0.25, data_rvs=np.ones, dtype=np.int8).astype(bool).A
        random_matrix = np.random.randint(0, 7, size=matrix.shape)
        matrix[mask] = random_matrix[mask]
        return matrix

    def set_state(self, act):
        action = self.disc_to_multidisc[act]
        action = Action(action)
        location = action.location
        connection = action.connection

        if connection == 1:
            self.hyperedges[location] = 1

        elif location in self.hyperedges \
                and connection == 0:
            del self.hyperedges[location]

        self.num_actions += 1

    def isEndState(self, valid_sched):
        if self.num_actions >= self.max_episode_steps \
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
        if not valid_sched:
            return
        r0 = 1
        ri = 1 
        card_c = self.obs_dict["courses"]

        tc_pairs = [(loc[0], loc[1]) for loc in self.hyperedges.keys()]
        p_hat = array([self.preferences[i, j] for i, j in tc_pairs], dtype=self.dtype)

        R = sum(tanh(p_hat - median(self.P)), dtype=float32)

        #if valid_sched:
        R += r0 * card_c

        self.reward = R

    def sparseToDense(self):
        state = zeros(self.obs_shape, dtype=self.dtype)

        for loc, conn in self.hyperedges.items():
            state[loc[0], loc[1]] = conn
        
        return state

    def get_state(self):
        #state = self.sparseToDense()
        #valid_act = ones(self.obser, dtype=self.dtype)
        valid_actions = Box(low=0, high=1, shape=self.obs_shape, dtype=self.dtype)
        return self.sparseToDense()
    
    def _get_info(self):
        return {}        