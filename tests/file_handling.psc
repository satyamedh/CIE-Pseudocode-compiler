OPENFILE "FileA.txt" FOR READ

DECLARE LineOfText: STRING

WHILE NOT EOF("FileA.txt")
    READFILE "FileA.txt", LineOfText
    OUTPUT LineOfText
ENDWHILE
CLOSEFILE "FileA.txt"
