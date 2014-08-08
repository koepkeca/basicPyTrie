#!/usr/bin/python

############################################
#Basic Trie structure written in python 2.6
#Tested on Python 2.6.6 CentOS 6.4
#Procedural version, for testing only
#Very Basic implementation
############################################
'''

This implementation has the following requirements:

1) Data Structure
2) Methods:
  a) build the trie from a list (*)
  b) add word to the trie (*)
  c) check if a specific word is in the trie (*)
  d) get a sub-trie at a start string (prefix) (*)
  e) get number of words in a trie (x) (you could just get the elements in the list.. not sure if easier/better way)
  f) get list of words in the trie (*)

'''

import signal
import sys


############################################
#Catches Ctrl+C for cleanup and bye message
############################################
def sigCatch(sig,frame):
    print "\n\nGoodbye!\n"
    sys.exit(0)

############################################
#Builds the trie data structure from a list 
#of words. void return
############################################

def buildTrie(trie,*words):
    for word in words:
        curr = trie 
        for letter in word:
            curr = curr.setdefault(letter,{})
        #I'm using {"EOL":1} to denote the end of a node
        #This signifies we've reached the end of a word in the trie
        #I suppose NULL would be just as good...
        curr = curr.setdefault("EOL",1)

#############################################
#Adds word to an existing or new trie
#void return
#############################################
def addToTrie(trie,word):
    curr = trie
    for letter in word:
        curr = curr.setdefault(letter,{})
    curr = curr.setdefault("EOL",1)

############################################
#Returns subtrie of prefix from passed trie
#dict return (trie)
############################################
def getSubTrie(trie,prefix):
    rootNode = trie
    for letter in prefix:
        if letter in rootNode:
            rootNode = rootNode[letter]
        else:
            return {}  ##could/should this be rootNode = {} ??? 
    else:
        return rootNode

################################################
#This return 1 if the complete word is found
#in the current trie structure. If the word
#is not found, then 0 is returned
#Also, this function has multiple return points
#I'm not proud or fond of that...
#int return (boolean)
#################################################

def isWordInTrie(trie,word):
    curr = trie
    for letter in word:
        if letter in curr:
            curr = curr[letter]
        else:
             return 0
    else:
        if "EOL" in curr:
            rv = 1
        else:
            rv = 0 
    return rv


##############################################
#Take a list of found suffixes and prepend a
#string to the front of each making a word
#list out of a partial string and list of
#suffixes generated from a partial trie
#list return (words)
##############################################
def prependList(prefix,wordList):
    retList = []
    for suffix in wordList:
        retList.append(prefix + suffix)
    return retList

###################################################
#testList takes a trie struct and a list of words
#and ensures each word in the list is in the trie
#this function should be run after a trie is build
#with all the letters in the alphabet to ensure that
#the trie was build correctly. This should not fail
#void return
####################################################
def testList(myTrie,listToTest):
    for word in listToTest:
        if not isWordInTrie(myTrie,word):
            print ("Whoops.. %s is not in trie" % word)

#########################################################
#walkTrie takes a trie and recursivly walks down it to 
#return words that are in a trie.
#I feel like the prefixStr = prefixStr[0:depth] line is 
#a kludge, but without it the prefixStr array grows
#with each iteration
#void return
#########################################################

def walkTrie(trie,rList,depth=0,prefixStr = list()):
     for k,v in trie.items():
        prefixStr = prefixStr[0:depth] #this works, but feels like cheating..
        if isinstance(v,dict):
            prefixStr.insert(depth,k)
#            print prefixStr
            walkTrie(v,rList,depth + 1,prefixStr)
        else:
            newArr = prefixStr[0:depth]
            rList.append(''.join(newArr))

##############################################################
#testGeneratedTrie is a self test function designed to ensure
#that a trie structure was created sucessfully. This takes
#a list of range [a-z] and generates sub-trie's for each
#letter and ensures all the words in those sub-trie's are
#infact in the trie. If this function produces any failures
#there is a problem with the trie implementation. Once a trie
#is created, this function should be run.
#void return
################################################################

def testGeneratedTrie(trieToTest):
    letterList = map(chr,range(97,123))
    for letter in letterList:
        rList = tList =  []
        testSubTrie = getSubTrie(trieToTest,letter)
        walkTrie(testSubTrie,rList)
        tList = prependList(letter,rList)
        testList(trieToTest,tList) 

################################################################
#createTrieFromFile takes a trie structure and a file and loads
#each line of the file into the trie. Lines are seperated by
#\n
#dict return (trie)
################################################################

def createTrieFromFile(trie,fileName):
    fp = open(fileName,'r')
    for line in fp:
        #normalize the words by removing the newline and 
        #making the words uniform lower case
        word = line.strip("\n").lower()
        addToTrie(trie,word)
    return trie


signal.signal(signal.SIGINT,sigCatch)


myTrie = subTrie = {} #main and sub trie
wordList = [] #word list

#Generate the trie from the words file and validate the data structure

print "Loading List..."
myTrie = createTrieFromFile(myTrie,'/usr/share/dict/words')
print "Validating List.."
testGeneratedTrie(myTrie)

##########################################
#The main loop here will accept prefixes
#and print a list of all the words in the
#trie with the given prefix
##########################################

while 1:
    wordList = [] #clear the word list
    inputWord = raw_input(">>")
    originalWord = inputWord
    inputWord = inputWord.strip("\n").lower()
    subTrie = getSubTrie(myTrie,inputWord)
    walkTrie(subTrie,wordList)
    print prependList(inputWord,wordList)
