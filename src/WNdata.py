import re
import sys
from WNEval import Eval
from thesaurus import Thesaurus


###filenames at home
#datadir="../data/"
#thesdir="../thesauruses/"

###filenames at uni

datadir="/Volumes/research/calps/data3/juliewe/"
thesdir="/Volumes/research/calps/data3/mlcl/DisCo/thesauri/"

###filenames on apollo
#datadir="/mnt/lustre/scratch/inf/juliewe/WNexp/data/"
#thesdir="/mnt/lustre/scratch/inf/juliewe/WNexp/thesauri/"
outputdir="../output/"


myfile="turney.txt"
filename=datadir+myfile
if len(sys.argv) > 1 :
    thesname=sys.argv[1]
else:
    thesname="exp4-11"
adjthesname=thesdir+thesname+"c.strings"
nounthesname=thesdir+thesname+"a.strings"



###test
lines = []
myeval=Eval(filename,'Testing')
lines.append('File : '+filename+"\n")
#print "Number of question sets is ",len(myeval.questions)
#myeval.displayQuestion(0)

myeval.addThesaurus(adjthesname)
lines.append("Read in thesaurus " +adjthesname+"\n")
print lines[len(lines)-1]
myeval.addThesaurus(nounthesname)
lines.append("Read in thesaurus" + nounthesname +"\n")
print lines[len(lines)-1]
myeval.readfile()
myeval.processQuestions()
lines.append("Number of questions is " + str(myeval.linecount)+"\n")
print lines[len(lines)-1]
lines.append("Number answered correctly using thesauruses is " + str(myeval.positive)+"\n")
print lines[len(lines)-1]
lines.append("Number of guesses is "+ str(myeval.guesses)+"\n")
print lines[len(lines)-1]
lines.append("Proportion is"+ str((100.0*myeval.positive)/myeval.linecount)+"\n")
print lines[len(lines)-1]
unigram = (100*myeval.token)/(myeval.linecount*7.0)
lines.append("Unigram coverage isb"+ str(unigram)+"\n")
print lines[len(lines)-1]
pairwise = (100*myeval.simpairs)/(myeval.linecount * 7.0)
lines.append("Pairwise coverage is "+ str(pairwise)+"\n")
print lines[len(lines)-1]
lines.append("Pairwise coverage if sim(a,a) = 1 : "+ str((100 * (myeval.simpairs + 2.0 * myeval.linecount))/(myeval.linecount * 7.0))+"\n")
print lines[len(lines)-1]
correct = (100.0 * myeval.correctpairs)/myeval.linecount
lines.append("Pairwise coverage for correct matches is "+ str(correct)+"\n")
print lines[len(lines)-1]

#print len(lines)

####write results file
outputname=outputdir+"results_"+thesname+"_"+myfile
fileoutput = open(outputname,'w')
fileoutput.writelines(lines)
fileoutput.close()



sys.exit()