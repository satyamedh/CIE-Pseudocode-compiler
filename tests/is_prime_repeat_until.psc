DECLARE num: INTEGER
DECLARE PRIME_FLAG: BOOLEAN

PRIME_FLAG <- TRUE
INPUT num

IF (num = 2) or (num = 1) THEN
    PRIME_FLAG <- FALSE
ENDIF

DECLARE i: INTEGER
i <- 2
REPEAT
    IF (num MOD i) = 0 THEN
        PRIME_FLAG <- FALSE
    ENDIF
    i <- i + 1
UNTIL (i >= num DIV 2) OR (PRIME_FLAG = FALSE)

IF PRIME_FLAG = TRUE THEN
    OUTPUT "PRIME"
ELSE
    OUTPUT "NOT PRIME"
ENDIF

