from typing import List
import numpy as np
import sys
from sudoku_schedule import ScheduledClass

COURSE_PER_PROF = 3
COOLDOWN_RATE = 28
BAD_ATTEMPT_MAX = 90

ECE_matrix = [
    [ 0, 0, 0, 0, 0, 0, 195, 195, 0, 100, 0, 0, 0, 0, 0, 0, 40, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20], 
	[ 0, 0, 0, 0, 40, 0, 0, 40, 0, 40, 0, 40, 0, 0, 0, 0, 195, 0, 0, 20, 40, 0, 0, 0, 0, 0, 0, 39, 0, 0, 0, 0, 0], 
	[ 0, 0, 40, 39, 0, 78, 20, 0, 0, 40, 78, 0, 0, 0, 40, 78, 0, 0, 0, 0, 0, 20, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 20], 
	[ 0, 0, 195, 78, 100, 100, 0, 20, 0, 78, 40, 0, 0, 78, 100, 78, 0, 0, 0, 0, 40, 195, 195, 100, 40, 0, 0, 0, 0, 0, 0, 0, 0], 
	[195, 78, 0, 0, 78, 0, 20, 40, 195, 78, 40, 195, 78, 78, 0, 0, 0, 78, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[ 0, 0, 0, 0, 0, 20, 100, 20, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 195, 40, 0, 0, 40, 0, 0, 39, 0, 0, 0, 0, 20], 
	[ 0, 0, 0, 0, 0, 0, 40, 0, 0, 20, 0, 40, 0, 78, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 195, 195, 0, 0, 0, 0, 0, 0, 0], 
	[ 0, 0, 195, 0, 40, 100, 0, 0, 0, 39, 0, 0, 0, 0, 100, 0, 195, 0, 0, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[ 40, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[ 0, 0, 40, 0, 195, 40, 0, 0, 0, 0, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 195, 40, 0, 0, 39, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 20, 0, 40, 0, 20, 100, 0, 0, 0, 100, 0, 0, 39, 0, 0, 0, 39, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[ 0, 0, 0, 0, 0, 40, 40, 0, 0, 20, 0, 0, 40, 0, 40, 0, 195, 195, 0, 0, 78, 0, 0, 0, 195, 195, 0, 100, 0, 0, 0, 0, 0], 
	[0, 0, 78, 0, 78, 78, 40, 0, 40, 40, 0, 40, 0, 40, 78, 0, 78, 40, 0, 0, 0, 0, 0, 0, 0, 195, 0, 20, 0, 0, 0, 0, 0], 
	[ 78, 195, 0, 0, 40, 0, 40, 0, 40, 20, 78, 40, 40, 195, 0, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[ 0, 0, 0, 0, 0, 0, 39, 0, 0, 39, 0, 0, 0, 39, 0, 0, 0, 0, 0, 0, 0, 78, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 195, 78, 39, 195, 0, 0, 0, 0, 0, 0, 0, 0, 78, 78, 0, 0, 0, 0, 0, 0, 0, 78, 0, 0, 0, 39, 0, 0, 0, 78, 0], 
	[ 40, 78, 0, 0, 78, 0, 20, 0, 0, 20, 100, 78, 78, 78, 0, 0, 78, 0, 0, 78, 78, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[ 0, 0, 0, 0, 39, 0, 78, 78, 0, 195, 0, 78, 0, 0, 0, 0, 78, 0, 0, 0, 0, 78, 0, 0, 0, 0, 0, 78, 0, 0, 0, 0, 0], 
	[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 0, 195, 0, 0, 0, 0, 40, 0, 0, 40, 0, 0, 0, 78, 78, 0, 78, 20], 
	[ 40, 195, 0, 0, 39, 0, 0, 39, 39, 0, 195, 39, 39, 0, 0, 0, 0, 0, 0, 78, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[ 0, 0, 0, 78, 78, 78, 0, 0, 0, 78, 0, 40, 0, 0, 40, 78, 0, 0, 0, 0, 40, 0, 0, 40, 20, 0, 0, 0, 0, 0, 20, 0, 20], 
	[ 0, 0, 78, 78, 20, 78, 0, 0, 0, 78, 0, 0, 0, 0, 195, 78, 78, 0, 0, 0, 0, 0, 0, 78, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[ 0, 39, 0, 0, 0, 0, 0, 0, 0, 0, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 0, 0, 0, 40, 40, 0, 0, 78, 78, 40, 78, 0, 0, 40, 40, 0, 0, 0, 195, 0, 0, 0, 78, 0, 0, 0, 0, 0, 0, 195, 0, 0], 
	[195, 78, 0, 0, 78, 0, 0, 20, 0, 0, 78, 0, 78, 0, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[ 195, 0, 0, 0, 78, 0, 0, 0, 0, 0, 0, 78, 195, 0, 0, 0, 40, 0, 195, 0, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0], 
	[40, 0, 0, 0, 78, 0, 0, 195, 78, 0, 0, 78, 40, 0, 0, 0, 78, 195, 195, 78, 40, 0, 195, 0, 0, 0, 195, 195, 0, 0, 0, 0, 0], 
	[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 0, 0, 0, 0, 195, 0, 0, 20], 
	[ 40, 0, 0, 0, 78, 0, 78, 0, 0, 78, 0, 20, 78, 78, 0, 0, 195, 0, 0, 0, 78, 78, 0, 0, 40, 40, 0, 0, 0, 0, 0, 0, 0]
]

CSC_matrix = [ 
    [ 78, 20, 20, 20, 20, 20, 20, 0, 0, 0, 0, 20, 78, 0, 20, 0, 0, 0, 0, 0, 0, 40, 0, 0], 
	[78, 20, 20, 20, 20, 0, 0, 0, 78, 20, 0, 20, 195, 0, 0, 0, 0, 0, 0, 0, 0, 195, 195, 0], 
	[ 40, 40, 0, 0, 0, 0, 195, 0, 0, 0, 78, 0, 0, 0, 0, 0, 0, 78, 0, 0, 0, 0, 0, 0], 
	[ 195, 40, 40, 40, 40, 0, 0, 0, 195, 0, 78, 0, 0, 0, 0, 0, 0, 78, 0, 0, 0, 0, 0, 0], 
	[ 78, 20, 195, 20, 195, 20, 0, 20, 40, 78, 0, 78, 0, 39, 0, 0, 0, 0, 0, 0, 78, 0, 0, 0], 
	[ 78, 78, 40, 20, 78, 0, 20, 20, 78, 40, 0, 20, 78, 20, 0, 20, 0, 0, 40, 40, 40, 195, 40, 40], 
	[ 0, 78, 0, 78, 0, 0, 78, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[ 78, 195, 0, 0, 20, 0, 20, 0, 78, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[ 78, 0, 0, 0, 78, 78, 0, 0, 20, 0, 40, 0, 20, 195, 195, 20, 20, 40, 195, 0, 40, 0, 20, 20], 
	[ 40, 40, 20, 40, 0, 0, 0, 0, 40, 195, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[ 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[ 40, 78, 40, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 195, 0, 0, 0, 0, 0, 0, 0], 
	[40, 20, 40, 20, 0, 0, 0, 20, 78, 20, 195, 195, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0], 
	[20, 0, 0, 0, 40, 40, 0, 0, 20, 0, 0, 40, 0, 40, 195, 195, 0, 0, 78, 0, 195, 0, 0, 0], 
	[ 78, 20, 20, 20, 20, 0, 0, 0, 78, 20, 0, 20, 195, 0, 0, 0, 0, 0, 0, 0, 0, 195, 195, 0], 
	[20, 20, 0, 20, 20, 195, 0, 0, 20, 0, 0, 20, 195, 20, 0, 0, 0, 40, 20, 0, 40, 40, 195, 0], 
	[ 20, 40, 0, 40, 0, 0, 195, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[ 195, 195, 195, 195, 195, 40, 40, 40, 78, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[ 20, 20, 0, 0, 40, 20, 0, 0, 20, 0, 0, 0, 195, 40, 0, 0, 0, 0, 0, 0, 40, 195, 195, 0], 
	[ 20, 0, 0, 0, 0, 0, 0, 0, 20, 0, 0, 0, 195, 0, 0, 0, 0, 0, 0, 0, 0, 78, 0, 0], 
	[ 0, 20, 0, 78, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 195, 0, 0, 0, 40, 0, 0, 0], 
	[ 40, 195, 40, 195, 0, 0, 195, 0, 40, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 78, 0, 0, 0], 
	[ 20, 195, 0, 195, 78, 0, 20, 0, 78, 0, 40, 0, 0, 40, 0, 0, 0, 0, 40, 40, 20, 0, 0, 20], 
	[ 195, 78, 195, 20, 40, 0, 0, 195, 78, 40, 40, 0, 0, 0, 40, 0, 0, 0, 0, 0, 20, 0, 0, 0], 
	[ 20, 0, 195, 0, 0, 0, 0, 195, 78, 40, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	[0, 40, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0], 
	[ 0, 20, 0, 78, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 195, 0, 0, 0, 40, 0, 0, 0], 
	[0, 0, 0, 78, 0, 0, 195, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 195, 0, 0, 0], 
	[40, 40, 0, 40, 0, 0, 0, 0, 0, 0, 0, 195, 0, 0, 0, 0, 195, 0, 0, 0, 0, 0, 0, 0], 
	[ 0, 40, 0, 20, 0, 20, 0, 0, 40, 0, 20, 78, 0, 0, 0, 0, 40, 20, 0, 0, 0, 0, 0, 0], 
	[ 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 39, 0, 0, 78, 0, 0, 0, 39, 0, 0, 0, 0, 39, 0], 
	[ 195, 0, 195, 0, 195, 20, 0, 0, 78, 195, 0, 0, 0, 0, 0, 40, 0, 0, 0, 40, 40, 0, 0, 0], 
	[ 40, 78, 78, 40, 195, 20, 40, 0, 195, 78, 0, 39, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

np.set_printoptions(threshold=sys.maxsize, linewidth=400)

def random_search_preference(pref_matrix, teaching_credits = None, iterations = 1000, distribute_work = True, score_type = "min_bad_pref"):
    matrix = np.array(pref_matrix) #The original preference matrix as a numpy array.
    best_matrix = [] #Save best output matrix here.
    best_score = 0 #Score heuristic gets computed differently depending on score type.
    worst_score = 9999
    print("Given matrix:\n", matrix)
    n = 0
    total_thrown_out = 0 #Total invalid schedules discarded. In real scenarios this often ends up very high.
    have_enough_availability = True

    if teaching_credits is None:
        teaching_credits = np.ones(matrix.shape[0]) * 3
    
    have_enough_availability = np.sum(teaching_credits) >= matrix.shape[1]
    if have_enough_availability == False:
        print("Did not have enough availability!")

    while n < iterations:
        output_matrix = np.zeros(matrix.shape)
        bad_attempts = 0
        profs_cooldown = []
        profs_teach_at_least_one = False
        while bad_attempts < BAD_ATTEMPT_MAX and np.sum(np.sum(output_matrix, axis = 0)) < matrix.shape[1]:
            if len(profs_cooldown) > 0 and distribute_work:
                curr_prof = np.random.choice(np.setdiff1d(np.arange(matrix.shape[0]), np.asarray(profs_cooldown, dtype=int)))
            else:
                curr_prof = np.random.choice(matrix.shape[0])

            if np.sum(output_matrix[curr_prof]) < teaching_credits[curr_prof]:
                taken_courses = np.sum(output_matrix, axis = 0)

                free_courses = matrix[curr_prof] * np.logical_not(taken_courses).astype(int)
                if np.all(free_courses == 0):
                    #When we arrive at this case, it's because we managed to select a prof that can't be assigned to any course.
                    #We increment bad attempts. If we keep doing this without assigning anyone, its probably an invalid schedule, so we throw it away.
                    bad_attempts += 1
                    continue
               
                selected = np.random.choice(np.flatnonzero(free_courses == np.max(free_courses)))
                #The flatnonzero part of this will get all max value occurences (ie. if a prof has 195 listed many times)
                assert(matrix[curr_prof][selected] >= 20)
                output_matrix[curr_prof][selected] = 1

                if profs_teach_at_least_one == False:
                    profs_cooldown.append(curr_prof)
                
                if len(profs_cooldown) == matrix.shape[0]:
                    profs_cooldown.clear()
                    profs_teach_at_least_one = True
                    #If we just placed the last prof on cooldown, then every prof has at least one course.


        n += 1
        if n % 100 == 0:
            print("Completed this many tries: ", n)
        
        if bad_attempts >= BAD_ATTEMPT_MAX and have_enough_availability:
            total_thrown_out += 1
            continue

        mula = (matrix * output_matrix).astype(int)
        a = np.sum(mula, axis = 0)
        #print("Making assertion on this: ", a)
        assert(np.count_nonzero(a > 0) == output_matrix.shape[1])

        score = 0
        if score_type == "sum":
            score = np.sum(output_matrix)
        elif score_type == "mean":
            score = np.mean(np.sum(output_matrix, axis=1))
        elif score_type == "min_bad_pref":
            mul = (matrix * output_matrix).astype(int)
            score = (mul > 39).sum()
            has_zero_row = (~output_matrix.any(axis=1)).any()
            if has_zero_row == False:
                score *= 100
        elif score_type == "no_bad_pref":
            mul = (matrix * output_matrix).astype(int)
            if (mul < 40).sum() == 0:
                score = 1
            else:
                score = 0
        else:
            score = np.sum(output_matrix)

        if score > best_score:
            best_score = score
            best_matrix = output_matrix
        if score < worst_score:
            worst_score = score

    print("Bad attempts: ", total_thrown_out)

    if isinstance(best_matrix, list):
        print("No valid schedule was found. Check your input!")
        print(output_matrix)
        return np.zeros(matrix.shape)

    print("Best Matrix was \n", best_matrix.astype(int))
    print("With best score of: ", best_score)
    print("Worst score seen was:", worst_score)
    print("Visualizing original preferences \n", (matrix * best_matrix).astype(int))
    

    return best_matrix

SLOTS_PER_DAY = 13

def random_search_schedule(courses: List[ScheduledClass], course_assignments):
    matrix = np.zeros((len(courses), 13 * 5))
    not_at_same_time = course_assignments
    courses_scheduled = 0
    while courses_scheduled < matrix.shape[0]:
        curr_course = np.random.choice(matrix.shape[0])
        


        

def main():
    mapping_dict = {0:0, 1:20, 2:39, 3:40, 4:78, 5:100, 6:195}
    teachers = 29
    courses = 50
    P = np.array([0,1,2,3,4,5,6])
    prefs = np.random.randint(0, P.size, (teachers, courses), dtype=np.int64)
    prefs = np.vectorize(mapping_dict.get)(prefs)


    prefs_bad = [
        [20, 40, 40],
        [0, 78, 20]
    ]

    relief_bad = [1, 2]
    
    hardcoded_relief = np.array([3, 3, 2, 2, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 2, 2, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3])
    random_search_preference(prefs_bad, relief_bad, distribute_work=True, iterations=10, score_type="min_bad_pref")
    return 0


if __name__ == '__main__':
    main()