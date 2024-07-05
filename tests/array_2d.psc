DECLARE array_2D: ARRAY[1:3, 1:3] OF INTEGER

DECLARE i, j, count: INTEGER

count <- 1

FOR i <- 1 TO 3
    FOR j <- 1 TO 3
        array_2D[i, j] <- count
        count <- count + 1
    NEXT j
NEXT i

FOR i <- 1 TO 3
    FOR j <- 1 TO 3
        OUTPUT array_2D[i, j]
    NEXT j
NEXT i
