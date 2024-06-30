import os
import re
import pandas as pa
from userfunctions import Extract_Patterns
from Text_to_Excel import text_to_excel
#   Function name:main
#   Author: venkanna gunaganti
#   Description:Extracting and writing to the Excel
#   How to invoke?:main(job_name,folder_path)
#   Input parameters : job_name and folder_path
#   Date created: 19/12/2023
#   Date last modified & Changes done: 19/12/2023
folder_path = '/Users/Developer/python projects/match/Jobs'
file_name_to_match = 'ASP_Monitoring_P0_Job_J0055107 _20231120_13.txt'
app_name = "bvj"
pattern_1 = r'(?i)\bsysout id\b'
pattern_2 = r'(?i)\bgen\b'
regex = r'.'
pattern3 = r'(?i)return-code:'
full_pattern = [pattern_1, pattern_2,pattern3]

def sys_to_excel(app_name, folder_path, verbose=False, count=False):
    '''app_name= name of the app,folder_path=where all files are located'''
    x=[]
    df=pa.DataFrame(x)
    p1 = os.path.join(os.getcwd() + '/temp', 'text1.txt')
    p2 = os.path.join(os.getcwd() + '/temp', 'text2.txt')
    path = os.path.join(os.getcwd()+'/Jobs', f'{app_name}.xlsx')
    if os.path.exists(path):
        os.remove(path)
    app_name=app_name.lower()
    l = []
    files = []
    for file in os.listdir(folder_path):
        files.append(file)
    pattern = re.compile(re.escape(app_name))
    files_data = []
    c=0
    for f in files:
        new_dict_list = []

        f=f.lower()
        if pattern.search(f):
            c+=1
            file_path = os.path.join(folder_path, f)
            file =os.path.basename(file_path)
            if 'dnf' not in file:
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


                        found = True
                        not_found = False
                        row1 = not_found
                        row2 = not_found
                        j = 0
                        k = 0

                        gdg = []
                        for obs in observations:
                            if 'GDG:' in obs:
                                gdg.append(obs)
                        gdg = '\n'.join(gdg)
                        if observations and (isinstance(observations[-1], list) and not observations[-1]) or (
                                isinstance(observations[-1], str) and not observations[-1].strip()) or (
                                'GDG:' in str(observations[-1])):
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
                                    keys = ['SYSOUT ID', 'JOBNAME', 'PRINT DATE', 'ARCHIVE DATE', 'GEN Id', 'JOB ID',
                                            'PRINT TIME',
                                            'ARCHIVE TIME', 'RETURN-CODE', 'OBSERVATION', 'GDG']

                                    if len(observations) == 0:
                                        values = [sysout_id, job_name, print_date, archive_date, gen_id, job_id, print_time,
                                                  archive_time,
                                                  return_line[s], gdg]
                                    else:
                                        values = [sysout_id, job_name, print_date, archive_date, gen_id, job_id, print_time,
                                                  archive_time,
                                                  return_line[s], observations[k], gdg]

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
                        # path = os.getcwd()+'\Jobs' + {app_name}.xlsx'
                        if os.path.exists(path):
                            existing_df = pa.read_excel(path)
                            df = existing_df._append(df,ignore_index=True)
                            # df = pa.concat([existing_df, df], ignore_index=True)
                        df.replace('\x01', '', regex=True, inplace=True)
                        df.to_excel(path, sheet_name='sys',index=False)




    return df
def dnf_to_excel(app_name,folder_path):
    '''app_name= name of the app,folder_path=where all files are located'''

    x=[]
    df=pa.DataFrame(x)
    path = os.path.join(os.getcwd()+'/Jobs', f'{app_name}.xlsx')

    if os.path.exists(path):
        os.remove(path)
    app_name=app_name.lower()
    l = []
    files = []
    for file in os.listdir(folder_path):
        files.append(file)
    pattern = re.compile(re.escape(app_name))
    files_data = []
    c=0
    for f in files:
        new_dict=[]
        f=f.lower()
        if pattern.search(f):
            file_path = os.path.join(folder_path, f)
            file=os.path.basename(file_path)
            if 'dnf' in file:


                with open(file_path, 'r',errors='ignore') as f:
                    data = f.read()
                data=data.split('\n')

                keys=[]
                data = [item for item in data if item != '']
                for d in data :
                    values=[]
                    pairs=d.split()
                    pairs=pairs[3:]
                    for pair in pairs:
                        k,v=pair.split('=')


                        values.append(v)
                        if len(values)==3:
                            keys=['Observation','Id','DDName','DDlist']
                            values=['Data not found',values[0],values[1],values[2]]

                    pair = zip(keys, values)
                    dictionaries = dict(pair)
                    new_dict.append(dictionaries)

                df = pa.DataFrame(new_dict)

                path = os.path.join(os.getcwd()+'/Jobs', f'{app_name}.xlsx')
                if os.path.exists(path):
                            existing_df = pa.read_excel(path)
                            df = existing_df._append(df,ignore_index=True)
                df.replace('\x01', '', regex=True, inplace=True)
                df.to_excel(path,sheet_name='dnf', engine='openpyxl',index=False)



    return df

def main(app_name, folder_path,choice=3):
    '''app_name= name of the app,folder_path=where all files are located,choice=1 for sys data,choice=2 for dnf and for both optional'''

    if choice==1:
        sys_to_excel(app_name,folder_path)
    elif choice==2:
        dnf_to_excel(app_name,folder_path)
    else:
        sys_df = sys_to_excel(app_name, folder_path, verbose=False, count=False)
        dnf_df = dnf_to_excel(app_name, folder_path)

        path = os.path.join(os.getcwd(), 'Jobs', f'{app_name}.xlsx')
        with pa.ExcelWriter(path, engine='openpyxl') as writer:
               sys_df.to_excel(writer, sheet_name='sys', index=False)

               dnf_df.to_excel(writer, sheet_name='dnf', index=False)

main(app_name,folder_path)
# sys_to_excel(app_name,folder_path)
# dnf_to_excel(app_name,folder_path)
