DECLARE num: INTEGER
DECLARE PRIME_FLAG: BOOLEAN

PRIME_FLAG <- TRUE
INPUT num

IF (num = 2) OR (num = 1) THEN
    PRIME_FLAG <- TRUE
ELSE
    DECLARE i: INTEGER
    i <- 2
    REPEAT
        IF (num MOD i) = 0 THEN
            PRIME_FLAG <- FALSE
        ENDIF
        i <- i + 1
    UNTIL (i >= num DIV 2) OR (PRIME_FLAG = FALSE)
ENDIF
IF PRIME_FLAG = TRUE THEN
    OUTPUT "PRIME"
ELSE
    OUTPUT "NOT PRIME"
ENDIF


