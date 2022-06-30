import gym, ray
from ray import tune
from hypergraph import HyperGraphEnv
from ray.rllib.agents import ppo
from ray.tune.registry import register_env
import numpy as np
import os

def env_creator(env_config):
    return HyperGraphEnv(
        env_config["obs_dict"], 
        env_config["act_dict"], 
        env_config["preferences"], 
        env_config["P"], 
        env_config["ep_len"]
    )

val_map = {
    0 : 0,
    20 : 1,
    39 : 2,
    40 : 3,
    78 : 4,
    100 : 5,
    195 : 6
}

def main():
    with open("prefs.csv", "r") as fprefs:
        prefs = np.loadtxt("prefs.csv", delimiter=",", dtype=np.int16)

    rows, cols = prefs.shape
    for i in range(rows):
        for j in range(cols):
            prefs[i, j] = val_map[prefs[i, j]]

    teachers = 15
    courses = 15
    times = 3
    actions = 2
    steps = 2 * courses

    env_config = {
        "obs_dict" : {"teachers":teachers, "courses":courses},
        "act_dict" : {"teachers":teachers, "courses":courses, "actions":actions},
        "P" : np.arange(7),
        "preferences" : prefs,
        "ep_len" : steps
    }

    nn_config = {
        "use_attention" : True
    }

    agent_config = {
        "env" : "HyperGraphEnv",
        "env_config" : env_config,
        "num_gpus" : 1,
        "num_workers" : 1,
        "framework" : "tf2",
        "eager_tracing" : True,
        "horizon" : steps,
        "model" : nn_config
    }

    stop = {
        "training_iteration" : 40,
        "done" : True
    }
    
    register_env("HyperGraphEnv", env_creator)

    ray.init(
        #object_store_memory = 2048 * 1024 * 1024,
        num_gpus = 1,
        num_cpus = 6
    )

    tune.run(
        "R2D2",
        name = "HyperGraphEnv",
        local_dir = "./tune_output/",
        stop = stop,
        config = agent_config
    )

if __name__ == '__main__':
    main()

