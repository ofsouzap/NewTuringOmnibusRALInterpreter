from typing import List as tList;
from typing import Tuple as tTuple;
from typing import Dict as tDict;
import argparse;

def read_all_from_mem(m: tDict[int, int]) -> tList[int]:

    end = max(m.keys());

    out = [];

    for i in range(end + 1):
        out.append(get_from_mem(m, i));

    return out;

def get_from_mem(m: tDict[int, int], i: int) -> int:
    
    if i in m.keys():
        return m[i];
    else:
        return 0;

def run(prog: tList[tTuple[str, int]], init_mem: tDict[int, int]) -> tDict[int, int]:
    
    mem = dict(init_mem);
    ac = 0;

    head = 0;

    running = True;

    while running:

        ins, arg = prog[head];
        head += 1;
        ins = ins.upper();

        assert type(ins) == str, "Instructions should all be strings";
        assert type(arg) == int, "Arguments should all be integers";

        if ins == "LDA":
           ac = get_from_mem(mem, arg);
           
        elif ins == "LDI":
            ac = get_from_mem(mem, get_from_mem(mem, arg));
            
        elif ins == "STA":
            mem[arg] = ac;
            
        elif ins == "STI":
            mem[get_from_mem(mem, arg)] = ac;
            
        elif ins == "ADD":
            ac += get_from_mem(mem, arg);
            
        elif ins == "SUB":
            ac -= get_from_mem(mem, arg);

        elif ins == "JMP":
            head = arg;

        elif ins == "JMZ":
            if ac == 0:
                head = arg;

        elif ins == "HLT":
            running = False;

        elif ins != "PAS":
            raise Exception("Invalid instruction: " + ins);

    return mem;

def parse_prog(s: str) -> tList[tTuple[str, int]]:

    prog = [];

    lines = s.strip("\n").split("\n");

    for line in lines:

        # Comments
        if "/" in line:
            line = line.split("/")[0].strip();

        parts = line.strip(" ").split(" ");

        n = None;
        ins = None;
        arg = None;

        if len(parts) < 1:
            raise Exception("Invalid instruction line: " + line);

        n = int(parts[0]);
        ins = parts[1];

        if len(parts) > 2:
            arg = int(parts[2]);
        else:
            arg = 0;

        assert n >= 0;
        assert arg >= 0;

        while n > len(prog) - 1:
            prog.append(("PAS", 0));

        prog[n] = (ins, arg);

    return prog;

def load_prog_file(filename: str) -> tList[tTuple[str, int]]:

    prog_string = None;

    with open(filename, "r") as file:
        prog_string = file.read();

    return parse_prog(prog_string);

def parse_init_mem(s: str) -> tDict[int, int]:

    mem = {};

    lines = s.strip("\n").split("\n");

    for line in lines:

        # Comments
        if "/" in line:
            line = line.split("/")[0];

        parts = line.strip(" ").split(" ");

        if len(parts) < 2:
            raise Exception("Invalid memory line: " + line);

        n = int(parts[0]);
        v = int(parts[1]);

        mem[n] = v;

    return mem;

def load_init_mem_file(filename: str) -> tDict[int, int]:

    init_string = None;

    with open(filename, "r") as file:
        init_string = file.read().strip();

    return parse_init_mem(init_string);

def main():

    prog = None;
    init_mem = None;

    # Argument parsing

    arg_parser = argparse.ArgumentParser(description="Run a RAL program");

    arg_parser.add_argument("-p", "--prog",
                            type = str,
                            help = "Filename of program file");

    arg_parser.add_argument("-m", "--mem",
                            type = str,
                            help = "Filename of initial memory file");

    args = arg_parser.parse_args();

    if args.prog == None: # Input program

        print("""Select program input type:
0) Console
1) File""");

        prog_inp_opt = input("$> ");

        if prog_inp_opt =="0":

            print("Start program below:");
            lines = [];

            while True:
                l = input();
                if l == "":
                    break;
                else:
                    lines.append(l);

            prog = parse_prog("\n".join(lines));

        elif prog_inp_opt == "1":

            filename = input("Filename> ");
            prog = load_prog_file(filename);

        else:
            raise Exception("Invalid option");

    else: # Program file as argument

        prog = load_prog_file(args.prog);

    if args.mem == None: # Input initial memory

        print("""Select initial memory input type:
0) Console
1) File""");

        init_inp_opt = input("$> ");

        if init_inp_opt == "0":

            mem_inp = input("Memory Values (separate by commas):\n");

            init_mem_list = [int(x) for x in mem_inp.split(",")];
            
            init_mem = {};
            
            for i in range(len(init_mem_list)):
                init_mem[i] = init_mem_list[i];

        elif init_inp_opt == "1":

            filename = input("Filename> ");
            init_mem = load_init_mem_file(filename);

        else:
            raise Exception("Invalid option");

    else: # Initial memory as argument

        init_mem = load_init_mem_file(args.mem);

    # Running program

    mem_end = run(prog, init_mem);

    # Output

    print("Program complete.");
    print("Final memory state:");

    out = read_all_from_mem(mem_end);

    for i in range(len(out)):
        print(i, out[i]);

if __name__ == "__main__":
    main();
