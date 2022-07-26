import time
import numpy as np
import multiprocessing as mp
from matplotlib import pyplot as plt
from times import Times
from rand_opt import RandOpt


def get_orig_prefs(fname):
    val_map = {0:0, 20:1, 39:2, 40:3, 78:4, 100:5, 195:6}
    with open(fname, "r") as fprefs:
        prefs = np.loadtxt("prefs.csv", delimiter=",", dtype=np.int16)
    rows, cols = prefs.shape
    for i in range(rows):
        for j in range(cols):
            prefs[i, j] = val_map[prefs[i, j]]
    return prefs

def generate_prefs(dims, seed_prefs):
    courses, _, teachers = dims.values()
    P = np.arange(0, 7)
    p_counts, bins = np.histogram(seed_prefs, bins=np.arange(0,8))
    pref_probs = p_counts / p_counts.sum()
    prefs = np.random.choice(P, size=(teachers, courses), p=pref_probs)
    return prefs

def async_random_search(ro):
    ro.solve()
    if ro.is_valid_schedule(): 
        return ro
    return None

def schedule(dims, prefs, avails, course_names, time_names, teacher_names):
    courses, times, teachers = dims.values()
    max_iter = 1500
    P = np.arange(7, dtype=np.uint8)
    p_tgt = 3
    num_workers = 20

    mp.set_start_method("spawn")
    with mp.get_context("spawn").Pool() as pool:
        ro_type = type(RandOpt(dims, prefs, avails, max_iter, P, p_tgt))
        ret_types = []
        max_runtime = 600
        start_time = time.time()
        while ro_type not in ret_types and (time.time() - start_time) < max_runtime:
            ro_objects = [RandOpt(dims, prefs, avails, max_iter, P, p_tgt) for i in range(num_workers)]
            res = pool.map(async_random_search, ro_objects)
            ret_types = [type(elem) for elem in res]
        
        valid_schedules = [schd for schd in res if isinstance(schd, ro_type)]
        valid_schd = valid_schedules[0]
        valid_schd.plot_3d()
        valid_schd.plot_hg(course_names, time_names, teacher_names)

def main():
    course_names = [
        "CSC111", 
        "CSC115",	
        "CSC225", 
        "CSC226",	
        "CSC230", 
        "SENG265", 
        "SENG275", 
        "CSC320", 
        "CSC355",	
        "CSC360", 
        "CSC361",	
        "CSC370", 
        "SENG310", 
        "SENG321",	
        "SENG350", 
        "SENG360", 
        "SENG371", 
        "CSC460", 
        "SENG401", 
        "SENG411", 
        "SENG421",	
        "SENG435", 
        "SENG466", 
        "SENG474"
    ]
    
    day = {True:"MW", False:"TWF"}
    time_names = [f"({day[ti.monday]},{ti.beginTime})" for ti in Times.values()]
    
    teacher_names = [   
        "Berg, Celina", 
        "Bird, Bill", 
        "Chester, Sean", 
        "Corless, Jason", 
        "Damian, Daniela", 
        "Ernst, Neil", 
        "Estey, Anthony", 
        "Ganti, Sudhakar", 
        "German, Daniel",
        "Haworth, Brandon"
        "Jabbari, Hosna",
        "Jackson, LillAnne",
        "Kapron, Bruce",
        "King, Valerie",
        "Koroth, Sajin",
        "Little, Rich",
        "Mehta, Nishant",
        "Muller, Hausi",
        "Nacenta, Miguel",
        "Numanagić, Ibrahim",
        "Pan, Jianping",
        "Perin, Charles",
        "Schneider, Teseo",
        "Somanath, Sowmya",
        "Srinivasan, Venkatesh",
        "Stege, Ulrike",
        "Storey, Margaret-Anne",
        "Summers, Cecilia",
        "Thomo, Alex",
        "Tzanetakis, George",
        "Weber, Jens",
        "Wu, Kui",
        "Zastre, Michael"
    ]

    courses, times, teachers = (len(course_names), len(time_names), len(teacher_names))
    dims = {"courses":courses, "times":times, "teachers":teachers}
    orig_prefs = get_orig_prefs("prefs.csv")
    prefs = generate_prefs(dims, orig_prefs)
    avails = [3 for i in range(teachers)] #np.random.randint(1, 4, size=(teachers,), dtype=np.uint8)
    schedule(dims, prefs, avails, course_names, time_names, teacher_names)


if __name__ == "__main__":
    main()