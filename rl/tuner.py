import gym, ray
from ray import tune
from hypergraph import HyperGraphEnv
from ray.tune.registry import register_env
import numpy as np
import os

teachers = 10
courses = 10
times = 3
actions = 2


def env_creator(env_config):
    return HyperGraphEnv(env_config["obs_dict"], env_config["act_dict"], env_config["preferences"], env_config["P"], env_config["ep_len"])

register_env("HyperGraphEnv", env_creator)

ray.init()

config = {
    "env" : "HyperGraphEnv",
    "env_config" : {
        "obs_dict" : {"teachers":teachers, "courses":courses},
        "act_dict" : {"teachers":teachers, "courses":courses, "actions":actions},
        "P" : np.arange(7),
        "preferences" : np.random.randint(0, 7, (teachers, courses), dtype=np.int64),
        "ep_len" : 350
    },
    #"disable_env_checking" : True,
    "num_gpus" : 0, #int(os.environ.get("RLLIB_NUM_GPUS", "1")),
    "num_workers" : 5,
    "framework" : "tf2",
    "horizon" :350
}

stop = {
    "training_iteration" : 30,
    "done" : True
}

def main():
    tune.run(
        "PPO",
        name = "HyperGraphEnv",
        local_dir="./ppo_adj/",
        stop=stop,
        config=config
    )

if __name__ == '__main__':
    main()

