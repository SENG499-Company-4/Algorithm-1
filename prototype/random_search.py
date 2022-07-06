import numpy as np
import sys

NUM_TRIES = 1000
COURSE_PER_PROF = 3
DECAY_RATE = 3

np.set_printoptions(threshold=sys.maxsize, linewidth=200)

def random_search(pref_matrix, previous_scores = []):
    matrix = np.array(pref_matrix)
    best_matrix = []
    best_score = 0
    worst_score = 9999
    print("Given matrix:\n", matrix)
    n = 0
    while n < NUM_TRIES:
        output_matrix = np.zeros(matrix.shape)
        score = 0

        while np.sum(np.sum(output_matrix, axis = 0)) < matrix.shape[1]:
            curr_prof = np.random.choice(matrix.shape[0])
            #print("Selected prof: ", curr_prof)
            if np.sum(output_matrix[curr_prof]) < COURSE_PER_PROF:
                taken_courses = np.sum(output_matrix, axis = 0)
                #print("Taken courses ", taken_courses)
                free_courses = matrix[curr_prof] * np.logical_not(taken_courses).astype(int)
                if np.all(free_courses == 0):
                    continue
                #print("Free courses: ", free_courses)
                #print("Argmax will be: ", np.flatnonzero(free_courses == np.max(free_courses)))
                selected = np.random.choice(np.flatnonzero(free_courses == np.max(free_courses)))
                #print("Selected index: ", selected)
                output_matrix[curr_prof][selected] = 1
                score += matrix[curr_prof][selected]
                #print("\n")

        n += 1
        
        print()
        print("Results of attempt ",  n)
        print(score)
        print(output_matrix)
        print(np.sum(output_matrix, axis = 0))
        assert(np.all(np.sum(output_matrix, axis = 0) == 1) == True)

        if score > best_score:
            best_score = score
            best_matrix = output_matrix
        if score < worst_score:
            worst_score = score
    
    print("Best Matrix was \n", best_matrix)
    print("With best score of: ", best_score)
    print("Worst score seen was:", worst_score)
    print("Visualizing original preferences \n", matrix * output_matrix)

        

def main():
    teachers = 29
    courses = 50
    P = np.array([0,1,2,3,4,5,6])
    prefs = np.random.randint(0, P.size, (teachers, courses), dtype=np.int64)
    random_search(prefs)
    return 0


if __name__ == '__main__':
    main()