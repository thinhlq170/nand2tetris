#ifndef CODE_WRITER_H
#define CODE_WRITER_H

#include <stdio.h>
#include "enum_command_type.h"

#define T Code_Writer
typedef struct T *T;

/**
 * Opens an output stream and gets ready to write into it
 */
extern T Code_Writer_new(FILE *outputFileStream);

/**
 * Writes to the output file the assembly code that implements the given arithmetic-logic
 * command.
 */
extern void writeArithmetic(char *command);

/**
 * Writes to the output file the assembly code that implements
 * the given push or pop command
 */
extern void writePushPop(Command_Type commandType, char* segment, unsigned int index);


#undef T
#endif
