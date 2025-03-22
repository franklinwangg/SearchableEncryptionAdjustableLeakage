import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

from path_oram import PathOramClient  # Importing the Person class from person.py
from path_oram import PathOramServer  # Importing the Person class from person.py

class query_recovery_attacker :
    def __init__(self):
        pass
    
    def query_recovery_attack(self, seal_server):
        seal_server_odict = seal_server.element_start_indices_and_length
        CORRECT = 0

        for key in seal_server_odict.keys():
            size_of_return_query = len(seal_server.search(key))
            
            all_keywords_with_same_query_length = []
            
            for k, v in seal_server.element_start_indices_and_length.items():
                if(v[1] == size_of_return_query):
                    all_keywords_with_same_query_length.append(k)
            
            if(len(all_keywords_with_same_query_length) == 0):
                continue
            else:   
                random_element = random.choice(all_keywords_with_same_query_length)
                if(random_element == key):
                    CORRECT += 1
        return CORRECT / len(seal_server_odict.keys())
            
    def query_recovery_attack_path_oram(self, path_oram, list_of_keywords):
        # how it works : for each keyword in path oram, we query it and set x = (size of return query)
        # then we find all keywords that return queries of size x, and choose random one out of them
        
        # 1) create a list of all the keyword results first
        keyword_query_list = dict()
        for keyword in list_of_keywords:
            # print("keyword : ", keyword)
            temp = path_oram.access("R", str(keyword))
            # print("z. temp : ", temp)
            keyword_query_list[keyword] = temp
            
        print("keyword query list : ", keyword_query_list)

        CORRECT = 0
        for key1, val1 in keyword_query_list.items():
            if(val1 == None):
                continue
            res = []
            for key2, val2 in keyword_query_list.items():
                if(val2 != None and len(val1) == len(val2)):
                    if(key1 != key2):
                        res.append(key2)
            # print("1. res : ", res)
            if(len(res) == 0):
                continue
            else:
                if(random.choice(res) == key1): ###
                    CORRECT += 1
        
        return CORRECT / len(list_of_keywords)
    
    def database_recovery_attack(seal_server, decrypted_keyword, alpha): # map plaintext values to tuples of encrypted database
        
        matching_prefixes = []
        encrypted_keyword = decrypted_keyword.encrypt()
        for element in seal_server.memory_array:
            encrypted_element = element.encrypt()
            if(encrypted_element[alpha:] == encrypted_keyword[alpha:]):
                matching_prefixes.append(element)
        
        random_element = random.choice(matching_prefixes) # should it choose 2^alpha random elements? and see how many of these match the actual elements of the query
        if(random_element == decrypted_keyword):
            return True
        
        
        return False