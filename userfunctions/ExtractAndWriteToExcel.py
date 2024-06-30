import sys

from userfunctions import Extract_Patterns
import os, pandas as pa

#   Function name:ExtractJesLog
#   Author: venkanna gunaganti
#   Description:Extracting and writing to the Excel
#   How to invoke?:write_to_log_file(input_file_path,output_file_path)
#   Input parameters : input_file_path=path to the input file and
#                      output_file_path=path to the output file
#   Output parameters:returns 1 if success -1 for any failure
#   Date created: 30/08/2023
#   Date last modified & Changes done: 30/08/2023
def ExtractJesLog(input_file_path, output_file_path):
    '''this will take input and output file path as arguments and returns an integer values(1,-1)'''
    y = 1
    pattern1 = r'(?i)\bsysout id\b'
    pattern2 = r'(?i)\bgen\b'
    pattern3 = r'(?i)return-code'
    patterns = [pattern1, pattern2, pattern3]
    try:
        if  os.path.exists(input_file_path):

            Extract_Patterns.extract_info(input_file_path, 'new.txt', patterns)

            with open('new.txt', 'r') as f:
                data = f.read()
            lines = data.split('\n')
            filtered_lines = []
            x = True
            for i, line in enumerate(lines):
                if "SYSOUT ID" in line:
                    combined_line = [f"{lines[i]} //{lines[i + 1]}"]
                    if x:
                        filtered_lines.append(combined_line)
                        i += 1
                        # print(line)
                        x = False
                    elif not x:
                        i += 1
                        x = True
                elif "RETURN-CODE" in line:
                    filtered_lines.append(line)

            new_lst = []
            for item in filtered_lines:
                if type(item) == list:
                    for i in item:
                        listt = i.split('//')
                    for k in listt:
                        new_lst.append(k)

                else:
                    new_lst.append(item)

            with open('final.txt', 'w') as file:
                for line in new_lst:
                    file.write(line + '\n')
            with open('final.txt', 'r') as file:
                new_lines = file.read()

            new_dict_list = []

            found = True
            not_found = False
            row1 = not_found
            row2 = not_found
            row3 = not_found
            skip_line = 0
            i = 0
            new_lines = [lines for lines in new_lines.split('\n')]
            while i < len(new_lines):

                line = new_lines[i]

                if 'SYSOUT ID' in line:
                    sysout_id = line.split()[2]
                    job_name = line.split()[4]
                    print_date = line.split()[7]
                    archive_date = line.split()[10]
                    row1 = found

                if 'GEN' in line:
                    gen_id = line.split()[1]
                    job_id = line.split()[3]
                    print_time = line.split()[6]
                    archive_time = line.split()[9]

                    row2 = found
                    skip_line = 1
                if skip_line > 0:
                    i += 1
                    skip_line -= 1
                line = new_lines[i]
                if row1 and row2:
                    if 'RETURN-CODE' in line:
                        return_code = line.split()[2]
                        program_name = line.split()[0]

                    else:
                        return_code = None
                        program_name = None
                        i -= 1

                    row3 = found

                if row1 and row2 and row3:
                    keys = ['SYSOUT ID', 'JOBNAME', 'PRINT DATE', 'ARCHIVE DATE', 'GEN', 'JOBID', 'PRINT TIME',
                            'ARCHIVE TIME', 'RETURN-CODE', 'PROGRAM NAME']
                    values = [sysout_id, job_name, print_date, archive_date, gen_id,
                              job_id, print_time, archive_time, return_code, program_name]
                    pair = zip(keys, values)
                    dictionaries = dict(pair)

                    new_dict_list.append(dictionaries)
                    row1 = not_found
                    row2 = not_found
                    row3 = not_found
                i += 1

            df = pa.DataFrame(new_dict_list)
            path = output_file_path
            df.to_excel(path, index=False)
        else:
            print(f'{input_file_path} does not exists')
            y=-1

        
    except PermissionError as pe:
            print(f'{pe}:close the file ')

            y = -1

    return y
