#ifndef PARSER_INCLUDED
#define PARSER_INCLUDED

#include <stdbool.h>
#include <stdio.h>
#include "enum_command_type.h"


/**
 * Opens the input stream file, and gets ready to parse it.
 * @param file_path the input file path
 * @return the Parser object
 */
extern void parse(char *file_path);

/**
 * Are there more lines in the input
 * @param void
 * @return true if there are more lines in the input and otherwise
 */
extern bool hasMoreLines(void);

/**
 * Reads the next command from the input and makes it the current command.
 * This routine should be called only if hasMoreLines is true.
 * Initially there is no current command.
 * 
 * @param void
 * @return void
 */
extern void advance(void);

/**
 * Returns a constant representing the type of the current command.
 * If the current command is an arithmetic-logical command, returns C_ARITHMETIC.
 * 
 * @param empty
 * @return a command type enum
 */
extern Command_Type commandType(void);

/**
 * Returns the first argument of the current command.
 * In the case of C_ARITHMETIC, the command itself (add, sub, etc.) is returned.
 * Should not be called if the current command is C_RETURN.
 * 
 */
extern char* arg1(void);

/**
 * Returns the second argument of the current command.
 * Should be called only if the current command is C_PUSH, C_POP,
 * C_FUNCTION, or C_CALL.
 */
extern int arg2(void);

#endif