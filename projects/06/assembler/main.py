from assembler import Parser, Code, SymbolTable
import argparse

def main():
    parser = argparse.ArgumentParser(description="HACK Assembler")
    parser.add_argument('--path', required=True, help="path of the assembly file.")
    
    args = parser.parse_args()
    Parser(args.path)
    
    

if __name__ == "__main__":
    main()