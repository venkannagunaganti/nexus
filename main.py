import re
import re
import openpyxl
from userfunctions import Extract_Patterns
file = open('J0032069.x', errors='ignore')

# file.close()
pattern1 = r'(?i)\bsysout id\b'
pattern2 = r'(?i)\bgen\b'
pattern3 = r'(?i)return-code'
def string_search():
    output = ''
    for line in file:
        line_1 = re.search(pattern1, line)
        line_2 = re.search(pattern2, line)
        line_3 = re.search(pattern3, line)
        line = re.sub(r'\*?', '', line)
        re.split(r'\s*:\s*', line)
        if line_1 or line_2  :
            output+=line

    return output


raw_lines = string_search()
with open('file.txt','w') as f:
    f.write(raw_lines)




with open('file.txt','r') as f:
    data=f.read()
lines = data.strip().split('\n')
filtered_lines = []
seen_ids = set()

for i, line in enumerate(lines):
    if "SYSOUT ID" in line:
        sysout_id = line.split()[2]
        # print(sysout_id)
        if sysout_id not in seen_ids:
            seen_ids.add(sysout_id)
            filtered_lines.append(line)
            # print(line)
    elif "GEN"  in line:
        gen_id=line.split()[3]
        # print(gen_id)
        if gen_id not in seen_ids:
            seen_ids.add(gen_id)

            filtered_lines.append(line)

filtered_output = '\n'.join(filtered_lines)
# print(filtered_output)
with open( 'file1.txt','w') as f:
    f.write(filtered_output)



# Read input from a text file
with open('file1.txt', 'r') as file:
    new_lines = file.read()

# print(new_lines)
lines=[]
for line in new_lines.split('\n'):
    lines.append(line)

# lines=(line for line in new_lines.split('\n'))
# print(lines)
#
# Split the input text into individual records
# Create a new Excel workbook and sheet
wb = openpyxl.Workbook()
ws = wb.active

# Set the column headers
headers = ["SYSOUT ID", "JOBNAME", "PRINT DATE", "ARCHIVE DATE", "GEN", "JOBID", "PRINT TIME", "ARCHIVE TIME",
           "RETURN-CODE"]
ws.append(headers)

# Process each record
i = 0
j = 1
k=2
while i < len(lines) and j < len(lines):
    sysout_id = re.search(r"SYSOUT ID: (.*?)\s", lines[i]).group(1)

    jobname = re.search(r"JOBNAME: (.*?)\s", lines[i]).group(1)
    print_date = re.search(r"PRINT DATE: (\d{2}/\d{2}/\d{4})\s", lines[i]).group(1)
    archive_date = re.search(r"ARCHIVE DATE: (\d{2}/\d{2}/\d{4})\s", lines[i]).group(1)
    gen = re.search(r"GEN:\s{7}(.*?)\s", lines[j]).group(1)
    jobid = re.search(r"JOBID:\s{3}(.*?)\s", lines[j]).group(1)
    print_time = re.search(r"PRINT TIME: (.*?)\s", lines[j]).group(1)
    archive_time = re.search(r"ARCHIVE TIME: (.*?)\s", lines[j]).group(1)
    # return_code=re.search(r'RETURN-CODE:\s{14}(.*?)\s',lines[k]).group(1)
    i += 2
    j += 2
    k+=2

    # Append data to the Excel sheet
    data = [sysout_id, jobname, print_date.replace('/', '-'), archive_date.replace('/', '-'), gen,
            jobid, print_time,archive_time]
    ws.append(data)

# Save the Excel file
wb.save('output.xlsx')
