listTest = [[1,"hello"],[2,"goodbye"]]

for i in range(0, len(listTest)):
    if listTest[i-1][0] == 1:
        print("found")
        del listTest[i-1]


print(listTest)