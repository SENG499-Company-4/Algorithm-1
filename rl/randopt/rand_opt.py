import numpy as np
from matplotlib import pyplot as plt


class RandOpt:
    def __init__(self, shape, prefs, avails, max_iter, P, p_tgt):
        self.dtype = np.uint8
        self.shape = shape
        self.prefs = prefs
        self.avails = avails
        self.max_iter = max_iter
        self.P = P
        self.p_tgt = p_tgt
        self.tensor = np.zeros(shape=self.shape, dtype=self.dtype)
        self.reset()
        self.set_sufficient_reward()

    def reset(self, tensor=None):
        if tensor is None:
            tensor = self.tensor 
        
        tensor[:, :, :] = 0
        self.random_seed(tensor)

    def random_seed(self, tensor):
        card_c, card_ti, card_te = tensor.shape
        courses, times, teachers = tensor.nonzero()

        for course in range(card_c):
            time = np.random.randint(low=0, high=card_ti, size=1)
            ideal_tc_matches = np.where(self.prefs[:, course] > self.p_tgt)[0]
            teacher = np.random.choice(ideal_tc_matches, size=1)
            tensor[course, time, teacher] = 1

    def set_sufficient_reward(self):
        card_c = self.shape[0]
        self.sufficient_reward = card_c * np.tanh(self.p_tgt - np.median(self.P))

    def solve(self):
        reward, max_reward = 0, 0
        tmp_tensor = np.zeros(self.shape, dtype=self.dtype)

        for i in range(self.max_iter):
            if self.done(max_reward): 
                print(f"state:\n{self.sparse()}\nreward = {max_reward}\nsufficient reward = {self.sufficient_reward}")
                self.plot()
                break
            
            self.reset(tmp_tensor)
            reward = self.calc_reward(tmp_tensor)

            if reward > max_reward:
                max_reward = reward
                self.tensor[:, :, :] = tmp_tensor[:, :, :]

    def done(self, reward):
        if self.is_valid_schedule() or \
                reward >= self.sufficient_reward:
            return True
        return False

    def sparse(self):
        courses, times, teachers = self.tensor.nonzero()
        sparse_tensor = {(courses[i], times[i], teachers[i]) : self.prefs[teachers[i], courses[i]] \
                            for i in range(courses.size)}
        return sparse_tensor

    def plot(self, tensor=None):
        if tensor is None:
            tensor = self.tensor

        plt.rcParams["figure.figsize"] = [10.00, 5.00]
        plt.rcParams["figure.autolayout"] = True
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('$Courses$')
        ax.set_ylabel('$Times$')
        ax.set_zlabel('$Teachers$')
        courses, times, teachers = tensor.nonzero()
        ax.scatter(courses, times, teachers, c=courses, alpha=1)
        plt.show()

    def calc_reward(self, tensor=None):
        if tensor is None:
            tensor = self.tensor

        card_c = self.shape[0]
        courses, _, teachers = tensor.nonzero()
        tc_pairs = [(teachers[i], courses[i]) for i in range(card_c)]
        p_hat = np.array([self.prefs[tc_pair] for tc_pair in tc_pairs], dtype=self.dtype)

        R = np.sum(np.tanh(p_hat - np.median(self.P)), dtype=np.float32)

        return R
    
    def is_valid_schedule(self):
        state = self.tensor
        num_courses_per_teacher = np.count_nonzero(state, axis=1)
        num_teachers_per_course = np.count_nonzero(state, axis=0)
        return False
        
        if num_teachers_per_course[num_teachers_per_course < MIN_TEACHERS_PER_COURSE].size > 0:
            return False
        
        if num_teachers_per_course[num_teachers_per_course > MAX_TEACHERS_PER_COURSE].size > 0:
            return False

        if num_courses_per_teacher[num_courses_per_teacher > MAX_COURSES_PER_TEACHER].size > 0:
            return False
        
        return True
    

