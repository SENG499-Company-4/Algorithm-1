from sched import scheduler
from hyperopt import hp
import gym, ray
from ray import tune
from hypergraph import HyperGraphEnv
from ray.rllib.agents import ppo
from ray.rllib.algorithms import alpha_zero
from ray.tune.registry import register_env
from ray.tune import schedulers
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
        "ep_len" : 250
    },
    #"disable_env_checking" : True,
    "num_gpus" : int(os.environ.get("RLLIB_NUM_GPUS", "0")),
    "num_workers" : 5,
    "framework" : "torch",
    "horizon" : tune.uniform(100,250),
    "grad_clip" : tune.uniform(10,40),
    "lr" : tune.uniform(0.00005, 0.005)
}

stop = {
    "training_iteration" : 100,
    "done" : True
}


param_scheduler = schedulers.ASHAScheduler(
    time_attr="training_iteration",
    metric="episode_reward_mean",
    mode="max",
    max_t=10,
)

def main():
    analysis = tune.run(
        "IMPALA",
        name = "HyperGraphEnv",
        local_dir="./tune_output/",
        stop=stop,
        config=config,
        scheduler=param_scheduler,
        num_samples=10
    )
    print("All configs from this run -- ", analysis.get_all_configs())
    print("**************************************")
    print("Determined best params -- ", analysis.get_best_config(metric="episode_reward_mean", mode="max"))

if __name__ == '__main__':
    main()

