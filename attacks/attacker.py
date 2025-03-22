import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

from path_oram import PathOramClient  # Importing the Person class from person.py
from path_oram import PathOramServer  # Importing the Person class from person.py

class attacker :
    def __init__(self):
        pass
    
    
# Briefly, the attacker knows the database in plaintext. 
# Thus, the adversary knows the sizes of each keyword list 
# (number of documents associated with a keyword). When the 
# client issues a query and the adversary sees that 4 
# documents/entries/tuples are returned, then he chooses 
# one keyword with the same size at random, if the keyword
#  was the correct one we increase the counter, if not we 
# move to the next keyword. You do this for all keywords.

# 0) params : seal_server(or path oram server)
# 1) client issues query, receives 4 elements back
# 2) attacker goes through entire seal_server odict, and retrieves all elements that have size 4. choose one at random

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
            
            

# I don't understand what you are trying to say in your second paragraph. 
# How is an attack tailored for SEAL but not for Path ORAM? 
# SEAL uses a Path ORAM as a black box.

#  Our query recovery attack (see Figure 7) is very simple
#  and uses only volume pattern leakage. Having access to the
#  plaintext table T , the adversary computes the new padded
#  table for the queried attribute (Line 1 in Figure 7) using the
#  padding parameter x. Now, for a given encrypted query q with
#  size q the adversary uses T to find the candidate plaintext
#  values which have size q,andchooses one ofthem atrandom
#  (see Line 4 in Figure 7). Note that the higher the value of x
#  is, the larger the set of possible values in Line 4 is therefore
#  reducing the success rate of the attack.



# 0) encrypted query q with size q - goal : decrypt client's encrypted queries
# 1) use padding parameter x, and knowing the element_start_and_end_indices, adversary computes size of new padded table
# 2) 
# 3) 
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

                    
                    
        
#     DatabaseRecoveryAttack(T, enc(T), {t_q, S_q} q 
# belongs to Q)
# input: plaintext tuples T, encrypted tuples enc(T) 
# and tokens t_q along with respective set S_q of 
# encrypted tuples(and their alpha bit identifiers)
# output : the success rate DR_SR of the attack 

# 1) set T <- adj-padding(x, T)
# 2) set CORRECT = 0
# 3) for each pair (t_q, S_q) do
#     choose q' at random from the set {q': |T(q')| = 
# |S_q|}
#     for each encrypted tuple e belongs to S_q do
#         let id be the alpha bit identifier of e
#         choose at random a tuple t from enc(T) that 
# has id as the first alpha bits of its identifier 
#         remove t from enc(T)
#         if encrypted tuple t has value q' at the 
# queried attribute then CORRECT ++
#     remove q' from T 
# return CORRECT/sum of all |S_q|


# input: plaintext tuples T, encrypted tuples enc(T) 
# and tokens t_q along with respective set S_q of 
# encrypted tuples(and their alpha bit identifiers)
# output : the success rate DR_SR of the attack 
    


# database recovery attack - 1) adversary decrypts 
# some keyword and tries to map this decrypted keyword
# to the correct encrypted tuples. 2) the adversary 
# can see the first alpha bits of each returned 
# encrypted tuple, and chooses a random tuple
# out of the tuples that have the same first alpha 
# bits as the decrypted keyword. 3) attacker removes
# the chosen tuples t from list of encrypted tuples
# 4) if at the end of the process, the encrypted 
# tuple contains original keyword, they are 
# successful
    def database_recovery_attack(seal_server, decrypted_keyword, alpha): # map plaintext values to tuples of encrypted database
        
        # 1) input an ENCRYPTED keyword
        # 2) adversary decrypts it, call the decrypted result "q". goal : map q to correct encrypted tuples in 
        # the encrypted database in SEAL - in this case, your adj oram?
        # 3) adversary iterates through entire plaintext table, adding any elements whose encryptions start with the same "alpha" 
        # characters as the encrypted keyword
        # 4) adversary maps ONE random result from this to the tuple
        # 5) if the random result has q' at end of queried attribute, attacker is successful
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

    

# The database recovery (see Figure 8) works as follows.
#  First the adversary decrypts which keyword we are querying,
#  as before—say this keyword is q. 
# Now, the goal is to map
#  the value q to the correct encrypted tuples in enc(T ), where
#  enc(T ) is the encrypted database produced by the SETUP
#  algorithm of SEAL. The adversary knowing from L2 leakage
#  the alpha bits of each returned encrypted tuple, chooses at random
#  for each of them one tuple from enc(T ) with same bits as
#  prefix andmapsq tothistuple. 
# Finally,the adversary removes
#  the chosen tuples t from enc(T ). The adversary is successful
#  if after this process the encrypted tuple t has value q at the
#  queried attribute. Clearly, the smaller is, the more bits the
#  adversary will have to guess (the larger the set of tuples with
#  same bits as prefix is) and therefore the less successful the
#  attack is going to be.
