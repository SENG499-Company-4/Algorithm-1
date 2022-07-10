import numpy as np
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

def main():
    courses = 33
    times = 51
    teachers = 29
    dims = {"courses":courses, "times":times, "teachers":teachers}

    """
    with open("prefs.csv", "r") as fprefs:
        prefs = np.loadtxt("prefs.csv", delimiter=",", dtype=np.int16)

    rows, cols = prefs.shape
    for i in range(rows):
        for j in range(cols):
            prefs[i, j] = val_map[prefs[i, j]]
    """
    
    prefs = np.random.randint(7, size=(teachers, courses), dtype=np.uint8)
    avails = np.array([3 for i in range(teachers)], dtype=np.uint8)
    max_iter = 1000
    P = [0,1,2,3,4,5,6]
    p_tgt = 3

    ro = RandOpt(dims, prefs, avails, max_iter, P, p_tgt)
    ro.solve()
    print(f"connections: {ro.sparse()}\nvalid: {ro.is_valid_schedule()}")
    ro.plot()


if __name__ == "__main__":
    main()