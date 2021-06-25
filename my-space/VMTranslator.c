#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>

void err_mes() {
	printf("%s\n", strerror(errno));
	exit(1);
}


size_t getNumByteOfFile(FILE *fp) {
	size_t numByte;

	//get number of byte
	if(fseek(fp, 0, SEEK_END) != 0) {
		err_mes();
	}
	if(ftell(fp) == -1) {
		err_mes();
	}
	numByte = ftell(fp);

	//reset to the first offset
	fseek(fp, 0, SEEK_SET);
	return numByte;
}

int isBlankLine(char *line) {
	int res = 1; //true
	int len = strlen(line);
	for(int i = 0; i < len; i++) {
		char character = *(line+i);
		if(i != len-1 && character != ' ' && character != '\t') {
			res = 0; //false
			break;
		}
	}
	return res;
}

char *removeCommentInLine(char *line, int isLastLine) {
	char *res;
	if(line != NULL) {
		size_t length = strlen(line) + 1;
		int hasComment = 0; //false
		size_t buf_size = 0;
		size_t i;
		for(i = 0; i < length; i++) {
			if(*(line+i) == '/' && *(line+i+1) == '/') {
				hasComment = 1; //true
				break;
			}	
		}
		buf_size = i;
		res = (char*)calloc(buf_size, sizeof(char));
		memcpy(res, line, buf_size);
		if(hasComment) {
			//remove blank before comment
			int j;
			for(j = buf_size-1; j >= 0; j--) {
				char character = *(res+j);
				if(character != ' ' || character != '\t')
					break;
			}
			if(isLastLine) {
				*(res + j) = '\0';
			} else {
				*(res + j) = '\n';
				*(res + j + 1) = '\0';
			}
		}
	}
	return res;
}

void parseVMFile(FILE *fp) {
	FILE *outFile = fopen("parseVMfile.txt", "w");
	size_t total_byte = getNumByteOfFile(fp);
	size_t file_size_allocate = total_byte + 1;
	char *buffer = (char *)calloc(file_size_allocate, sizeof(char));
	
	while(fgets(buffer, file_size_allocate, fp)) {
		if(buffer != NULL) {
			int isLastLine = 0;
			int cur_offset = ftell(fp);
			int checkLastLine = cur_offset + 1; //plus 1 because file_size_allocate = total_byte + 1
			if(checkLastLine == file_size_allocate)
				isLastLine = 1;
			if((*(buffer) == '/' && *(buffer+1) == '/') || isBlankLine(buffer))
				continue;
			char *res = removeCommentInLine(buffer, isLastLine);
			fwrite(res, sizeof(char), strlen(res), outFile);
		}
	}
	free(buffer);
	fclose(outFile);
}

int main(int argc, char *argv[]) {
	if (argc != 2) {
		printf("Usage: VMTranslator <file>");
		return 1;
	}
	FILE *fp;
	fp = fopen(argv[1], "r");
	if(fp == NULL) {
		printf("Cannot open file");
		return 1;
	}
	if(getNumByteOfFile(fp) > 0) //avoid empty file
		parseVMFile(fp);
	fclose(fp);

	return 0;
}