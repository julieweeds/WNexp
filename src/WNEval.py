
from thesaurus import Thesaurus
import re


class Eval:
    entrycount=0
    comment = re.compile('#')
    testingPatt = re.compile('#   Testing Subset')
    trainingPatt = re.compile('#   Training Subset')

    def __init__(self,filename,type):
        self.filename=filename
        Eval.entrycount+=1
        self.linecount=0
        self.commentcount=0
        self.type=type
        self.inset=False
        self.positive=0
        self.token=0
        self.guesses=0
        self.simpairs=0
        self.correctpairs=0
        self.thesauri = []
        self.questions=[]




    def addLine(self,line):
        betterlist=[]
        wordlist=line.split('|')
        for word in wordlist:
            word=word.strip()
            betterlist.append(word)
            #       print betterlist
        self.questions.append(betterlist)
        #       self.processQuestion(betterlist)


    def process(self,line):

        matchobj = Eval.comment.match(line)
        if matchobj:
            self.commentcount+=1
            matchobj = Eval.trainingPatt.match(line)
            if matchobj:
                #print line
                if (self.type=='Training'):
                    self.inset=True
                else:
                    self.inset=False
            else:
                matchobj = Eval.testingPatt.match(line)
                if matchobj:
                    #print line
                    if(self.type=='Testing'):
                        self.inset=True
                    else:
                        self.inset=False

                        #print line, self.inset
        else:
            if(self.inset):
                self.linecount+=1
                self.addLine(line)


    def readfile(self):
        f = open(self.filename,'r')
        for line in f:
            self.process(line.rstrip())
            #           if self.linecount>1:
            #              exit()
        f.close()

    def processCoverQuestion(self,question):
        #print question
        index = len(self.thesauri)
        for word in question:
            positive=0
            for thes in self.thesauri:
                if thes.hasNeighs(word):
                    positive = 1
            self.positive+=positive
            self.token+=1

    def processQuestions(self):
        for question in self.questions:
            self.processQuestion(question)

    def processQuestion(self,question):
        question.reverse()
        bigram = question.pop()
        bigramlist = bigram.split(' ')
        mod=bigramlist[0]
        head=bigramlist[1]
        maxsim=0.01
        mostsim=0
        choiceno=0
        #        print mod,head
        while(len(question)>0):
            choice=question.pop()
            choiceno = choiceno+1
            sim = self.findSim(mod,head,choice)
            if ((choiceno == 1) & (sim>0.01)): self.correctpairs= self.correctpairs + 1
            print mod,head,choice,sim
            if (sim>maxsim):
                maxsim=sim
                mostsim=choiceno
        if mostsim==1:
        #            print "YAY!"
            self.positive = self.positive + 1.0
        if mostsim==0:
            self.guesses = self.guesses + 1.0
        print self.positive, self.guesses, self.linecount

    def findSim(self,a,b,c):
        #simplesimilarity
        return self.findGeoSim(a,b,c)

    def findGeoSim(self,a,b,c):
        maxasim=0.01
        maxbsim=0.01
        inthes = False
        for thes in self.thesauri:
            if thes.inThes(c):inthes = True
            asim=float(thes.lookupSim(a,c))
            bsim=float(thes.lookupSim(b,c))
            if(asim>maxasim):maxasim=asim
            if(bsim>maxbsim):maxbsim=bsim
        geosim = (maxasim*maxbsim)**0.5
        if geosim > 0.01 : self.simpairs = self.simpairs + 1
        if inthes:self.token = self.token + 1
        return geosim




    def addThesaurus(self,thesname):
        index = len(self.thesauri)
        self.thesauri.append(Thesaurus(thesname))
        self.thesauri[index].readfile()

