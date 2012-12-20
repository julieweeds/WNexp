'''
Created on Dec 4, 2012

@author: juliewe
'''

#test thesaurus class

from thesaurus import Thesaurus
from thesaurus import Entry
from thesaurus import Neighbours

filename='/Volumes/research/calps/data3/mlcl/DisCo/thesauri/exp4-11c.strings'

mythesaurus = Thesaurus("test")
#
e1 = Entry("cat/N","dog/N",0.8)
e2 = Entry("cat/N","ostrich/N",0.5)
e3 = Entry("dog/N","ostrich/N",0.6)

mythesaurus.addEntry(e1)
mythesaurus.addEntry(e2)
mythesaurus.addEntry(e3)



print "Similarity between cat and ostrich is ", mythesaurus.lookupSim("cat","ostrich")
print "Similarity between cat and bird is ", mythesaurus.lookupSim("cat","bird")

print "Number of entries:", Entry.entrycount
print "Number of neighbour sets:", Neighbours.entrycount
print "Number of thesauruses:", Thesaurus.entrycount

mythesaurus2 = Thesaurus(filename)
mythesaurus2.readfile()
print "Similarity between hare and parakeet is ", mythesaurus2.lookupSim("hare","parakeet")
print "Similarity between month and year is ", mythesaurus2.lookupSim("month","year")
print "Similarity between year and month is ", mythesaurus2.lookupSim("year","month")

mythesaurus2.displayNeighs("hare")
mythesaurus2.displayNeighs("month")

print "Number of entries:", Entry.entrycount
print "Number of neighbour sets:", Neighbours.entrycount
print "Number of thesauruses:", Thesaurus.entrycount
