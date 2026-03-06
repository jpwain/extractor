#!/usr/bin/env python3
import sys
import re
import argparse
import subprocess

def build_bookmarklet(input_file, copy_to_clipboard=False):
    # Try reading the input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{input_file}': {e}")
        sys.exit(1)

    # 1. Remove single-line comments (// ...)
    code = re.sub(r'//.*', '', code)
    
    # 2. Remove multi-line comments (/* ... */) if any exist
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    # 3. Strip leading/trailing whitespace from each line and remove newlines
    lines = [line.strip() for line in code.split('\n')]
    single_line_code = ''.join(lines)
    
    # Ensure it starts with the javascript: protocol
    if not single_line_code.startswith('javascript:'):
        single_line_code = 'javascript:' + single_line_code
        
    if copy_to_clipboard:
        # Copy to clipboard using pbcopy on macOS
        try:
            process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
            process.communicate(single_line_code.encode('utf-8'))
            
            # Check if pbcopy was successful
            if process.returncode == 0:
                print("Success: copied minified script to clipboard.")
            else:
                print(f"Error: pbcopy failed with exit code {process.returncode}")
                sys.exit(1)
        except FileNotFoundError:
             print("Error: 'pbcopy' command not found. Is this script running on macOS?")
             sys.exit(1)
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
            sys.exit(1)
    else:
        output_file = 'bookmarklet.txt'
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(single_line_code)
            print(f"Success: wrote minified script to {output_file}.")
        except PermissionError:
            print(f"Error: Permission denied when writing to '{output_file}'.")
            sys.exit(1)
        except Exception as e:
            print(f"Error writing to '{output_file}': {e}")
            sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Minify JS to a bookmarklet")
    parser.add_argument('input_file', nargs='?', default='extractor.js', help="Input JavaScript file")
    parser.add_argument('-c', '--copy', action='store_true', help="Copy the output to the clipboard instead of writing to file")
    
    args = parser.parse_args()
    build_bookmarklet(args.input_file, args.copy)
