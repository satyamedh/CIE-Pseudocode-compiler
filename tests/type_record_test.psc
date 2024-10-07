TYPE StudentRecord
    DECLARE LastName : STRING
    DECLARE FirstName : STRING
    DECLARE YearGroup : INTEGER
    DECLARE FormGroup : CHAR
ENDTYPE

DECLARE Pupil1 : StudentRecord
DECLARE Pupil2 : StudentRecord
DECLARE Pupils : ARRAY[1:30] OF StudentRecord

Pupil1.LastName <- "Johnson"
Pupil1.FirstName <- "Leroy"
Pupil1.YearGroup <- 6
Pupil1.FormGroup <- 'A'

Pupil2 <- Pupil1

FOR i <- 1 TO 30
    Pupils[i].YearGroup <- Pupils[i].YearGroup + 1
NEXT i

OUTPUT Pupil1.LastName, Pupil1.FirstName, Pupil1.YearGroup, Pupil1.FormGroup



