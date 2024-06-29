# CIE Pseudo-Code Compiler

This is a pseudo-code compiler for the CIE IGCSE and AS&A Levels Computer Science course. It is designed to be used with 0478/9718/9708.

I am using the official CIE pseudo-code specification as a reference for this compiler. You can find the specification [here](https://www.cambridgeinternational.org/Images/697401-2026-syllabus-legacy-notice.pdf).

## Small rant
WHY IS IT CALLED PSEUDOCODE IF IT CAN BE COMPILED? IT'S NOT PSEUDOCODE IF IT CAN BE COMPILED. IT'S A REAL PROGRAMMING LANGUAGE. IT'S NOT PSEUDO.

## How does it work?
The compiler is not exactly a compiler, I am using `ply` (Python Lex-Yacc) to parse the pseudo-code and convert it to an abstract syntax tree (AST).
I then use the AST to generate C++ code, and call `g++` to compile the generated C++ code.

## Requirements
- Python 3
- gcc (for compiling the generated C++ code)

## Limitations (for now)
- Only supports integer data types for now
- Barely any part of the actual CIE pseudo-code is implemented




