from parser import Parser
import argparse

def main():
    parser = argparse.ArgumentParser(description="VM Translator")
    parser.add_argument('--path', required=True, help="path of the VM file.")
    
    args = parser.parse_args()
    my_parser: Parser = Parser(args.path)
    
    

if __name__ == "__main__":
    main()