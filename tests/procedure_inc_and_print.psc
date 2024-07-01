PROCEDURE increment_and_print(number: INTEGER, by: INTEGER)
    OUTPUT number + by
ENDPROCEDURE

FOR i <- 1 TO 5
    CALL increment_and_print(i, 2)
NEXT i



