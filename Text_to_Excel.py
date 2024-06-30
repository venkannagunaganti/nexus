import encodings
import os
import pandas as pa
from userfunctions import Extract_Patterns

#   Function name:Text_to_excel
#   Author: venkanna gunaganti
#   Description:Extracting and writing to the Excel
#   How to invoke?:text_to_excel(job-name,file_path)
#   Input parameters : input_file_path=path to the input file,job_name
#   Date created: 19/12/2023
#   Date last modified & Changes done: 19/12/2023
pattern_1 = r'(?i)\bsysout id\b'
pattern_2 = r'(?i)\bgen\b'
regex = r'.'
pattern3 = r'(?i)return-code:'
full_pattern = [pattern_1, pattern_2,pattern3]


def text_to_excel(app_name, file_path):
    p1=os.path.join(os.getcwd()+'\\temp','text1.txt')
    p2=os.path.join(os.getcwd()+'\\temp','text2.txt')
    try:
        global first_return_code_index
        Extract_Patterns.extract_info(file_path, p1, full_pattern)
        Extract_Patterns.extract_info(file_path, p2, regex)
        with open(p1, 'r') as s:
            sys_data = s.read()
        sys_data = sys_data.split('\n')
        sys_data = [element for element in sys_data if element != ""]
        with open(p2, 'r') as f:
            data = f.read()
        data = data.split('\n')
        first_return_code_available = True
        second_return_code_available = True
        return_code_indices = [i for i, sublist in enumerate(data) if "RETURNCODE:" in sublist]
        start_index = next((i for i, line in enumerate(data) if "GEN:" in line), None) + 1

        observations = []
        if len(return_code_indices) > 0:
            first_return_code_index = return_code_indices[0]
            observations.append(data[start_index:first_return_code_index])

            for i in range(len(return_code_indices) - 1):
                current_return_code_index = return_code_indices[i]
                next_return_code_index = return_code_indices[i + 1]

                observation = [line for line in data[current_return_code_index + 1:next_return_code_index] if
                               "RETURNCODE:" not in line]
                observations.append(observation)

            last_return_code_index = return_code_indices[-1]
            observations.append(data[last_return_code_index + 1:])

        else:
            first_return_code_index = None

            observations.append(data[start_index:])
        observations = ['\n'.join(inner_list) if inner_list else inner_list for inner_list in observations]
        data = [line for line in data]
        # data='\n'.join(data)
        return_line = []
        for line in data:
            if 'RETURNCODE' in line:
                return_line.append(line)
        new_dict_list = []

        found = True
        not_found = False
        row1 = not_found
        row2 = not_found
        j = 0
        k = 0




        gdg=[]
        for obs in observations:
            if 'GDG:' in obs:
                print(obs)
                gdg.append(obs)
        gdg='\n'.join(gdg)
        if observations and (isinstance(observations[-1], list) and not observations[-1]) or (
                isinstance(observations[-1], str) and not observations[-1].strip())or ('GDG:' in str(observations[-1])):
            observations.pop()


        if len(observations) > len(return_line):
            i = len(observations) - len(return_line)
            for x in range(0, i):
                return_line.append('')

        if len(return_line) > len(observations):
            i = len(return_line) - len(observations)
            for x in range(0, i):
                observations.append('')
        if len(return_line) == 0 and len(observations) == 0:
            k = -1

            return_line.append('')

        observations = [item if item != [] else '' for item in observations]

        print(len(return_line),len(observations))
        s = 0
        while j < len(return_line) or k < len(observations):
            i = 0

            if k == -1:
                s = 0

            while i < len(sys_data):
                line = sys_data[i]
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

                if row1 and row2:
                    keys = ['SYSOUT ID', 'JOBNAME', 'PRINT DATE', 'ARCHIVE DATE', 'GEN Id', 'JOB ID', 'PRINT TIME',
                            'ARCHIVE TIME', 'RETURN-CODE', 'OBSERVATION','GDG']

                    if len(observations) == 0:
                        values = [sysout_id, job_name, print_date, archive_date, gen_id, job_id, print_time,
                                  archive_time,
                                  return_line[s],gdg]
                    else:
                        values = [sysout_id, job_name, print_date, archive_date, gen_id, job_id, print_time,
                                  archive_time,
                                  return_line[s], observations[k],gdg]

                    pair = zip(keys, values)
                    dictionaries = dict(pair)
                    new_dict_list.append(dictionaries)
                    row1 = not_found
                    row2 = not_found
                    row3 = not_found
                i += 1
            j += 1
            k += 1
            s += 1

        df = pa.DataFrame(new_dict_list)
        path = f'C:/Users/vgunaganti/PycharmProjects/match/Jobs/{app_name}.xlsx'
        if os.path.exists(path):
            existing_df = pa.read_excel(path)
            df = existing_df._append(df, ignore_index=True)
        df.replace('\x01', '', regex=True, inplace=True)
        df.to_excel(path, index=False)
    except PermissionError as pe:
        print(f'close the file {app_name}.xlsx ')

