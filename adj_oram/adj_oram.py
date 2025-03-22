import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

from path_oram import PathOramClient  # Importing the Person class from person.py
from path_oram import PathOramServer  # Importing the Person class from person.py


class adj_oram :
    def __init__(self, memory_array, tree_height, bucket_capacity, data_block_capacity, alpha, bit_size_of_key = 128):
        self.bit_size_of_key = bit_size_of_key
        self.secret_key = self._generate_secret_key()

        self.alpha = alpha

        self.clients = []
        self.orams = []
        
        self.tree_height = tree_height
        self.bucket_capacity = bucket_capacity
        self.data_block_capacity = data_block_capacity
        
        self.data_block_count_in_tree = (2 ** (self.tree_height + 1) - 1) * self.bucket_capacity
        
        for i in range(2 ** self.alpha):
            temp_oram = PathOramServer(self.tree_height, self.bucket_capacity, self.data_block_capacity)     #def __init__(self, tree_height, bucket_capacity, data_block_capacity):
            temp_client = PathOramClient(temp_oram)

            self.orams.append(temp_oram)
            self.clients.append(temp_client)
            
        self._read_in_memory_array(memory_array)
        
    def _read_in_memory_array(self, memory_array):
        for element in memory_array:
            name = element[0]
            team_number = element[1]
            self.adj_oram_access("W", int(team_number), (name, team_number))

    def prp(self, index, max_range):

        cipher = AES.new(self.secret_key, AES.MODE_ECB)
        data = pad(index.to_bytes((index.bit_length() + 7) // 8, 'big'), AES.block_size)
        cipher_bytes = cipher.encrypt(data) # 128 bits, 16 bytes
                
        int_value = int.from_bytes(cipher_bytes, "big") # int value
        int_value_mod_maxrange = int_value % max_range

        binary_representation = bin(int_value_mod_maxrange)[2:].zfill(8) # byte value

        return binary_representation

    def prp_aes(self, index):
        cipher = AES.new(self.secret_key, AES.MODE_ECB)
        data = pad(index.to_bytes((index.bit_length() + 7) // 8, 'big'), AES.block_size)
        return cipher.encrypt(data) # 128 bits, 16 bytes

    
    def _generate_secret_key(self):
        
        key = bytearray(random.getrandbits(8) for _ in range(self.bit_size_of_key // 8))
        return bytes(key)

        
        
    #     self.clients[int_tree_index].access(op, int_block_index, (team_number, name)) # previously : both the tree AND datablock are determined by team number
    #     # now : tree is determined by team number, datablock is determined by name
        
    ### define some prp function "pi"
    def adj_oram_access(self, op, index, val = 0): 
                    # self.adj_oram_access("W", int(team_number), (name, team_number))
        # return self.adjustable_oram.adj_oram_access("R", int(query_keyword))

        prp_mapping = self.prp(index, len(self.orams))
        
        tree_string = prp_mapping[:self.alpha]
        data_block_string = prp_mapping[self.alpha:]
        
        tree_int = int(tree_string, 2)
        data_block_int = int(data_block_string, 2)
                
        tree_int += 1
        data_block_int += 1
        if(op == "R"):
            res = self.clients[tree_int].access(op, data_block_int, val) # given an index, maps the val=name to tree index and data block index using index
            read_res = []
            for name, team_number in res:
                if(int(team_number) == index):
                    read_res.append((name, team_number))
            return read_res
        else:
            self.clients[tree_int].access(op, data_block_int, val)
    
    def debug_print_tree(self):
        
        print("\n=== Debug ORAM Tree Structure ===")
        for i in range(len(self.orams)):
            print(f"\nORAM {i}:")
            self.orams[i].debug_print_tree()
            print(f"Stash {i}:", self.clients[i].stash)
            print(f"Position Map {i}:", self.clients[i].position_map)
            
            
