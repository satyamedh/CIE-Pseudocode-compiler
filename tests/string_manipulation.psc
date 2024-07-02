DECLARE myString: STRING
INPUT myString

IF LENGTH(myString) <= 5 THEN
    OUTPUT "Too short"
ELSE
    OUTPUT RIGHT(myString, 2) & LEFT(myString, 2) & MID(myString, 3, 1)
ENDIF



