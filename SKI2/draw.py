from concurrent.futures import ThreadPoolExecutor #, ProcessPoolExecutor
#from concurrent.futures import 
import time
import struct
threshold = 3

def is_small_problem(problem):
    
    prob = problem[0]
    set1 = prob[0]
    set2 = prob[1]
    
    #l1, l2 = problem[6], problem[7]
    #print(l1, l2)
    return len(set1) <= threshold or len(set2) <= threshold

def solve_small_problem(problem):
    set1 = problem[0][0]
    set2 = problem[0][1]
    dict1 = problem[1]
    dict2 = problem[2]

    offset = problem[3]
    addr_and_byte = problem[4]
    recur = []
    
    channel_freq = problem[5]
    for i in set1:
        for j in set2:
            recur.append((i, j))
            write_value_dict = dict1[i]
            read_value_dict = dict2[j]
            for write_value in write_value_dict:
                write_bytes_value = struct.pack('<I', write_value)
                write_actual_value = write_bytes_value[offset[0]: offset[1]] #[: write_end_offset]
                for read_value in read_value_dict:
                    read_bytes_value = struct.pack('<I', read_value)
                    read_actual_value = read_bytes_value[offset[2]: offset[3]] #[read_begin_offset: read_end_offset]
                    if(read_actual_value != write_actual_value):
                        write_candidate_list = write_value_dict[write_value]
                        read_candidate_list = read_value_dict[read_value]
                        if(read_candidate_list[0][0] != 0):
                            freq = write_candidate_list[0] * read_candidate_list[0][0]
                            if(freq != 0):
                                if(write_value == 0):
                                    channel = tuple([i, addr_and_byte[0], addr_and_byte[1], j, addr_and_byte[2], addr_and_byte[3], 0, 0])
                                else:
                                    channel = tuple([i, addr_and_byte[0], addr_and_byte[1], j, addr_and_byte[2], addr_and_byte[3], 0, 1])
                                if(channel not in channel_freq):
                                    channel_freq[channel] = 0
                                channel_freq[channel] += freq
                                #num_new_pmc += 1
                                #num_pmc += 1
                        if(read_candidate_list[1][0] != 0):
                            freq = write_candidate_list[0] * read_candidate_list[1][0]
                            if(freq != 0):
                                if(write_value == 0):
                                    channel = tuple([i, addr_and_byte[0], addr_and_byte[1], j, addr_and_byte[2], addr_and_byte[3], 1, 0])
                                else:
                                    channel = tuple([i, addr_and_byte[0], addr_and_byte[1], j, addr_and_byte[2], addr_and_byte[3], 1, 1])
                                if(channel not in channel_freq):
                                    channel_freq[channel] = 0
                                channel_freq[channel] += freq
                                #num_new_pmc += 1
                                #num_pmc += 1
    #return [(item1, item2) for item1 in set1 for item2 in set2]
    #recur = [(item1, item2) for item1 in set1 for item2 in set2]
    ret = (recur, dict1, dict2, offset, addr_and_byte, channel_freq)
    return ret

def divide_problem(problem):
    #set1, set2 = problem
    prob = problem[0]
    set1, set2 = prob
    mid1 = len(set1) // 2
    mid2 = len(set2) // 2
    subproblems = [
        [(set1[:mid1], set2[:mid2]), problem[1], problem[2], problem[3], problem[4], problem[5]],
        [(set1[mid1:], set2[:mid2]), problem[1], problem[2], problem[3], problem[4], problem[5]],
        [(set1[:mid1], set2[mid2:]), problem[1], problem[2], problem[3], problem[4], problem[5]],
        [(set1[mid1:], set2[mid2:]), problem[1], problem[2], problem[3], problem[4], problem[5]]
    ]
    return subproblems

def merge_results(results):
    return [item for sublist in results for item in sublist]

def divide_and_conquer_parallel(problem):
    if is_small_problem(problem):
        return solve_small_problem(problem)

    subproblems = divide_problem(problem)

    
    executor = ThreadPoolExecutor(max_workers = 16)
    futures = []
    for subproblem in subproblems:
        futures.append(executor.submit(divide_and_conquer_parallel, subproblem))
    results = [future.result() for future in futures]
    '''
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(divide_and_conquer_parallel, subproblem) for subproblem in subproblems]
        results = [future.result() for future in futures]
    ''' 
    return results #merge_results(results)

