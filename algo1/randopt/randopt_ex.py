import numpy as np
import multiprocessing as mp
import time
from rand_opt import RandOpt


val_map = {
    0 : 0,
    20 : 1,
    39 : 2,
    40 : 3,
    78 : 4,
    100 : 5,
    195 : 6
}

def async_random_search(ro):
    ro.solve()
    if ro.is_valid_schedule(): 
        return ro
    return None

def main():
    courses = 33
    times = 51
    teachers = 29
    dims = {"courses":courses, "times":times, "teachers":teachers}

    #"""
    with open("prefs.csv", "r") as fprefs:
        prefs = np.loadtxt("prefs.csv", delimiter=",", dtype=np.int16)

    rows, cols = prefs.shape
    for i in range(rows):
        for j in range(cols):
            prefs[i, j] = val_map[prefs[i, j]]
    #"""
    
    #prefs = np.random.randint(7, size=(teachers, courses), dtype=np.uint8)
    avails = [3 for _ in range(teachers)] #np.random.randint(1, 4, size=(teachers,), dtype=np.uint8)
    max_iter = 1500
    P = np.arange(7, dtype=np.uint8)
    p_tgt = 3
    num_workers = 20

    mp.set_start_method("spawn")
    with mp.get_context("spawn").Pool() as pool:
        ro_type = type(RandOpt(dims, prefs, avails, max_iter))
        ret_types = []
        max_runtime = 600
        start_time = time.time()
        while ro_type not in ret_types and (time.time() - start_time) < max_runtime:
            ro_obs = [RandOpt(dims, prefs, avails, max_iter) for i in range(num_workers)]
            res = pool.map(async_random_search, ro_obs)
            ret_types = [type(elem) for elem in res]
        
        valid_schedules = [schd for schd in res if isinstance(schd, ro_type)]
        
        for schd in valid_schedules:
            print(f"connections:\n{schd.sparse()}\nreward: {schd.calc_reward()}\niterations: {schd.iter+1}")
        
        if len(valid_schedules) > 0:
            valid_schedules[0].plot()

if __name__ == "__main__":
    main()