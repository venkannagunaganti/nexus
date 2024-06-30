import os.path
from datetime import datetime
from pathlib import Path

#Declaring global variables
log_file=""
p=os.path.abspath(__file__)
path=Path(p).parent
path=str(path)+"\\"
time_stamp=""
i=""
#   Function name:create_log_file
#   Author: venkanna gunaganti
#   Description:creating logfile using caller filename
#   How to invoke?:create_log_file(filename)get filename from path using os module

#   Input parameters : filename.
#   Output parameters:NONE
#   Date created: 02/08/2023
#   Date last modified & Changes done: 02/08/2023
@staticmethod
def create_log_file(filename):
      global path
      name=filename.split(".")
      x=name[0]
      y=".log"
      path=str(path)+x+y
      msg = ''
      with open(path, 'w') as file:
         file.write(msg)
class LogFile:
#   Function name:write_to_log_file
#   Author: venkanna gunaganti
#   Description:writing to the created log file
#   How to invoke?:write_to_log_file(filename,line_number,msg_type,msg)
#   Input parameters : filename, line no, message type , message.
#   Output parameters:NONE
#   Date created: 02/08/2023
#   Date last modified & Changes done: 02/08/2023

  @staticmethod
  def write_to_log_file(file_name,line_number,msg_type,msg):
        p = Path(path)
        global time_stamp
        time_stamp = datetime.fromtimestamp(p.stat().st_mtime).isoformat()

        with open(path,'a+') as file:

            file.write(f"{time_stamp} {file_name}:{line_number} {msg_type}:{msg}\n")

#   Function name:msg
#   Author: venkanna gunaganti
#   Description:funtion for calling different Error message types
#   How to invoke?:mssg(filename,line_no,msg_type,msg)
#   Input parameters :file_name,line_no,msg_type,msg.
#   Output parameters:NONE
#   Date created: 02/08/2023
#   Date last modified & Changes done: 02/08/2023
@staticmethod
def msg(file_name,line_no,msg_type,msg):

    global log_file
    log_file=file_name
    match msg_type:
        case Message.critical_type:
            LogFile.write_to_log_file(file_name,line_no,Message.critical_type,msg)
        case Message.debug_type:
            LogFile.write_to_log_file(file_name,line_no,Message.debug_type,msg)
        case Message.warning_type:
            LogFile.write_to_log_file(file_name,line_no,Message.warning_type,msg)
        case Message.info_type:
            LogFile.write_to_log_file(file_name,line_no,Message.info_type,msg)
        case Message.error_type:
            LogFile.write_to_log_file(file_name,line_no,Message.error_type,msg)
        case Message.display_type:
            print(f"{time_stamp} {file_name}:{line_no} {Message.display}")

        case unknown_command:
            print(f"invalid message:{unknown_command} at lineno:{line_no}")




