from hypergraph import HyperGraphEnv
from action import Action
import numpy as np


def main():
    teachers = 10
    courses = 10
    times = 3
    actions = 2

    obs_d = {"teachers":teachers, "courses":courses}
    act_d = {"teachers":teachers, "courses":courses, "actions":actions}
    P = np.array([0,1,2,3,4,5,6])
    prefs = np.random.randint(0, P.size, (teachers, courses), dtype=np.int64)
    ep_len = 500
    hg = HyperGraphEnv(obs_d, act_d, prefs, P, ep_len)

    for _ in range(50):
        sample = hg.action_space.sample()
        action = Action(tuple(sample[:-1]), sample[-1])
        obs, rew, done, _ = hg.step(action)
        print(f"done: {done}\nreward: {rew}\nprefs:\n{obs['preferences']}\nhypergraph:\n{obs['hypergraph']}\n\n")

        
    

if __name__ == "__main__":
    main()