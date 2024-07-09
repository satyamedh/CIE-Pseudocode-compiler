DECLARE numstr: STRING
INPUT numstr
DECLARE num: INTEGER
num <- STRING_TO_NUM(numstr)
num <- num + 1
numstr <- NUM_TO_STRING(num) & "1"
OUTPUT numstr





