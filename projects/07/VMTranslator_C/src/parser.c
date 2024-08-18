
#include "parser.h"

#define MAX_LENGTH_LINE 1024
#define MAX_LINES 2024

char current_command[MAX_LENGTH_LINE];
char total_lines[MAX_LINES][MAX_LENGTH_LINE];

void parse(const char *file_path) {
    FILE *input_file = fopen(file_path, "r");

    while (fgets(current_command, sizeof(current_command), input_file) != NULL) {

    }
}

bool hasMoreLines(void) {

}

#undef T