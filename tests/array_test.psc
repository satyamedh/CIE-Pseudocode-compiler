DECLARE myArray: ARRAY[1:3] OF INTEGER

FOR i <- 1 TO 3
    DECLARE num: INTEGER
    INPUT num
    myArray[i] <- num
NEXT i

FOR i <- 1 TO 3
    OUTPUT myArray[4-i]
NEXT i



