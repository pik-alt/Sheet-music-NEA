from noteclass import Note


#taken from the essential algorithms for A level cs
def merge(list1, list2):

    newlist = []

    index1 = 0
    index2 = 0


    while index1 < len(list1) and index2 < len(list2):
        if list1[index1].outputX_POS() < list2[index2].outputX_POS():
            newlist.append(list1[index1])
            index1 += 1
        
        elif list1[index1].outputX_POS() > list2[index2].outputX_POS():
            newlist.append(list2[index2])
            index2 += 1
        
        else:
            newlist.append(list1[index1])
            newlist.append(list2[index2])
            index1 += 1
            index2 += 1
    
    if index1 < len(list1):
        for i in range(index1, len(list1)):
            newlist.append(list1[i])
    
    else:
        for i in range(index2, len(list2)):
            newlist.append(list2[i])

    return newlist



def mergeSort(USlist):
    newlist = []

    #Adds every element in US list into it's own list in newlist[]
    for i in USlist:
        item = [i]
        newlist.append(item)

    #keep going while there's still things to be merged
    while len(newlist) != 1:
        index = 0

        while index < len(newlist) - 1:
            mergedList = merge(newlist[index],newlist[index + 1])
            newlist[index] = mergedList

            del newlist[index + 1]
            index += 1
    
    return newlist



def linearSearch(self, wantedItem, list):
    found = False
    index = 0
    #Item will always be in the array, we don't need a condition if index > len(list)
    while found != True:
        if list[index].outputID() == wantedItem:
            found = True
            return index
        else: index += 1




#taken from "Essential Algorithms for A level Computer Science"
def binarySearch(itemToFind, list, functionCalled):

    functionCalled

    found = False
    
    first = 0

    last = len(list) - 1
    while first <= last and not found:
        midpoint = (first+last) // 2

        if functionCalled(list[midpoint]) == itemToFind:
            found = True
            return midpoint
        
        else:
            if functionCalled(list[midpoint]) < itemToFind:
                first = midpoint + 1
            
            else:
                last = midpoint - 1
    