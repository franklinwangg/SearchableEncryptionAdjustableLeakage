# ODS
# Node (id, data)
# ODS Client
# Same as Path ORAM
# Stash list
# Access method - 
# Op = Read (id), Write(id, data), Insert(id, data), Del(id)


class ODS_Client : 
    def __init__(self):
        self.cache = []
    def start(self):
        # update cache to contain rootPos
        pass
    def Access(self, op, id, data):
        if(op == "I"):
            self.insert(id, data, None, None)
        elif(op == "R"):
            temp = None
            for i in range(len(self.cache)):
                if(self.cache[i][0] == id):
                    temp = self.cache[i]
            if(temp == None):
                # pos = get pos from cache using childrenPos entries
                (data_id, data_data, data_pos, data_childrenPos) = self.read_and_remove(id, pos)
                self.cache.insert((data_id, data_data, data_pos, data_childrenPos))
            if(temp != None):
                return temp[1]
            return None
        elif(op == "W"):
            temp = None
            for i in range(len(self.cache)):
                if(self.cache[i][0] == id):
                    temp = self.cache[i]
            if(temp != None):
                temp[1] = data
            else:
                # pos = get pos from cache using childrenPos entries
                (data_id, data_data, data_pos, data_childrenPos) = self.read_and_remove(id, pos)
                self.cache.insert((data_id, data_data, data_pos, data_childrenPos))
        elif(op == "D"):
            temp = None
            for i in range(len(self.cache)):
                if(self.cache[i][0] == id):
                    temp = self.cache[i]
            if(temp != None):
                self.cache.remove(temp)
            else:
                # pos = get pos from cache using childrenPos entries
                self.read_and_remove(id, pos)            
        else:
            pass
    def finalize(self, root_id, pad_val):
        for element in self.cache:
            element[2] = self.generate_uniform_random() # what is uniformRandom
            root_pos = root_id
            # pad read_and_remove() to pad_val
            while(len(self.cache) > 0):
                (data_id, data_data, data_pos, data_childrenPos) = self.cache.delete_next_element() # what is delete next element
                self.add((data_id, data_data, data_pos, data_childrenPos))
            # pad Add() to pad_val
        
        
#  ReadAndRemove(idpos): fetches and removes from server a block identi ed by id. pos is the position tag
#  of the block, indicating a set of physical addresses where the block might be.
#  Add(idposdata): writes a block denoted data, identi ed by id, to some location among a set of locations
#  indicated by pos.