import sys

def run(src):
    print(src)
    print("Scanner Not Implemented")

def open_file(name):
    file = open(name, "r")
    src = file.read()
    file.close()
    run(src)

def run_prompt():
    while True:
        l = input("> ")
        run(l)

def main():
    if len(sys.argv) > 2:
        print("Usage: python main.py [script]")
    elif len(sys.argv) == 2:
        open_file(sys.argv[1])
    else:
        run_prompt()

main()


