DECLARE LineOfText: STRING
OPENFILE "FileA.txt" FOR READ
OPENFILE "FileB.txt" FOR WRITE
WHILE NOT EOF("FileA.txt")
    READFILE "FileA.txt", LineOfText
    WRITEFILE "FileB.txt", LineOfText
ENDWHILE
CLOSEFILE "FileA.txt"
CLOSEFILE "FileB.txt"
