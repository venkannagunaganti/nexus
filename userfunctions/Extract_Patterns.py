import re
import string


# ====================================================================================================================
# Function name: extract_info
# Author: Sneha Dalvi
# Description: Extracts lines from an input file that match any of the provided patterns and writes
#              them to an output file. If the output file already exists, it will be overwritten.
# Input Parameters: input_file (str) - The path to the input file from which lines will be extracted.
#                    patterns (list of str) - A list of patterns (regular expressions) to search for in the input file.
# Output Parameters:  output_file (str) - The path to the output file where matching lines will be written.
# How to invoke?:  CALL THIS Method ----- extract_info(input_file, output_file, patterns)
# Date created: 02/08/2023
# Date last modified & Changes done: 02/08/2023 - Initial version
# =================================================================================================================

def extract_info(input_file, output_file,patterns=r' '):
    try:
        printable_chars = set(string.printable)
        # Open & Read input file, Open & Write output file
        with open(input_file, 'r',errors='ignore') as infile, open(output_file, 'w') as outfile:

            for line in infile:
                line = line.replace('-', '')
                # line = line.replace('E', 'e')
                line = line.replace('~', '')
                line = line.replace('=', '')
                line = line.replace(r'ü|ä','')
                line=line.replace('*','')
                line = line.replace('', '')
                line=line.replace('','')
                cleaned_line = ''.join(char for char in line if char in printable_chars)
                for pattern in patterns:
                    if re.search(pattern, cleaned_line):
                        outfile.write(cleaned_line)
                        break
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' could not be found.")
    except FileNotFoundError:
        print(f"Error: The file '{output_file}' could not be found.")
    except Exception as e:
        print(f"An error occurred: {e}")


