import socket
import pickle
import random
import time
import struct
import json

class Oblivious_AVL:
    

    def __init__(self, server):

        self.document_collection = set() # collection of documents with unique id’s 
        self.keyword_dictionary = dict() # stores sets of keywords “id(w)”, id’s of documents that contain w
        
#     The algorithm accesses a path from the root down to
#  leaves. By storing the position tag for the root, all po
# sitions can be recovered from the nodes fetched. This
#  eliminates the need to store a position map for all iden
# ti ers.
#  After the position tags are regenerated, the tag in ev
# ery nodes childrenPos must also be updated. So we
#  require that every node has only one parent, i.e., the
#  access pattern graph is a bounded-degree tree.

    def get_random_leaf_node(self):
        pass
    
    
# 1) index creation - break A into a set of ranges, and attribute unique keyword to every range
# 2) query - break query range into sub ranges, map them to keywords, and generate tokens for searching the SSE index
# 3) security - augment the leakage functions L1 and L2 of the underlying SSE scheme, in order to capture the extra leakage coming from keyword mapping and index structure
# 4) updates - for every batch, create a separate index using new keys. Periodically consolidate separate indices into a single one
# Can you achieve better complexity than O(r · log2 N), where N is the database size (number of tuples) and r is the size of the range, without storing the position map locally?
# Yes, BRC and URC are both log(R + r), where R is the size of the range and r is the size of the return result
