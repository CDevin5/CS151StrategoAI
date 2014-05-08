i = open("randoTraining.txt")
o = open("randoTrainingGraphData.txt", 'w')

line = i.readline()

o.write("Games\t% won\n")

while line != '':
    if line[:6] == "Player":
        won = float((line[13:])[:-7])
        line = i.readline()
        lost = float((line[13:])[:-7])
        line = i.readline()
        timedout = float((line[15:])[:-1])
        total = won+lost+timedout
        o.write("%d\t\t%f\n"%(total, won/total))
    line = i.readline()

i.close()
o.close()
