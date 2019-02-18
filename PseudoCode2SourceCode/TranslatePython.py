import sys
import os

arg = sys.argv

language = arg[2]

f = open(arg[1], 'r')
lines = f.readlines()

if arg[2] == 'Python':
    c = open('sample.pcp', 'r')
elif arg[2] == 'R':
    c = open('sample.pcr', 'r')

statements = c.readlines()

outputFName = arg[1].split('.')

o = open(outputFName[0]+'Complete.'+outputFName[1], 'w+')

for line in lines:
    stmtCount = 0
    for stmt in statements:
        fw = stmt.split(' ', 1)[0]
        #  MULTILINE TRANSLATION
        if fw == '#' or fw == '$':
            stmt = stmt.split(' ', 1)[1]
            compoundStmt = []
            if line == stmt:
                # print(stmt)
                compoundStmt.append(line)
                prevcount = stmtCount - 1
                while True:
                    prevstmt = statements[prevcount]
                    fwpr = prevstmt.split(' ', 1)[0]
                    if fwpr == '#' or fwpr == '$':
                        prevstmt = prevstmt.split(' ', 1)[1]
                        compoundStmt.append(prevstmt)
                        prevcount = prevcount - 1
                    else:
                        break

                compoundStmt.reverse()

                follcount = stmtCount + 1
                while True:
                    follstmt = statements[follcount]
                    fwfl = follstmt.split(' ', 1)[0]
                    if fwfl == '#' or fwfl == '$':
                        follstmt = follstmt.split(' ', 1)[1]
                        compoundStmt.append(follstmt)
                        follcount = follcount + 1
                    else:
                        break

                compoundStmt.reverse()

                while True:
                    o.write(compoundStmt.pop())
                    if len(compoundStmt) == 0:
                        break

                break
        #  SINGLE LINE TRANSLATION
        else:
            if line == stmt:
                # WRITE PSEUDOCODE LINE TO INTERMEDIATE OUTPUT
                o.write(stmt)
                # print(stmt)
                break
        stmtCount = stmtCount + 1


f.close()
c.close()
o.close()

# translation = open(outputFName[0]+'Translated.'+outputFName[1], 'w+')

# if os.path.isfile(outputFName[0]+'Complete.'+outputFName[1]):
    # CALL THE TRANSLATION MODEL TO TRANSLATE THE COMPLETED PSEUDOCODE FILE.

# translation.close()

print('finished')