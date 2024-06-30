DECLARE num: INTEGER
INPUT num
DECLARE count: INTEGER
count <- 0
FOR i <- 2 TO num DIV 2
    IF (num MOD i) = 0 THEN
        count <- count + 1
    ENDIF
NEXT i
IF count = 0 THEN
    OUTPUT "PRIME"
ELSE
    OUTPUT "NOT PRIME"
ENDIF


