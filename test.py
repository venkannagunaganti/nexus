import os
import pandas as pa
from userfunctions import Extract_Patterns
#   Function name:Text_to_excel
#   Author: venkanna gunaganti
#   Description:Extracting and writing to the Excel
#   How to invoke?:text_to_excel(file_path)
#   Input parameters : input_file_path=path to the input file
#   Date created: 19/12/2023
#   Date last modified & Changes done: 19/12/2023
# file_path = 'C:/Users/vgunaganti/PycharmProjects/match/Jobs/ASP_Monitoring_sample_Job_J0110240_20231120.txt'
pattern_1 = r'(?i)\bsysout id\b'
pattern_2 = r'(?i)\bgen\b'
regex = r'.'
pattern3 = r'(?i)return-code:'
full_pattern = [pattern_1, pattern_2,pattern3]
def text_to_excel(file_path,sub_string):

  x=f"{file_path}"
  file_name=os.path.basename(file_path)
  file_name=file_name.split('.')
  file_name=file_name[0]
  try:
    global first_return_code_index
    Extract_Patterns.extract_info(file_path, 'new.txt', regex)
    Extract_Patterns.extract_info(file_path, 'new1.txt', full_pattern)
    with open('new1.txt', 'r') as s:
        sys_data = s.read()
    sys_data = sys_data.split('\n')

    sys_data = [element for element in sys_data if element != ""]
    with open('new.txt', 'r') as f:
        data = f.read()
    data = data.split('\n')

    first_return_code_available=True
    second_return_code_available = True
    return_code_indices = [i for i, sublist in enumerate(data) if "RETURNCODE:" in sublist]
    start_index = next((i for i, line in enumerate(data) if "GEN:" in line), None)+1
    if len(return_code_indices)==2:
     first_return_code_index=return_code_indices[0]
     second_return_code_index = return_code_indices[1]
     observation_1=data[start_index:first_return_code_index]
     observation_2=[line for line in data[first_return_code_index :second_return_code_index] if "RETURNCODE:" not in line]

    elif len(return_code_indices)==1:
        first_return_code_index=return_code_indices[0]
        first_return_code_available=False
        second_return_code_available=False
        observation_1=data[start_index:first_return_code_index]
        observation_2=data[first_return_code_index+1:]
    elif len(return_code_indices)==0:
        first_return_code_index=None
        second_return_code_index=None
        observation_1=data[start_index:]
        observation_2=None
    if observation_1=='':
        observation_1 =None
        # observation_1=None
    else:
        observation_1 = '\n'.join(observation_1)

    if observation_2==None:
        observation_2=None
    else:
     observation_2 = '\n'.join(observation_2)

    if observation_1!=None:
       observation_1=observation_1.replace('-','')
    if observation_2!=None:
       observation_2=observation_2.replace('-','')

    observations = []

    observations.append(observation_1)
    observations.append(observation_2)
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
    row3 = not_found
    gen_id = None
    job_id = None
    print_time = None
    return_code = None
    observation = None
    j = 0
    k = 0
    Nones=False
    if (observation_1==None or observation_1=='') and (observation_2==None or observation_2==''):
        observations=[]
        Nones=True
        j=-1
        k=-1
    if any((element ==  '') or( element is None) or (element=='\n\n') for element in observations) and len(return_line)<2:
        observations=[observation_1]
    if len(return_line) == 0:
        return_line = ['']
    if len(observations)>1 and len(return_line)<2:
        return_line.append('')
    s=0
    while j <len(return_line) or k <len(observations):
        i = 0
        if len(return_line) < 2:
            j = 0

        if len(observations) < 2:
            k = 0
        if s>1:
            break
        while i < len(sys_data) :
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
            if row1 and row2   :
                keys = ['SYSOUT ID', 'JOBNAME', 'PRINT DATE', 'ARCHIVE DATE', 'GEN Id', 'JOB ID', 'PRINT TIME',
                        'ARCHIVE TIME', 'RETURN-CODE', 'OBSERVATION']

                if len(observations)==0:
                  values = [sysout_id, job_name, print_date, archive_date, gen_id, job_id, print_time, archive_time,
                          return_line[s]]
                else:
                    values = [sysout_id, job_name, print_date, archive_date, gen_id, job_id, print_time, archive_time,
                              return_line[s],observations[k],file_path]

                pair = zip(keys, values)
                dictionaries = dict(pair)
                new_dict_list.append(dictionaries)
                row1 = not_found
                row2 = not_found
                row3 = not_found
            i += 1
        j += 1
        k += 1
        s+=1
    df = pa.DataFrame(new_dict_list)
    path = f'C:/Users/vgunaganti/PycharmProjects/match/{sub_string}.xlsx'
    if os.path.exists(path):
        existing_df = pa.read_excel(path)
        df = existing_df._append(df, ignore_index=True)
    df.replace('\x01', '', regex=True, inplace=True)
    df.to_excel(path, index=False)
  except PermissionError as pe:
      print(f'close the file {file_name}.xlsx ')

