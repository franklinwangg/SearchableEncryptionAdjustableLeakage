from path_oram import PathOramClient
from path_oram import PathOramServer
from seal import SEALServer
from attacks import attacker

import pandas as pd
import sys
import os
import time

def split_string(input_string):
    parts = input_string.split()

    if len(parts) >= 3:
        return parts[0], parts[1], ' '.join(parts[2:])
    elif len(parts) == 2:
        return parts[0], parts[1] 
    else:
        return None 

if __name__ == "__main__":
    # 1) read in the data    
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    file_path = os.path.join(root_dir, 'crime.csv')
    print("file path : ", file_path)
    df = pd.read_csv('crime.csv', usecols=["CB_NO", "RACE"])
    df_subset = df.head(3000)
    
    # 2) some constant parameters for our tests
    security_parameter = 1    
    bit_size_of_key = 128    
    tree_height = 1
    bucket_capacity = 1
    data_block_capacity = 100
    data_set = []
    atk = attacker()

    
    for index, row in df_subset.iterrows():
        cb_no = row["CB_NO"]
        race = row["RACE"]
        data_set.append((cb_no, race))
        
    # 3) test for 3 different values of alpha
    alpha = 1
    
    padding_parameter = 0
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 1, padding = 0 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    
    padding_parameter = 1
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 1, padding = 1 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    padding_parameter = 2
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 1, padding = 2 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    padding_parameter = 3
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 1, padding = 3 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    padding_parameter = 4
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 1, padding = 4 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    padding_parameter = 5
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 1, padding = 5 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    alpha = 2
    padding_parameter = 0
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 2, padding = 0 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    
    padding_parameter = 1
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 2, padding = 1 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    padding_parameter = 2
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 2, padding = 2 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    padding_parameter = 3
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 2, padding = 3 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    padding_parameter = 4
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 2, padding = 4 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    padding_parameter = 5
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 2, padding = 5 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    alpha = 3
    padding_parameter = 0
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 3, padding = 0 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    
    padding_parameter = 1
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 3, padding = 1 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    padding_parameter = 2
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 3, padding = 2 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    padding_parameter = 3
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 3, padding = 3 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    padding_parameter = 4
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 3, padding = 4 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    padding_parameter = 5
    server = SEALServer(padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity)
    time1 = time.time()
    accuracy1 = atk.query_recovery_attack(server)
    time2 = time.time()
    print("Query Recovery Attack on SEAL with alpha = 3, padding = 5 : ")
    print("Time to execute : ", (time2 - time1))
    print("Accuracy : ", accuracy1)
    
    # print(atk.query_recovery_attack_path_oram(path_oram_client, list_of_keywords))