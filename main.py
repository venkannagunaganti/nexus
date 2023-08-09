import datetime
import re
# splitting using patterns
pattern=r' '
text="a:b d: e,f:l"
print(re.split(pattern,text))


# # group
# text='start date:20230810, end date 20230810'
# pattern=r'(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})'
# matched_text=re.search(pattern,text)
# # print(matched_text.group('year'))
# for i,val in enumerate(matched_text.groups()):
#     pass
#     # print(val)
# # find and replace
# replacement_pattern=r'\g<day>-\g<month>-\g<year>'
#
# # print(new_text)
# # text replacement
# def format_date(match):
#     in_date=match.groupdict()
#     year=int(in_date['year'])
#     month = int(in_date['month'])
#     day = int(in_date['day'])
#     return datetime.date(year,month,day).strftime('%y-%b-%d')
# # print(format_date(matched_text.groups()))
#
# new_text=re.sub(pattern,format_date,text)
# print(new_text)