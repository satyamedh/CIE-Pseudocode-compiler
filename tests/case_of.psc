DECLARE Move: CHAR
INPUT Move
DECLARE PosX: INTEGER
DECLARE PosY: INTEGER

CASE OF Move
    'W': OUTPUT "F"
        PosY <- PosY + 1
    'A': OUTPUT "L"
        PosX <- PosX - 1
    'S': OUTPUT "B"
        PosY <- PosY - 1
    'D': OUTPUT "R"
        PosX <- PosX + 1
    OTHERWISE: OUTPUT "Invalid Move"
ENDCASE
OUTPUT PosX, PosY

