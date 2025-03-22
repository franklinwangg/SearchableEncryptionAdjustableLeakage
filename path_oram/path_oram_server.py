import socket
import struct

import json
import ast
import random
    
import socket
import random

class Data:
    def __init__(self, value=None):
        """
        Represents an individual piece of data.
        :param value: The actual data being stored.
        """
        self.value = value  # Data value

class DataBlock:
    def __init__(self, block_id=-1, capacity=1, leaf_node=-1):
        """
        Represents a data block stored in a bucket.
        :param block_id: Unique identifier for the data block (-1 indicates a dummy block).
        :param capacity: Capacity of the block (how many data objects it can hold).
        :param leaf_node: The assigned leaf node for this block.
        """
        self.block_id = block_id  # -1 indicates a dummy block
        self.capacity = capacity
        self.leaf_node = leaf_node  # Assigned leaf position
        self.data = []  # List of Data objects

    def to_dict(self):
        """
        Convert DataBlock to a dictionary for JSON serialization.
        """
        return {
            "block_id": self.block_id,
            "capacity": self.capacity,
            "leaf_node": self.leaf_node,
            "data": [data.value for data in self.data]  # Convert Data objects to a simple list
        }

class Node:
    def __init__(self, bucket_id, bucket_capacity, data_block_capacity):
        """
        Represents a node in the Path ORAM tree, which contains a bucket of data blocks.
        :param bucket_id: Unique identifier for this node.
        :param bucket_capacity: Maximum number of data blocks this bucket can hold.
        :param data_block_capacity: Capacity of each individual data block.
        """
        self.bucket_id = bucket_id
        self.bucket_capacity = bucket_capacity  # Maximum number of data blocks per bucket
        self.data_block_capacity = data_block_capacity
        self.bucket = [DataBlock(capacity=data_block_capacity) for _ in range(bucket_capacity)]  # Fill with dummy blocks
        self.actual_buckets_count = 0
        
    def to_dict(self):
        """
        Convert Node to a dictionary for JSON serialization.
        """
        return {
            "bucket_id": self.bucket_id,
            "bucket_capacity": self.bucket_capacity,
            "data_block_capacity": self.data_block_capacity,
            "bucket": [data_block.to_dict() for data_block in self.bucket],
            "actual_buckets_count": self.actual_buckets_count
        }

class Tree:
    def __init__(self, height, bucket_capacity, data_block_capacity):
        """
        Represents the Path ORAM tree structure.
        :param height: The height of the tree (logarithmic depth).
        :param bucket_capacity: Number of blocks each bucket can hold.
        :param data_block_capacity: Capacity of each individual data block.
        """
        self.height = height
        self.bucket_capacity = bucket_capacity
        self.data_block_capacity = data_block_capacity
        self.nodes = []  # List to store nodes

        self._initialize_buckets()

    def _initialize_buckets(self):
        """
        Initializes the nodes in the tree with empty (dummy) data blocks.
        """
        num_nodes = (2 ** (self.height + 1)) - 1  # Total number of nodes in a complete binary tree
        for i in range(num_nodes):
            self.nodes.append(Node(i, self.bucket_capacity, self.data_block_capacity))

class PathOramServer:
    def __init__(self, tree_height, bucket_capacity, data_block_capacity):

        self.tree = Tree(tree_height, bucket_capacity, data_block_capacity)  # Initialize ORAM tree

    def debug_print_tree(self):
        """
        Prints the ORAM tree in a structured, visual format to represent hierarchy.
        """
        print("\n===== ORAM Tree Debugging Output =====\n")

        num_nodes = len(self.tree.nodes)
        level = 0
        index = 0
        next_level_size = 1  # Binary tree level starts with 1 node

        # Determine the maximum width for the top-level node to center the output
        max_width = 2 ** (num_nodes.bit_length())  # Maximum width for the tree's visualization

        while index < num_nodes:
            # Adjust spacing dynamically to maintain tree alignment
            base_spacing = 2 ** (num_nodes.bit_length() - level + 1)  # More space for higher levels
            inner_spacing = " " * base_spacing

            # For centering the root node and other nodes based on the max width
            line = " " * (max_width // (2 ** level) - 1)  # Dynamically adjust to center nodes

            # Print each node in the current level
            for _ in range(next_level_size):
                if index >= num_nodes:
                    break
                node = self.tree.nodes[index]

                # Format bucket contents
                bucket_content = []
                for data_block in node.bucket:
                    if data_block.block_id == -1:
                        bucket_content.append("db -1")
                    else:
                        block_str = f"db {data_block.block_id} ({','.join(str(d.value) for d in data_block.data)})"
                        bucket_content.append(block_str)

                bucket_str = " | ".join(bucket_content) if bucket_content else "empty"
                line += f"bucket{index}: {bucket_str}" + inner_spacing

                index += 1

            print(line)
            level += 1
            next_level_size *= 2  # Each level in a binary tree has 2^level nodes
            print()  # Newline for better separation between levels

        print("\n===== End of Debugging Output =====\n")

    def get_bucket(self, bucket_id):
        return_dict = self.tree.nodes[bucket_id].to_dict()  # Convert node to dictionary
        return return_dict
    def remove_bucket(self, bucket_id, block_id):

        for i in range(len(self.tree.nodes[bucket_id].bucket)):
            if(self.tree.nodes[bucket_id].bucket[i].block_id == block_id):
                self.tree.nodes[bucket_id].bucket.pop(i)
                break

        self.tree.nodes[bucket_id].bucket.append(DataBlock())
        # self.debug_print_tree()
    def write_bucket(self, bucket_id, data_block_list):
        # 1) kick out as many dummy blocks as we need
        temp = len(data_block_list)
        to_remove = []

        for i in range(len(self.tree.nodes[bucket_id].bucket)):
            if(len(to_remove) == temp):
                break
            if(self.tree.nodes[bucket_id].bucket[i].block_id == -1):
                to_remove.append(i)

        # for i in to_remove:
        #     self.tree.nodes[bucket_id].bucket.pop(i)
        for i in reversed(to_remove):  # Iterate from largest to smallest index
            self.tree.nodes[bucket_id].bucket.pop(i)

        # 2) create the datablock
        if(len(data_block_list) == 0):
            pass
        else:

            try:
                # what happens if there are two blocks?

                for i in range(len(data_block_list)):
                    new_data_block = DataBlock(data_block_list[i]['block_id'], data_block_list[i]['capacity'], data_block_list[i]['leaf_node'])

                    # 2.1) add each piece of data in the received datablock into new_data_block
                    data = data_block_list[i]['data']

                    if isinstance(data, list):
                        if(len(data) == 1):
                            data = data[0]
                            new_data_block.data.append(Data(data))
                        else:
                            for d in data:
                                new_data_block.data.append(Data(d))
                    else:                                
                        new_data_block.data.append(Data(data))

                    # 3) add the datablock to the bucket
                    self.tree.nodes[bucket_id].bucket.append(new_data_block)


            except Exception as e:
                print("Exception : ", e)