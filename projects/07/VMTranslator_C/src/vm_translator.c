#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
// #include "code_writer.h"
// #include "parser.h"

int validate_file_path(const char*);

int main(int argc, char **argv) {

    const char *file_path;
    file_path = argv[1];

    if (validate_file_path(file_path)) {
        FILE *input_file = fopen(file_path, "r");
        
    }


    

    return 0;
}

int validate_file_path(const char *path) {
    // Check if the file exists
    if (access(path, F_OK) == 0) {
        return 1; // the file does exist
    } else {
        fprintf(stderr, "'%s': %s\n", path, strerror(errno));
        return 0;
    }
}
