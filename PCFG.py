'''
@author: Kechen
'''

class PCFG():
    def __init__(self):
        self.lexicon={'that':('Det',), 'a':('Det',), 'the':('Det',), 
                      'book':('Noun','Verb','Nominal'), 'flight':('Noun','Nominal'), 'money':('Noun','Nominal'),'flights':('Noun','Nominal'), 'dinner':('Noun','Nominal'),
                      'includes':('Verb',), 'prefer':('Verb',),
                      'I':('Pronoun','NP'), 'she':('Pronoun','NP'), 'me':('Pronoun','NP'), 'you':('Pronoun','NP'),
                      'Houston':('Proper-Noun','NP'), 'NWA':('Proper-Noun','NP'),
                      'from':('Preposition',), 'to':('Preposition',), 'on':('Preposition',), 'with':('Preposition',), 'through':('Preposition',),}
        
        self.lexiconpro={('that','Det'):0.1, ('a','Det'):0.3, ('the','Det'):0.6,
                         ('book','Noun'):0.1, ('flight','Noun'):0.3, ('dinner','Noun'):0.15, ('money','Noun'):0.05, ('flights','Noun'):0.4,
                         ('includes','Verb'):0.3, ('book','Verb'):0.3, ('prefer','Verb'):0.4,
                         ('I','Pronoun'):0.4, ('she','Pronoun'):0.5, ('me','Pronoun'):0.15, ('you','Pronoun'):0.4,
                         ('Houston','Proper-Noun'):0.6, ('NWA','Proper-Noun'):0.4,
                         ('from','Preposition'):0.3, ('to','Preposition'):0.3, ('on','Preposition'):0.2, ('with','Preposition'):0.15,
                         ('through','Preposition'):0.05,
                         ('I','NP'):0.2, ('she','NP'):0.05, ('me','NP'):0.05, ('you','NP'):0.05,
                         ('Houston','NP'):0.2, ('NWA','NP'): 0.1,
                         ('book','Nominal'):0.075, ('flight','Nominal'):0.225, ('dinner','Nominal'):0.1, ('money','Nominal'):0.05, ('flights','Nominal'):0.3,}
        
        self.grammar={('NP','VP'):'S',('X1','VP'):'S',('X2','PP'):'S',('VP','PP'):'S',('Verb','PP'):'S',('Aux','NP'):'X1',
                      ('Det','Nominal'):'NP',
                      ('Verb','NP'):'VP', ('X2','PP'):'VP', ('Verb','PP'):'VP', ('VP','PP'):'VP', ('Verb','PP'):'X2',
                      ('Preposition','NP'):'PP',
                      ('Nominal','Noun'):'Nominal', ('Nominal','PP'):'Nominal'}
        
        self.grammarpro={('NP','VP','S'):0.8,('X1','VP','S'):0.15,('X2','PP','S'):0.01,('VP','PP','S'):0.01,('Verb','PP','S'):0.03,('Aux','NP','X1'):1.0,
                         ('Det','Nominal','NP'):0.2, 
                         ('Verb','NP','VP'):0.2, ('X2','PP','VP'):0.2, ('Verb','PP','VP'):0.2, ('VP','PP','VP'):1.0, ('Verb','PP','X2'):1.0,
                         ('Preposition','NP','PP'):1.0,
                         ('Nominal','Noun','Nominal'):0.2, ('Nominal','PP','Nominal'):0.05,
                          }
        self.allgrammar=['Det', 'Noun', 'Verb', 'Nominal', 'NP', 'Proper-Noun', 'Preposition', 'S', 'PP', 'VP', 'X2']
        
    def pcfg(self, sentence):
        words=sentence.split()
        parsetree={}
        for x in range(len(words)+1):
            for y in range(len(words)+1):
                parsetree[x,y]=0
        back={}
        wordgram={}
        for j in range(1,len(words)+1):
            word=words[j-1]
            grammars=self.lexicon[word]
            for grammar in grammars:
                prob=self.lexiconpro[(word,grammar)]
                parsetree[j-1,j,grammar]=prob
                wordgram[j-1,j,grammar]=prob
            for i in range(j-2,-1,-1):
                for k in range(i+1,j):
                    for leftgram in self.allgrammar:
                        for rightgram in self.allgrammar:
                            if (i,k,leftgram) in parsetree and (k,j,rightgram) in parsetree and (leftgram,rightgram) in self.grammar:
                                leftgramprob=parsetree[i,k,leftgram]
                                rightgramprob=parsetree[k,j,rightgram]
                                combinegram=self.grammar[(leftgram,rightgram)]
                                combineprob=self.grammarpro[(leftgram,rightgram,combinegram)]
                                if parsetree[i,j]<(combineprob*leftgramprob*rightgramprob):
                                    parsetree[i,j,combinegram]=(combineprob*leftgramprob*rightgramprob)
                                    parsetree[i,j]=(combineprob*leftgramprob*rightgramprob)
                                    back[i,j,combinegram]=(k,leftgram,rightgram,parsetree[i,j,combinegram])
        print back
        print wordgram          
                                
if __name__ == '__main__':
    PCFG().pcfg('I book a dinner from Houston')
    PCFG().pcfg('I book a dinner')
    PCFG().pcfg('I prefer to book a dinner')
    PCFG().pcfg('the flight includes a dinner')
    PCFG().pcfg('I prefer to book a dinner from you')
    PCFG().pcfg('I prefer to flight with you')
    
    