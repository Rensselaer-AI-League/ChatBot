#The markov chain node class, it stores a list of words leading up to this point
#and the possibilities after this point
class MarkovNode:
    #The chain of words leading up to this node
    previous_words = None
    #A dictionary of the possible words after this node, and thier frequency
    next_words = None
    #The depth of the node
    depth = 0
    #Nodes are created by knowing the chain up to this point
    def __init__(self,previous_words):
        self.previous_words = previous_words
        self.depth = len(self.previous_words)
        self.next_words = {}
    #Returns the depth of the current node
    def depth(self):
        return self.depth
    #Syntactic Sugar Operations
    def __contains__(self,key):
        return key in self.next_words.keys()
    #Add a possibility to this node, with syntactic sugar
    def __setitem__(self,key,value):
        self.next_words[key] = value
    #Get the possibilities from this node
    def __getitem__(self,key):
        return self.next_words[key]
        
class MarkovChain:
    #A dictionary that stores lists of words to thier Markov Node representation
    node_dict = None
    #Initialize a new Markov Chain
    def __init__(self):
        self.node_dict = {}
    #Store this chain in a file
    def store(self,filename):
        import pickle
        #Open the store file
        dumpfile = open(filename,"w")
        #Dump this object
        pickle.dump(self,dumpfile)
    #Retrieve this object from a file
    def load(self,filename,**kwargs):
        import pickle
        #Flags
        merge_flag = False
        if "merge" in kwargs.keys():
            merge_flag = kwargs["merge"]
        #Open the load file
        loadfile = open(filename,"r")
        load_obj = pickle.load(loadfile)
        #Load each item in the file into this object
        for node in load_obj.node_dict.keys():
            if merge_flag:
                try:
                    print "Not implememneted"
                    continue
                except KeyError: pass
            self.node_dict[node] = load_obj.node_dict[node]
    #A dispatcher for differnet training sets
    def train(self,**kwargs):
        if "file" in kwargs.keys():
            self.file_train(**kwargs)
        if "sentence" in kwargs.keys():
            self.sentence_train(**kwargs)
    #Train the Markov Chain on the given sentence
    def sentence_train(self,sentence):
        for index in range(0,len(sentence)):
            #The chain leading up to this word and this word
            target = sentence[index]
            chain = tuple(sentence[:index])
            #Update the values of the current markov node if it is already there
            if chain in self.node_dict.keys():
                if target in self.node_dict[chain]:
                    self.node_dict[chain][target] += 1
                else:
                    self.node_dict[chain][target] = 1
            #Create the markov node if it is not there
            else:
                self.node_dict[chain] = MarkovNode(chain)
                self.node_dict[chain][target] = 1
    #Train the Markov Chain on the given file
    def file_train(self,file = "",lines = -1):
        #The current sentence being read
        current_sentence = []
        #A breaker term to break the loop, FOR DEV
        line_counter = 0
        for line in file:
            word_list = line.strip().split()
            #Empty word lists should be skipped
            if len(word_list) == 0: continue
            #Train on sentences in the word list
            word_list_index = 0
            previous_mark_index = 0
            while True:
                #print word_list[word_list_index]
                for mark in [".","!","?"]:
                    if mark in word_list[word_list_index]:
                        current_sentence += word_list[previous_mark_index:word_list_index+1]
                        self.train(sentence = current_sentence)
                        current_sentence = []
                        previous_mark_index = word_list_index+1
                word_list_index += 1
                if word_list_index >= len(word_list): break
            line_counter += 1
            if line_counter > lines: break
        
        
def make_shakespear_chain(lines = 300):
    #The source filename is called shakespeare.txt
    source_filename = "shakespeare.txt"
    #The dump file is called dump_shakespear.pickle
    dump_filename = "dump_shakespear.pickle"
    #Attempt to pickle load the dump file
    try:
        print "Attempting to load from dump..."
        loadfile = open(dump_filename,"r")
        return_chain = MarkovChain()
        return_chain.load(dump_filename)
        return return_chain
    #If that does not work, make a chain from shakespeare
    except IOError:
        print "Load failed."
        print "Training on shakespeare...."
        shakespear = open("shakespeare.txt","r")
        chain = MarkovChain()
        chain.train(file = shakespear,lines = lines)
        return chain

if __name__ == "__main__":
    #Make a markov chain that is trained to speak like shakespear
    chain = make_shakespear_chain(lines = 300)
    print len(chain.node_dict.keys())
    