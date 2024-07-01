DECLARE Distance : INTEGER
INPUT Distance

FUNCTION Max(Number1 : INTEGER, Number2 : INTEGER) RETURNS INTEGER
    IF Number1 > Number2 THEN
        RETURN Number1
    ELSE
        RETURN Number2
    ENDIF
ENDFUNCTION
OUTPUT Max(10, Distance*2)
