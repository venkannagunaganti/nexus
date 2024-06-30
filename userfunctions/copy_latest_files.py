# =============================================================================
#   Function name: copy_latest_files
#   Author: N.CHITTARIVEERABAHD1
#   Description: Copy the latest 'n' files (general, with wild character eg. , ) from a folder to other folder
#   Input Parameters:source_folder, destination_folder,Pattern,n
#   Output Parameters:  NONE
#  How to invoke ? : copy_latest_files(source_folder, destination_folder,Pattern, n)
#    Where As
#    source_folder = 'C:/Users/nchittarivee/OneDrive - DXC Production/Documents/narendra'
#    destination_folder = 'C:/Users/nchittarivee/OneDrive - DXC Production/Documents/python'
#    Pattern='*'
#    n=10
#   Date created: 02/08/2023
#   Date last modified & Changes done: 02/08/2023
# =============================================================================
import os
import glob
import shutil

def copy_latest_files(source_folder, destination_folder,Pattern, n):
    #  list of files in the source folder
    file_list = glob.glob(os.path.join(source_folder,Pattern ))

    # Sort the files by  (newest first)
    file_list.sort(key=os.path.getmtime, reverse=True)

    # Copy the latest 'n' files to the destination folder
    for file_path in file_list[:n]:
        if os.path.isfile(file_path):
            shutil.copy(file_path, destination_folder)




