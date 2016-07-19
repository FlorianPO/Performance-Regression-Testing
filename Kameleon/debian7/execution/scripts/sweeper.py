#!/usr/bin/env python

import sys
from math import factorial
import random

class Sweeper():
    def __init__(self):
        self.arguments = []
        self.combinaisons = []
        self.avoided = []

    def setArguments(self, argument_list):
        self.arguments = list(argument_list)
        
    def setAvoided(self, combinaison_list):
        self.avoided = list(combinaison_list)

    def calculate(self, empty_combinaison=False, singleton=True):
        if empty_combinaison:        
            self.combinaisons.append([''])

        nbr_arg = None
        if singleton:
            nbr_arg = 1
        else:
            nbr_arg = 2
        while nbr_arg <= len(self.arguments):
            # Init index_list
            index_list = []
            for i in range(0, nbr_arg):    
                index_list.append(i)
            
            # Calculate combinaisons
            while True:
                cmb = self._getFromIndex(index_list)
                if (not self._isAvoided(cmb)):
                    self.combinaisons.append(cmb)
                if (self._stepIndexList(index_list) == True):
                    break             
            nbr_arg += 1

    def add(self, combinaison):
        self.combinaisons.append(combinaison)

    def insert(self, combinaison, index=0):
        self.combinaisons.insert(index, combinaison)

    def hasNext(self):
        return len(self.combinaisons) > 0

    def next(self): # You should test hasNext() before
        cmb = self.combinaisons[0]        
        del self.combinaisons[0]
        return cmb

    def contains(self, combinaison):
        if combinaison in self.combinaisons:
            return True
        else:
            return False

    def remove(self, combinaison):     
        self.combinaisons.remove(combinaison)

    def shuffle(self):
        random.shuffle(self.combinaisons)

    def __str__(self): # Returns all combinaisons
        string = ''
        for i in range(0, len(self.combinaisons)):
            string += self.combinaisons[i].__str__() + '\n'
        return string

    def _getFromIndex(self, index_list):
        tmp_list = []
        for i in range(0, len(index_list)):
            tmp_list.append(self.arguments[index_list[i]])
        return tmp_list

    def _stepIndexList(self, index_list):
        index_dealed = len(index_list)-1
    
        # Last index
        if (index_list[index_dealed] < len(self.arguments)-1):                
            index_list[index_dealed] += 1
            return False
        
        # Other index
        while index_dealed > 0:
            index_dealed -= 1
            if (index_list[index_dealed]+1 != index_list[index_dealed+1]):
                index_list[index_dealed] += 1
                sum_this = 1
                for i in range(index_dealed+1, len(index_list)):
                    index_list[i] = index_list[index_dealed] + sum_this
                    sum_this += 1
                return False
                        
        return True

    def _isAvoided(self, combinaison):        
        for i in range(0, len(self.avoided)):
            if (len(self.avoided[i]) == len(combinaison)):
                options_found = None
                for j in range(0, len(self.avoided[i])):
                    if self.avoided[i][j] in combinaison:
                        options_found = True
                    else:
                        options_found = False
                        break
                if (options_found):
                    return True
        return False 

if __name__ == "__main__":
    arguments = ['a', 'b', 'c', 'd', 'e']
    combinaisons_to_avoid = [['b', 'a'], ['d', 'b', 'c', 'a']]

    sweeper = Sweeper()

    sweeper.setArguments(arguments)
    sweeper.setAvoided(combinaisons_to_avoid)
    sweeper.calculate(singleton=False)

    sweeper.add(['this', 'is', 'added'])
    # sweeper.shuffle()
    
    print(sweeper)
