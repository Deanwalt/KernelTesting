from concurrent.futures import ThreadPoolExecutor
import time
threshold = 2


def is_small_problem(problem):
    set1, set2 = problem
    return len(set1) <= threshold or len(set2) <= threshold

def solve_small_problem(problem):
    set1, set2 = problem
    time.sleep(1)
    return [(item1, item2) for item1 in set1 for item2 in set2]

def divide_problem(problem):
    set1, set2 = problem
    mid1 = len(set1) // 2
    mid2 = len(set2) // 2
    subproblems = [
        (set1[:mid1], set2[:mid2]),
        (set1[mid1:], set2[:mid2]),
        (set1[:mid1], set2[mid2:]),
        (set1[mid1:], set2[mid2:])
    ]
    return subproblems

def merge_results(results):
    return [item for sublist in results for item in sublist]

def divide_and_conquer_parallel(problem):
    if is_small_problem(problem):
        return solve_small_problem(problem)

    subproblems = divide_problem(problem)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(divide_and_conquer_parallel, subproblem) for subproblem in subproblems]
        results = [future.result() for future in futures]

    return merge_results(results)


set1 = [1, 2, 3, 4, 6, 7, 8, 9]
set2 = ['a', 'b', 'c', 5, 5, 6, 10]



t1 = time.time()
result = divide_and_conquer_parallel((set1, set2))
t2 = time.time()
#print(result)
print(t2-t1)

def normal(s1, s2):
    res = []
    for i in s1:
        for j in s2:
            time.sleep(1)
            res.append((i, j))
    return res

t1 = time.time()
re = normal(set1, set2)
t2 = time.time()
#print(re)
print(t2-t1)

