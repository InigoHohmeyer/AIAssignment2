"""
Title: Artificial Intelligence Assignment 2
Author: Inigo Hohmeyer
"""


#   Putnam-Davis Solver
#   Objective: Need to create a method which given a set a statements and atoms can make
#   give us the T-F settings of the atoms so that all the statements will be true


def clause_maker(input):
    #   Creates a hashtable:
    #   clause number is key, value is actual clause as a list with each atom as an int
    clauseTable = {}
    with open(input) as file:
        data = file.readlines()
        for index, value in enumerate(data):
            if value[0] == "0":
                break
            else:
                clauseTable[index] = list(map(int, value.split()))
    return clauseTable
#   This method goes through clauseTable
#   And finds the atoms
#   It will then list the atoms in order
def number_list(clauseTable):
    if not clauseTable:
        return 0
    else:
        numberList = []
        for i in clauseTable:
            for j in clauseTable[i]:
                if abs(j) not in numberList:
                    numberList.append(abs(j))
        numberList = sorted(numberList)
        return numberList

#   This method will return a version of the clauseTable that gets rid
#   of all the clauses where the atom is true. And where it is false it simply deletes it.
def Deletion(clauseTable, atom):
    #   Creates a newClauseTable which will be returned
    newClauseTable = clauseTable.copy()
    #   Iterates through the clauseTable
    for i in clauseTable:
        #   If the clause that we are looking at
        #   has a length of 1, but it's the opposite of the atom we
        #   are testing we will return false
        if len(clauseTable[i]) == 1 and clauseTable[i][0] == atom * -1:
            return False
        else:
            for j in clauseTable[i]:
                #   If the atom is equal to our specified atom then the entire sentence
                #   will be removed
                if j == atom:
                    newClauseTable.pop(i)
                    continue
                #   If the atom is opposite to our specified atom and the clause has a length of 1
                #   then we will return False since this branch will never be true.

                #   If the atom is the negative version of our specified atom we will simply remove it from the
                #   clause
                elif j == atom * -1:
                    newClauseTable[i].pop(newClauseTable[i].index(j))
    #   returns the modified clauseTable with the certain atom deleted
    return newClauseTable


def putnam_davis(clauseTable, output, numberList):
    #   Base Case:
    #   If the entire clauseTable is empty then we can return.
    if not clauseTable:
        return 0
    #   If clauseTable is equal to False
    #   This means that our deletion function found a
    #   contradiction, and we must return 0.
    elif len(clauseTable) == 0:
        return output
    else:
        for i in clauseTable:
            #   Checks if the clause is a literal clause
            if len(clauseTable[i]) == 1:
                #   This is triggered if the clause is true
                if clauseTable[i][0] > 0:
                    #   Adds the true version of it to the OutPutTable
                    newOutput = output.copy()
                    newOutput[abs(clauseTable[i][0])] = "T"
                    #   Creates a new clause table by using the deletion method
                    newClauseTable = Deletion(clauseTable, clauseTable[i][0])
                    #   Creates a new number_list from that new clause
                    newNumberList = number_list(newClauseTable)
                    return putnam_davis(newClauseTable, newOutput, newNumberList)
                elif clauseTable[i][0] < 0:
                    #   Adds false version of it to the OutPutTable
                    newOutput = output.copy()
                    newOutput[abs(clauseTable[i][0])] = "F"
                    newClauseTable = Deletion(clauseTable, clauseTable[i][0])
                    newNumberList = number_list(newClauseTable)
                    return putnam_davis(newClauseTable, newOutput, newNumberList)
        #   If this point is reached this means that there are no literals.
        #   In that case, the next atom in the number list will be set to False or to True.
        #   And Putnam Davis will be run on one of those two conditions
        # Iterates through our current number
        for i in numberList:
            #   This will be the new output for True
            newOutputTrue = output.copy()
            #   This will be the new output for False
            newOutputFalse = output.copy()
            #   Sets the atoms in the new output tables to either be true or false
            newOutputTrue[i] = "T"
            newOutputFalse[i] = "F"
            #   This will get the new clause tables through deletion
            #   By setting the atom to be true or false
            newClauseTableTrue = Deletion(clauseTable, i)
            newClauseTableFalse = Deletion(clauseTable, i * -1)
            #   This will get the new number lists for our new condition.
            #   The new Number lists will not contain the atom, but also
            #   possibly other numbers were deleted as a result of the deletion method.
            newNumberListTrue = number_list(newClauseTableTrue)
            newNumberListFalse = number_list(newClauseTableFalse)
            #   If setting the atom to True does not work then we will set it to
            #   False.
            #   If neither one works then we will get 0.
            if putnam_davis(newClauseTableTrue, newOutputTrue, newNumberListTrue) != 0:
                return putnam_davis(newClauseTableTrue, newOutputTrue, newNumberListTrue)
            elif putnam_davis(newClauseTableFalse, newOutputFalse, newNumberListFalse) != 0:
                return putnam_davis(newClauseTableFalse, newOutputFalse, newNumberListFalse)
        #   If we get to this point this means that
        #   throughout the entire number_list we could not find any combination of True and False that
        #   deleted each clause
        return 0


C1 = clause_maker("input")
outputC1 = {}
numberListC1 = number_list(C1)
print(C1)
print(Deletion(C1, -2))
print(numberListC1)
print(putnam_davis(C1, outputC1, numberListC1))
