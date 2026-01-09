#taken from the essential algorithms for A level cs
def merge(list1, list2):
    newlist = []
    index1 = 0
    index2 = 0

    while index1 < len(list1) and index2 < len(list2):
        if list1[index1] < list2[index2]:
            newlist.append(list1[index1])
            index1 += 1
        
        elif list1[index1] > list2[index2]:
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

    for i in USlist:
        item = [i]
        newlist.append(item)


    while len(newlist) != 1:
        index = 0

        while index < len(newlist) - 1:
            mergedList = merge(newlist[index],newlist[index + 1])
            newlist[index] = mergedList

            del newlist[index + 1]
            index += 1
    
    return newlist