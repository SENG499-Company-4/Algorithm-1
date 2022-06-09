from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
from os import environ
import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts

OBS_SHAPE = (52,60)

class ScheduleEnv (py_environment.PyEnvironment):
    def __init__(self):
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int8, minimum=0, maximum=14, name='action'
        )

        self._observation_spec = array_spec.ArraySpec(
            shape=OBS_SHAPE, dtype=np.int8, name='observation'
        )

        self._obs = np.zeros(OBS_SHAPE, dtype=np.int8)
        self._index = np.zeros((2,), dtype=np.int32)
        self._episode_ended = False

    def _set_preference(self, pref):
        self._obs[self._index[0], self._index[1]] = pref

    def _move_index(self, ind):
        self._index = ind

    def _validate_schedule(self):
        a = np.count_nonzero(self._obs, axis = 1)
        return (a == 0).sum() == 0

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._obs = np.zeros(OBS_SHAPE)
        self._index = np.zeros((2,), dtype=np.int32)
        self._episode_ended = False
        return ts.restart(np.array([self._obs], dtype=np.int8))

    def _step(self, action):
        if self._episode_ended:
            return self.reset()
        
        if 0 <= action <= 6:
            self._set_preference(action)
        
        elif action == 7:
            self._index = (self._index[0] + 1, self._index[1])
        
        elif action == 8:
            self._index = (self._index[0] - 1, self._index[1])

        elif action == 9:
            self._index = (self._index[0], self._index[1] - 1)
        
        elif action == 10:
            self._index = (self._index[0], self._index[1] + 1)

        elif action == 11:
            self._index = (self._index[0] + 1, self._index[1] + 1)
        
        elif action == 12:
            self._index = (self._index[0] - 1, self._index[1] - 1)

        elif action == 13:
            self._index = (self._index[0] + 1, self._index[1] - 1)
        
        elif action == 14:
            self._index = (self._index[0] - 1, self._index[1] + 1)
        
        if self._episode_ended or self._validate_schedule == True:
            return ts.termination(np.array([self._obs], dtype=np.int8), 1)
        else:
            return ts.transition(np.array([self._obs], dtype=np.int8), reward = 0.0, discount = 1.0)
        

def main():
    environment = ScheduleEnv()
    time_step = environment.reset()
    print(time_step)
    cumulative_reward = time_step.reward

    for i in range(6):
        time_step = environment.step(i)
        print(time_step)
    time_step = environment.step(7)
    print(time_step)
    time_step = environment.step(3)
    print(time_step)
    time_step = environment.step(11)
    print(time_step)
    time_step = environment.step(4)
    print(time_step)
    return 0 

if __name__ == '__main__':
    main()