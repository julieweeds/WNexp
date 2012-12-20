'''
Created on Dec 4, 2012

@author: juliewe
'''

import re

class Entry:
    '''
    classdocs
    '''
    entrycount=0;
    wordPatt=re.compile('(.*)/.*')

    def __init__(self,word1,word2,sim):
        '''
        Constructor
        '''
        matchobj=Entry.wordPatt.match(word1)
        if matchobj:
            word1=matchobj.group(1)
        matchobj=Entry.wordPatt.match(word2)
        if matchobj:
            word2=matchobj.group(1)
        self.word1=word1
        self.word2=word2
        self.sim=sim
        Entry.entrycount +=1

    def displayEntry(self):
        
        print self.word1, ":", str(self.sim), ":", self.word2
        
class Neighbours:
    entrycount=0;
    
    def __init__ (self,word):
        self.word=word
        self.neighcount=0
        self.neighbours={}
        Neighbours.entrycount +=1
        
    def addEntry(self,entry):
        if(entry.word1==self.word):
            self.neighbours[entry.word2]=entry.sim
        else:
            print "Error : cannot add to ", self.word
            entry.displayEntry()
            
    def lookupSim(self,word):
        return self.neighbours[word]

    def displayNeighs(self):
        print "Neighbours of ",self.word,": "
        for key,value in self.neighbours.items():
            print key, value
    
class Thesaurus:
    entrycount=0;
    
    def __init__ (self, filename):
        self.filename=filename
        self.entries={}
        Thesaurus.entrycount +=1
        
    def addEntry(self,entry):
        if entry.word1 in self.entries:
            self.entries[entry.word1].addEntry(entry)    
        else:
            self.entries[entry.word1]=Neighbours(entry.word1)
            self.entries[entry.word1].addEntry(entry)
            
    def lookupSim(self,word1,word2):
        sim=0
        if word1 in self.entries:
            if word2 in self.entries[word1].neighbours:
                sim = self.entries[word1].lookupSim(word2)
        return sim

    def inThes(self,word):
        if word in self.entries:
            return True
        else:
            return False

    def displayNeighs(self,word):
        if word in self.entries:
            self.entries[word].displayNeighs()
        else:
            print "No neighbours for ",word," in thesaurus"
    def process(self,line):
        wordlist = line.split('\t')
        #print line
        #print wordlist
        wordlist.reverse()
        listlen = len(wordlist)
        headword = wordlist.pop()
        #print headword
        #print len(wordlist)
        if (len(wordlist)%2 != 0):
            print "Error with length of line", line
            exit()
        while(len(wordlist)>0):
            neigh=wordlist.pop()
            sim=wordlist.pop()
            e = Entry(headword,neigh,sim)
            self.addEntry(e)
        if ((Entry.entrycount%1000)==0):
            print headword, ":", Entry.entrycount


    
    def readfile(self):
        f = open(self.filename,'r')
        for line in f:
            self.process(line.rstrip())
        f.close()

        