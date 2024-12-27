import re

def detect_function_prologue(line):
    """Detect function prologues (common ones) like push, mov, etc."""
    # Prologue examples: push, mov, sub, etc.
    prologue_patterns = [
        r"^\s*push\s+%rbp",      # push %rbp
        r"^\s*mov\s+%rsp,\s+%rbp",  # mov %rsp, %rbp
        r"^\s*sub\s+.*\s+%rsp"   # sub to adjust stack
    ]
    
    for pattern in prologue_patterns:
        if re.match(pattern, line):
            return True
    return False

def detect_function_epilogue(line):
    """Detect function epilogues like ret, pop %rbp."""
    epilogue_patterns = [
        r"^\s*pop\s+%rbp",       # pop %rbp
        r"^\s*ret"               # ret
    ]
    
    for pattern in epilogue_patterns:
        if re.match(pattern, line):
            return True
    return False

def detect_function(file_path):
    """Detect all functions in the given assembly file."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    functions = []
    in_function = False
    function_start_line = None
    
    for i, line in enumerate(lines):
        # Detect function label (start)
        if line.strip().endswith(":") and not in_function:
            # A label is detected (potential function entry point)
            in_function = True
            function_start_line = i
            continue
        
        # Detect function prologue
        if in_function and detect_function_prologue(line):
            continue
        
        # Detect function epilogue
        if in_function and detect_function_epilogue(line):
            # Function ends here
            functions.append((function_start_line + 1, i + 1))  # Lines are 1-indexed
            in_function = False
    
    return functions

def main():
    """Main function to prompt user input and analyze the assembly file."""
    file_path = input("Enter the path to the assembly source file (.s): ")
    
    try:
        functions = detect_function(file_path)
        
        if functions:
            print(f"\nDetected functions in {file_path}:")
            for start, end in functions:
                print(f"Function starts at line {start} and ends at line {end}")
        else:
            print("No functions detected.")
    
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
