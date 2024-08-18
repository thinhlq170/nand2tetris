#ifndef ENUM_COMMAND_TYPE_H
#define ENUM_COMMAND_TYPE_H

enum Command_Type {
    C_ARITHMETIC,
    C_PUSH,
    C_POP,
    C_LABEL,
    C_GOTO,
    C_IF,
    C_FUNCTION,
    C_RETURN,
    C_CALL
};

typedef enum Command_Type Command_Type;

#endif