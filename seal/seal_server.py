from path_oram import PathOramClient
from path_oram import PathOramServer
from adj_oram import adj_oram

class SEALServer:
    def __init__(self, padding_parameter, alpha, bit_size_of_key, data_set, tree_height, bucket_capacity, data_block_capacity):
        
        self.padding_parameter = padding_parameter
        self.memory_array = []
        self.element_start_indices_and_length = dict()
        self.alpha = alpha
        
        self.build_dataset(self.padding_parameter, data_set)
        self.turn_data_set_into_list()
        
            # def __init__(self, memory_array, tree_height, bucket_capacity, data_block_capacity, alpha, bit_size_of_key = 128):        
        self.adjustable_oram = adj_oram(self.memory_array, tree_height, bucket_capacity, data_block_capacity, self.alpha, bit_size_of_key) #     def __init__(self, security_parameter, memory_array, alpha):
        
    
        # def database_recovery_attack(self, x, plaintext_tuples, encrypted_tuples, table): # map plaintext values to tuples of encrypted database
    # we need a plaintext tuple list, an encrypted tuples list, and a table like table = {(key : query, value : encrypted tuple)}
    # plaintext tuple list - memory array - like ('BLACK', 30409157)
    # encrypted tuples list - encrypt everything in memory array
    # table - like {(black : , 00111101)}
    
    
    
    def debug_print_seal(self):
        # for element_list in self.M:
        #     for element in element_list:
        print("Memory array : ", self.memory_array)
        print("Element start indices : ", self.element_start_indices_and_length)
        self.adjustable_oram.debug_print_tree()

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

        # def database_recovery_attack(self, plaintext_tuples, encrypted_tuples, table): # map plaintext values to tuples of encrypted database


    
    def group_like_elements(self, D):
        M = []  # List to store groups
        if not D:
            return M  # Return empty if D is empty

        current_group = [D[0]]  # Start with the first element

        for i in range(1, len(D)):  # Iterate through D starting from index 1
            if D[i][1] == current_group[0][1]:  # Compare with the first element of current group
                current_group.append(D[i])  # Add to the current group
            else:
                M.append(current_group)  # Store the completed group
                current_group = [D[i]]  # Start a new group

        M.append(current_group)  # Append the last group

        return M
    
    def turn_data_set_into_list(self) :
        res = []
        index = 0
        
        for element in self.memory_array:

            if(isinstance(element, list)):
                start_index = index
                length_of_elements = 0
                
                for item in element:
                    res.append(item)
                    index += 1
                    length_of_elements += 1
                self.element_start_indices_and_length[element[0][1]] = (start_index, length_of_elements)
            else:
                index += 1
        self.memory_array = res


    def build_dataset(self, padding_parameter, D):
                # D : [(1, A), (2, B), (3, C), (4, A)], W : {A, B, C}, D dict : {A : [1, 4], B : [2], C : [3], dummy}, sorted D : [(A, 1), (A, 4), (B, 2), (C, 3)]
        # W = {str(word) for entry in D for word in entry}
        
        # 1) build M : 
        temp = []
        for i in range(len(D)):
            temp.append((D[i][1], D[i][0]))

        D_word_count = len(D)
        
        sorted_list_of_players = sorted(temp, key=lambda x: x[1])
        list_of_lists_of_teams = self.group_like_elements(sorted_list_of_players)

        self.memory_array = self.adj_padding(padding_parameter, list_of_lists_of_teams, D_word_count) # pass in 2 for x

    def search(self, query_keyword): # queried keyword w, client's secret state stC, encrypted index I
        # 1) retrieve index and length of keyword w
        result = self.adjustable_oram.adj_oram_access("R", int(query_keyword))
        return result
