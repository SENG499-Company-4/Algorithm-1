import numpy as np
import sys

NUM_TRIES = 1000
COURSE_PER_PROF = 3
DECAY_RATE = 3
BAD_ATTEMPT_MAX = 29

hardcoded_matrix = [
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

np.set_printoptions(threshold=sys.maxsize, linewidth=400)

def random_search(pref_matrix, previous_scores = []):
    matrix = np.array(pref_matrix)
    best_matrix = []
    best_score = 0
    worst_score = 9999
    print("Given matrix:\n", matrix)
    n = 0
    total_thrown_out = 0
    while n < NUM_TRIES:
        output_matrix = np.zeros(matrix.shape)
        score = 0
        bad_attempts = 0
        while bad_attempts < BAD_ATTEMPT_MAX and np.sum(np.sum(output_matrix, axis = 0)) < matrix.shape[1]:
            curr_prof = np.random.choice(matrix.shape[0])
            #print("Selected prof: ", curr_prof)
            if np.sum(output_matrix[curr_prof]) < COURSE_PER_PROF:
                taken_courses = np.sum(output_matrix, axis = 0)
                #print("Taken courses ", taken_courses)
                free_courses = matrix[curr_prof] * np.logical_not(taken_courses).astype(int)
                if np.all(free_courses == 0):
                    bad_attempts += 1
                    continue
                #print("Free courses: ", free_courses)
                #print("Argmax will be: ", np.flatnonzero(free_courses == np.max(free_courses)))
                selected = np.random.choice(np.flatnonzero(free_courses == np.max(free_courses)))
                #print("Selected index: ", selected)
                output_matrix[curr_prof][selected] = 1
                score += matrix[curr_prof][selected]
                #print("\n")

        n += 1
        if bad_attempts < BAD_ATTEMPT_MAX:
            assert(np.all(np.sum(output_matrix, axis = 0) == 1) == True)
        else:
            total_thrown_out += 1
        '''
        print()
        print("Results of attempt ",  n)
        print(score)
        print(output_matrix)
        print(np.sum(output_matrix, axis = 0))
        '''
        

        if score > best_score:
            best_score = score
            best_matrix = output_matrix
        if score < worst_score:
            worst_score = score

        if n % 10 == 0:
            print("Completed this many tries: ", n)
    
    print("Best Matrix was \n", best_matrix.astype(int))
    print("With best score of: ", best_score)
    print("Worst score seen was:", worst_score)
    print("Visualizing original preferences \n", (matrix * output_matrix).astype(int))
    print("Bad attempts: ", total_thrown_out)

        

def main():
    mapping_dict = {0:0, 1:20, 2:39, 3:40, 4:78, 5:100, 6:195}
    teachers = 29
    courses = 50
    P = np.array([0,1,2,3,4,5,6])
    prefs = np.random.randint(0, P.size, (teachers, courses), dtype=np.int64)
    prefs = np.vectorize(mapping_dict.get)(prefs)
    
    
    random_search(hardcoded_matrix)
    return 0


if __name__ == '__main__':
    main()