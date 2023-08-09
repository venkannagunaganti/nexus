import re
pattern=r'\d+'
file=open('J0032069.x', errors="ignore")
# def numbers():
#     for i in range(1,222):
#
#         print(i)
# numbers()
def string_search(string1,string2,string3):

    new_line=''
    for line in file:
        if line.startswith(string1):
            new_line+=line
        if line.startswith(string2):
            new_line+=line
        if line.__contains__(string3):
            new_line+=line

    return new_line
lines=string_search('* SYSOUT','* GEN','RETURN-CODE')
print(lines)
with open('file.txt','w') as file:
    file.write(lines)
