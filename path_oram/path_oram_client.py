import socket
import pickle
import random
import time
import struct
import json

class PathOramClient:
    def __init__(self, server):

        self.stash = []
        self.position_map = dict()
        self.server = server
        self.tree_height = server.tree.height
        self.bucket_capacity = server.tree.bucket_capacity
        
    def access(self, op, a, data=None):
        # self.server.debug_print_tree()
# (1) Remap block (Lines 1 to 2): Randomly remap the position of block a to a new random
#  position. Let x denote the block’s old position.
        read_res = None

        old_position = -1
        # print("0. a : ", a, ", type : ", type(a))
        # print("0. position map : ", self.position_map)
        # print("0. test str 1: ", ('1' in self.position_map))
        # print("0. test int 1: ", (1 in self.position_map))
        ####
        
        if(a in self.position_map):
            # print("0a.")
            old_position = self.position_map[a]
        else:        
            # print("0b.")
            self.position_map[a] = self.get_random_leaf_node()
            old_position = self.position_map[a]
        # print("1. old position : ", old_position)
        
#  (2) Read path (Lines 3 to 5): Read the path P(x) containing block a. If the client performs
#  Access on block a for the first time, it will not find block a inthetreeorstash,andshould
#  assume that the block has a default value of zero.

        for level in range(self.tree_height + 1):
            current_bucket = self.P(old_position, level)
            for data_block in current_bucket['bucket']:
                if(data_block['block_id'] == -1):
                    continue
                else:
                    self.stash.append(data_block)
                    self.server.remove_bucket(current_bucket['bucket_id'], data_block['block_id'])
                        # def remove_bucket(self, bucket_id, block_id):

        # print("2. stash : ", self.stash)
            
#  (3) Update block (Lines 6 to 9): If the access is a write, update the data of block a.
        if(op == "W"):
            # remove old block a from the stash
            old_block = None
            
            for i in range(len(self.stash)):
                if(self.stash[i]['block_id'] == a):
                    old_block = self.stash.pop(i)
                    break 

            # replace it with new one
            if(old_block == None):
                
                new_block_data = []
                new_block_data.append(data)
                new_block = {
                    "block_id": a, 
                    "capacity": 100,  # Assuming capacity is always 100
                    "leaf_node": self.position_map[a], 
                    "data": new_block_data
                }
                self.stash.append(new_block)

            else:
                old_block['leaf_node'] = self.position_map[a]
                old_block['data'].append(data)
                self.stash.append(old_block)
                
                
        else:
            for i in range(len(self.stash)):
                # print("3. reading through stash : ", self.stash[i])
                # print("3.1  block id : ", self.stash[i]['block_id'], ", type : ", type(self.stash[i]['block_id']))
                # print("3.2 a : ", a, ", type : ", type(a))
                
                if(self.stash[i]['block_id'] == a):
                    read_res = self.stash[i]
                    # print("4. found : ", read_res)
                    break

#  (4) Write path (Lines 10 to 15): Write the path back and possibly include some additional
#  blocks from the stash if they can be placed into the path. Buckets are greedily filled with
#  blocks in the stash in the order of leaf to root, ensuring that blocks get pushed as deep
#  downinto the tree as possible. A block amapped to leafx can be placed in the bucket at
#  level only if the path P(x ) intersects the path accessed P(x) at level , in other words,
#  if P(x, ) = P(x , ).
        for level in range(self.tree_height + 1, -1, -1):
            current_bucket_on_old_path = self.P(old_position, level) # old position is still -1
            subtract_stash = []
            # gather all elements that belong to this bucket
            for i in range(len(self.stash)):
                stash_element_leaf = self.stash[i]['leaf_node']
                if(self.P(stash_element_leaf, level) == current_bucket_on_old_path):
                    subtract_stash.append(self.stash[i])
                
            min_blocks = min(len(self.stash), self.bucket_capacity - current_bucket_on_old_path['actual_buckets_count'])

            min_stash_blocks = self.stash[len(self.stash) - min_blocks:]
            self.stash = [block for block in self.stash if block not in min_stash_blocks]

            index_of_current_bucket = self._get_node_at_level(old_position, level, self.tree_height)
            self.server.write_bucket(index_of_current_bucket, min_stash_blocks)
        # print("done")

        if(op == "R"):
            # print("5. read res : ", read_res)
            if(read_res == None):
                # print("6. returning none")
                return None
            # print("7. returning data : ", read_res['data'])
            return read_res['data']

    
    def P(self, leaf_node, level):  # returns the bucket at this level on the path to this leaf_node
        
        x = self._get_node_at_level(leaf_node,level,self.tree_height)
        
        bucket_at_x = self.server.get_bucket(x)
        return bucket_at_x
    
    def _get_node_at_level(self,leaf_index, target_level, tree_height): # returns index(int)
        current_index = leaf_index
        current_level = tree_height 
        while current_level > target_level:
            if current_index == 0:
                break
            current_index = (current_index - 1) // 2 
            current_level -= 1 

        return current_index 
    
    def get_random_leaf_node(self):
        leaf_start = 2 ** (self.tree_height + 1) - 2 ** self.tree_height - 1
        leaf_end = 2 ** (self.tree_height + 1) - 1
        
        random_leaf_node = random.randint(leaf_start, leaf_end - 1)
        
        return random_leaf_node