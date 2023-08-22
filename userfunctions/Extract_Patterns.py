import re


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

def extract_info(input_file, output_file, patterns):
    try:
        # Open & Read input file, Open & Write output file
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                for pattern in patterns:
                    if re.search(pattern, line):
                        outfile.write(line)
                        break
        print(f"Extraction complete. Results saved to '{output_file}'.")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' could not be found.")
    except Exception as e:
        print(f"An error occurred: {e}")


