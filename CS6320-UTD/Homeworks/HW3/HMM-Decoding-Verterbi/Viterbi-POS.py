import pandas as pd
import sys

class Viterbi(object):
    def intialize(self):
    	transition_prob = pd.DataFrame({'tags':['NNP','MD','VB','JJ','NN','RB','DT'],
    	                   '<s>':[0.2767, 0.0006, 0.0031, 0.0453, 0.0449, 0.0510, 0.2026],
    	                   'NNP':[0.3777, 0.0110, 0.0009, 0.0084, 0.0584, 0.0090, 0.0025],
    	                   'MD':[0.0008, 0.0002, 0.7968, 0.0005, 0.0008, 0.1698, 0.0041],
    	                    'VB':[0.0322, 0.0005, 0.0050, 0.0837, 0.0615, 0.0514, 0.2231],
    	                    'JJ':[0.0366, 0.0004, 0.0001, 0.0733, 0.4509, 0.0036, 0.0036],
    	                    'NN':[0.0096, 0.0176, 0.0014, 0.0086, 0.1216, 0.0177, 0.0068],
    	                    'RB':[0.0068, 0.0102, 0.1011, 0.1012, 0.0120, 0.0728, 0.0479],
    	                    'DT':[0.1147, 0.0021, 0.0002, 0.2157, 0.4744, 0.0102, 0.0017]
    	                    })
    
    	transition_prob = transition_prob.set_index(['tags'])
    	transition_prob = transition_prob.T
    	transition_prob.columns = ('NNP','MD','VB','JJ','NN','RB','DT')
    
    
    	emission_prob = pd.DataFrame({'tags':['Janet', 'will', 'back', 'the', 'bill'],
    	                   'NNP':[0.000032, 0, 0, 0.000048, 0],
    	                   'MD':[0, 0.308431, 0, 0, 0],
    	                    'VB':[0, 0.000028, 0.000672, 0, 0.000028],
    	                    'JJ':[0, 0, 0.00340, 0, 0],
    	                    'NN':[0, 0.000200, 0.000223, 0, 0.002337],
    	                    'RB':[0, 0, 0.010446, 0, 0],
    	                    'DT':[0, 0, 0, 0.506099, 0]})
    	emission_prob = emission_prob.set_index(['tags'])
    	emission_prob = emission_prob.T
    	emission_prob.columns = ('Janet', 'will', 'back', 'the', 'bill')
    
    
    	viterbi_prob=  pd.DataFrame({'tags':['Janet', 'will', 'back', 'the', 'bill'],
    	                   'NNP':[0.0, 0.0, 0.0, 0.0, 0.0],
    	                   'MD':[0.0, 0.0, 0.0, 0.0, 0.0],
    	                    'VB':[0.0, 0.0, 0.0, 0.0, 0.0],
    	                    'JJ':[0.0, 0.0, 0.0, 0.0, 0.0],
    	                    'NN':[0.0, 0.0, 0.0, 0.0, 0.0],
    	                    'RB':[0.0, 0.0, 0.0, 0.0, 0.0],
    	                    'DT':[0.0, 0.0, 0.0, 0.0, 0.0]})
    
    	viterbi_prob = viterbi_prob.set_index(['tags'])
    	viterbi_prob = viterbi_prob.T
    	viterbi_prob.columns = ('Janet', 'will', 'back', 'the', 'bill')
    	#viterbi_prob
    
    	back_pointer=  pd.DataFrame({'tags':['Janet', 'will', 'back', 'the', 'bill'],
    	                   'NNP':["", "", "", "", ""],
    	                   'MD':["", "", "", "", ""],
    	                    'VB':["", "", "", "", ""],
    	                    'JJ':["", "", "", "", ""],
    	                    'NN':["", "", "", "", ""],
    	                    'RB':["", "", "", "", ""],
    	                    'DT':["", "", "", "", ""]})
    
    	back_pointer = back_pointer.set_index(['tags'])
    	back_pointer = back_pointer.T
    	back_pointer.columns = ('Janet', 'will', 'back', 'the', 'bill')
    
    	return emission_prob,transition_prob, viterbi_prob, back_pointer
    
    
    def viterbi(self,states, sentence, emission_prob, transition_prob, viterbi_prob, back_pointer):
    
        solution = []
        
        for s in states:
            viterbi_prob[sentence[0]][s] = transition_prob[s]['<s>'] * emission_prob[sentence[0]][s]
            back_pointer[sentence[0]][s] = None
           
                         
        for word in range(1, len(sentence)):
            for tag in range(0, len(states)):        
           
                prob_max = viterbi_prob[sentence[word-1]][states[0]] * transition_prob[states[tag]][states[0]] * emission_prob[sentence[word]][states[tag]]
                current_prev_tag = states[0]
    
                for prev_tag in states[1:]:
                    
                    temp_tr_prob = viterbi_prob[sentence[word - 1]][prev_tag] * transition_prob[states[tag]][prev_tag] * emission_prob[sentence[word]][states[tag]]
                 
                    if temp_tr_prob > prob_max:
                        prob_max = temp_tr_prob
                        current_prev_tag = prev_tag
                                        
                viterbi_prob[sentence[word]][states[tag]] = prob_max
                back_pointer[sentence[word]][states[tag]] = current_prev_tag
                
        max_prob = 0
        for word in range(0, len(sentence)):
            for tag in range(0, len(states)):
                if viterbi_prob[sentence[word]][states[tag]] > max_prob:
                    max_prob = viterbi_prob[sentence[word]][states[tag]]
                    max_prob_tag = states[tag]
            max_prob = 0
                    
            solution.append(max_prob_tag)
            
        print("The probability of assigning the tag sequence:", viterbi_prob[sentence[-1]][:].max())
                
            
                
        return solution, viterbi_prob, back_pointer


def main():
   
    sentence1 = "back the bill Janet will"
    V = Viterbi()
    emission_prob,transition_prob,viterbi_prob,back_pointer = V.intialize()
    states = emission_prob.index
   
    sentence1 = sys.argv[1].split()
    # sentence1 = "back the bill Janet will".split()

    print("For Sentence1:")
    solution_tags1, viterbi_matrix1, back_pointer1 = V.viterbi(states, sentence1, emission_prob, transition_prob, viterbi_prob,back_pointer)
    print("Sequence of tags assingned:",solution_tags1)
    # print("viterbi probability matrix", viterbi_matrix1)


main()