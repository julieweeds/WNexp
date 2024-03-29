import re
import sys
###
#gigacount takes an extracted feature file (from a corpus such as the gigaword) and counts the number of instance
# occurrences of each noun,verb,adj and adverb - it only looks at the first word in each line as this is the instance
# (other words in the line are the feature)
#
#it then takes the WN multiple choice test and looks up each unigram in its word lists - it checks for 1, 2, 3, 4, 5
#or more occurrences.  It also computes 2 unions 1) for nouns and adjs and 2) for all pos.  This is for a threshold
#frequency value



#from thesaurus import Thesaurus
from WNEval import Eval

###filenames on apollo
dirname = "/mnt/lustre/scratch/inf/mmb28/FeatureExtrationToolkit/feoutput-deppars/"
datadir="/mnt/lustre/scratch/inf/juliewe/WNexp/data/"


###filenames on local
#dirname = "/Volumes/research/calps/data3/juliewe/exp6-12/"
#datadir="/Volumes/research/calps/data3/juliewe/"

#filename="exp6small"
filename="exp6"
myfile="turney.txt"

inputname=dirname+filename
filename=datadir+myfile

class PoSset:
    #list of words and frequencies for particular POS
    entrycount=0

    def __init__(self,pos):
        PoSset.entrycount += 1
        self.pos = pos
        self.wordcountlist = {}
        self.testcounts={1:0,2:0,3:0,4:0,5:0} #each key is mapped to how many words (that are looked up) have occurred that number of times or more


    def addword(self,word):
        #increase seen frequency of word by 1
        if word in self.wordcountlist:
            self.wordcountlist[word] +=1
        else:
            self.wordcountlist[word] = 1

    def getword(self,word):
        #return seen frequency of word
        if word in self.wordcountlist:
            return self.wordcountlist[word]
        else:
            return 0

    def displayall(self):
        #print out all words and frequencies
        print self.pos
        for word in self.wordcountlist:
            print word, ":", self.getword(word)

    def check(self,word):
        #perform test on word.  If in list, update total number of words that have occurred over threshold levels
        #in test counts.  Also return frequency so that union totals can be updated appropriately.
        freq = self.getword(word)
        for key in self.testcounts.keys():
            if (freq >= key):
                self.testcounts[key]+=1
        return freq



class Gigadict:
    entrycount=0
    linePatt = re.compile("(.*)/(.)") #match the first word in each line and split into word and POS tag
    threshold = 1


    def __init__(self,filename):
        Gigadict.entrycount += 1
        self.nouns=PoSset("noun")
        self.verbs=PoSset("verb")
        self.adjs=PoSset("adj")
        self.advs=PoSset("adv")
        self.linecount=0
        self.readfile(filename)
        self.tests=0  #number of words looked up
        self.any=0    #union of words occurring in any list
        self.nj=0  #union of words occurring in noun and adj list


    def process(self,line):
        matchobj = Gigadict.linePatt.match(line)
        if matchobj:
            word = matchobj.group(1)
            pos = matchobj.group(2)
            if pos == "N":
                self.nouns.addword(word)
            if pos == "V":
               self.verbs.addword(word)
            if pos == "J":
                self.adjs.addword(word)
            if pos == "R":
                self.advs.addword(word)
        else:
            print "Input error line "+str(self.linecount)+" : "+line

    def readfile(self,filename):
        f = open(filename,'r')
        for line in f:
            self.linecount +=1
            self.process(line.rstrip())
            if((self.linecount % 1000)==0):print "Read line: "self.linecount
        f.close()

    def breakpoint(self):
        self.nouns.displayall()
        self.verbs.displayall()
        self.adjs.displayall()
        self.advs.displayall()
        sys.exit(1)

    def check(self,question):
        rq = question.reverse()
        bigram=question.pop()
        while(len(question)>0):
            word = question.pop()
            self.tests+=1
            n=self.nouns.check(word)
            v=self.verbs.check(word)
            j=self.adjs.check(word)
            r=self.advs.check(word)
            if(n+j>=Gigadict.threshold):self.nj+=1
            if(n+j+v+r>=Gigadict.threshold):self.any+=1


    def checkquestions(self,questionlist):
        for question in questionlist:
            self.check(question)


def posset_test():
    mynouns = PoSset("noun")
    myverbs = PoSset("verb")

    mynouns.addword("cow")
    mynouns.addword("sheep")
    myverbs.addword("hurry")
    mynouns.addword("cow")
    myverbs.addword("paste")
    myverbs.addword("paste")
    myverbs.addword("paste")
    mynouns.addword("paste")

    mynouns.displayall()
    myverbs.displayall()

#posset_test()

print "Coverage evaluation started for ",filename," and ",inputname
mydata = Eval(filename,'Testing')
mydata.readfile()
print "Read" + filename
mycount = Gigadict(inputname)
print "Read" + inputname
mycount.checkquestions(mydata.questions)
print mycount.nj, mycount.any, mycount.tests
print "nouns", mycount.nouns.testcounts
print "verbs", mycount.verbs.testcounts
print "adjs", mycount.adjs.testcounts
print "advs", mycount.advs.testcounts