import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
from collections import defaultdict

class query_recovery_attacker :
    def __init__(self):
        pass
    
    def encrypt_to_binary(self, plaintext, seal_server):
        cipher = AES.new(seal_server.adjustable_oram.secret_key, AES.MODE_ECB)
        padded_text = plaintext.ljust(16)
        ciphertext = cipher.encrypt(padded_text.encode())

        binary_cipher = ''.join(format(byte, '08b') for byte in ciphertext)
        return binary_cipher
    
    def create_token_to_encrypted_tuple_table(self, seal_server):
        res = defaultdict(list)
        for first, second in seal_server.memory_array():
            res[first].append(self.encrypt_to_binary(second, seal_server)) # should we encrypt race or id? (race, id)
        return res
    
    # make encrypted tuples
    


    def database_recovery_attack(self, x, plaintext_tuples, encrypted_tuples, table): # map plaintext values to tuples of encrypted database
        padded_plaintext_tuples = self.adj_padding(x, plaintext_tuples)
        CORRECT = 0
        for query, enc_tuple in table:
            same_length_plaintext_tuples = self.find_set_of_same_length() # find set of plaintext tuples such that length matches length of enc tuple
            random_same_length_tuple = random.choice(same_length_plaintext_tuples)
            for encrypted_tuple in table.values():
                id = encrypted_tuple.first_alpha_bits
                same_id_start_tuples = self.find_set_of_same_start_id(encrypted_tuples, id)
                random_same_id_start_tuple = random.choice(same_id_start_tuples)
                encrypted_tuple.remove(random_same_id_start_tuple)
                if(encrypted_tuple.plaintext() == random_same_length_tuple):
                    CORRECT += 1
            table.remove(random_same_length_tuple)
        return CORRECT / len(table)
    def find_set_of_same_length(self):
        pass
    
    def adj_padding(self, padding_parameter, list_of_lists_of_teams, D_word_count):
        res = []
        for list_of_team in list_of_lists_of_teams:
            team_number = list_of_team[0][1]
            min_i = 0
            for i in range(len(list_of_team)):
                if(len(list_of_team) <= padding_parameter ** i):
                    min_i = i
                    break
            for i in range(len(list_of_team), padding_parameter ** min_i):

                list_of_team.append(("dummy", team_number))

            res.append(list_of_team)

        while(len(res) < D_word_count * padding_parameter):
            res.append("dummy")
        return res