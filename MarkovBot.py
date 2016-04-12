import MarkovChain
import random

if __name__ == "__main__":
    #Make a chain from shakespeare texts
    chain = MarkovChain.make_shakespear_chain(lines = 2000)
    print "Hello my name is MarkovBot"
    #Print a ready symbol
    while(True):
        input = raw_input(">")
        #If input is exit, exit
        if input == "exit":
            import sys
            sys.exit()
        #Search the input for keywords
        candidate_tuples = []
        keywords = input.strip().split()
        for word in keywords:
            for tuple in chain.node_dict.keys():
                if word in tuple:
                    candidate_tuples.append(tuple)
                    break;
        #Make a response from the keywords in the markov chain
        response = []
        response_candidate_list = []
        for tuple in candidate_tuples:
            response_candidate_list.append(chain.node_dict[tuple])
        #Choose a first word
        words_to_choose = []
        for candidate in response_candidate_list:
            for word in candidate.next_words.keys():
                words_to_choose.append(word)
        random.shuffle(words_to_choose)
        #Make a chain from this word
        try:
            word_list = [words_to_choose[0]]
        except:
            print "ugh.. that sentence is confusing"
        for x in range(10):
            try:
                next_node = chain.node_dict[tuple(word_list)]
            except:
                break;
        #Print the sentence
        sentence = ""
        for word in word_list:
            sentence += word+" "
        print sentence