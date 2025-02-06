# Simulated Processor

## Description
This project implements a **simulated processor** in Python, capable of interpreting and executing a set of instructions defined in an input file. The processor includes registers, memory, and a stack for storing temporary values.

## Features
- Support for arithmetic operations: `add`, `addi`, `sub`, `subi`, `mul`, `div`
- Flow control: `blt`, `bgt`, `beq`, `j`, `jr`, `jal`
- Memory manipulation: `lw`, `sw`
- Data movement: `mov`, `movi`, `backup`
- Simulation of a set of registers and a stack

## Code Structure
The main code is in the `Processor` class, which performs:
1. **Initialization**: Loads instructions from a file.
2. **Execution**: Processes instructions line by line and executes the corresponding operations.
3. **Registers and Memory**: Displays the state of registers and memory after each instruction.

## How to Use
Save the instructions in a text file (e.g., `add_mov.txt`) and run the following command:
```bash
python processor.py
```

## Example Input (`add_mov.txt`)
```
addi r1, r0, 5
mov r2, r1
mul r3, r1, r2
sw r3, 0(r0)
```
