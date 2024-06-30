import os
import shutil
import zipfile
import openpyxl
from win32com import client


# =============================================================================
#  Function name: create_folder
#  Author: < Kondri Satyannarayana. >
#  Description: Creates a new folder at the specified 'folder_path'. If the folder already exists,
#               it will be deleted before creating the new one.
#  Input Parameters: folder_path (str) - The path to the folder to be created.
#  Output Parameters: Same as Input Parameter
#  How to invoke?: create_folder(folder_path)
#  Date created: <02/08/2023>
#  Date last modified & Changes done: <02/08/2023>
# =============================================================================

def create_folder(folder_path):
    if os.path.exists(folder_path):
        # Folder exists, so delete it
        print(f"Deleting existing folder: {folder_path}")
        os.rmdir(folder_path)

    # Create the new folder
    print(f"Creating new folder: {folder_path}")
    os.makedirs(folder_path)


# =============================================================================
#   Function name: zip_folder
#   Author: <Kondri Satyannarayana>
#   Description: Compresses all the contents of the 'folder_path' into a ZIP file with the name 'zip_name.zip'.
#   Input Parameters: folder_path (str) - The path to the folder to be zipped.
#   Output Parameters: zip_name (str) - The name of the ZIP file to be created.
#   How to invoke?: zip_folder(folder_path, zip_name)
#   Date created: <02/08/2023>
#   Date last modified & Changes done: <02/08/2023>
# =============================================================================

def zip_folder(folder_path, zip_name):
    try:
        # Zip all the contents to the folder.
        shutil.make_archive(zip_name, 'zip', folder_path)
        print(f"Folder {folder_path} zipped to {zip_name}.zip")
    except FileNotFoundError:
        print(f"Folder {folder_path} does not exist")


# =============================================================================
#   Function name: unzip_folder
#   Author: <Kondri Satyannarayana>
#   Description: Extracts the contents of the ZIP file located at 'zip_path' into a new folder
#                with the same name as the ZIP file (without the ".zip" extension).
#   Input Parameters: zip_path (str) - The path to the ZIP file to be extracted.
#   Output Parameters: NONE
#   How to invoke?: unzip_folder(zip_path)
#   Date created: <D02/08/2023>
#   Date last modified & Changes done: <02/08/2023>
# =============================================================================

def unzip_folder(zip_path):
    # Extract folder name from ZIP path
    folder_path = os.path.splitext(zip_path)[0]
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # Open the ZipFile.
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        # Extract all the contents to the same folder.
        zip_file.extractall(folder_path)


# =============================================================================
#  Function name: create_file
#  Author: <Kondri Satyannarayana>
#  Description: Creates an empty file at the specified 'file_path' based on the file extension (TXT, CSV, or XLSX.).
#  Input Parameters: file_path (str) - The path to the file to be created.
#  Output Parameters: NONE
#  How to invoke?:  create_file(file_path)
#  Date created: <02/08/2023>
#  Date last modified & Changes done: <02/082023>
# =============================================================================

def create_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    # Get the file extension
    file_extension = file_path.split('.')[-1].lower()

    if file_extension == 'txt':
        with open(file_path, "w"):
            pass
    elif file_extension == 'csv':
        with open(file_path, "w", newline="") as csv_file:
            pass
    elif file_extension == 'xlsx':
        wb = openpyxl.Workbook()
        wb.save(file_path)
    else:
        raise ValueError("Unsupported file type. Please use '.txt', '.csv', '.xlsx', or '.pdf'.")


# =============================================================================
#   Function name: zip_file
#   Author: <Kondri Satyannarayana>
#   Description: Compresses the 'file_to_zip' into a ZIP file with the specified 'zip_file_path'.
#   Input Parameters: file_to_zip (str) - The path to the file to be zipped.
#   Output Parameters: zip_file_path (str) - The path where the ZIP file will be created.
#   How to invoke?:  zip_file(file_to_zip, zip_file_path)
#   Date created: <02/08/2023>
#   Date last modified & Changes done: <02/08/2023>
# =============================================================================

def zip_file(file_to_zip, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(file_to_zip)


# =============================================================================
#  Function name: convert_to_pdf
#  Author: <Kondri Satyannarayana>
#  Description: Converts a given file (TXT, DOC, DOCX) located at 'file_path' into a PDF file
#                with the same name and in the same directory as the original file.
#                If the input file is empty or unsupported, it creates an empty PDF.
#  Input Parameters: file_path (str) - The path to the file to be converted.
#  Output Parameters: NONE
#  How to invoke?: convert_to_pdf(file_path)
#  Date created: <02/08/2023>
#  Date last modified & Changes done: <04/08/2023>
# =============================================================================

def convert_to_pdf(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    input_file_extension = os.path.splitext(file_path)[1].lower()

    output_file = os.path.splitext(file_path)[0] + ".pdf"

    if input_file_extension == '.txt':
        # Using pywin32 to convert txt to PDF
        word = client.Dispatch("Word.Application")
        doc = word.Documents.Open(file_path)
        doc.SaveAs(output_file, FileFormat=17)  # 17 is the PDF file format
        doc.Close()
        word.Quit()

    elif input_file_extension in ['.doc', '.docx']:
        # Using pywin32 to convert doc and docx to PDF
        word = client.Dispatch("Word.Application")
        doc = word.Documents.Open(file_path)
        doc.SaveAs(output_file, FileFormat=17)  # 17 is the PDF file format
        doc.Close()
        word.Quit()

    else:
        print("Error: File format not supported for conversion.")
        return

    print(f"File converted successfully. Saved as '{output_file}'")


# =============================================================================
#  Function name: open_excel_file
#  Author: Kondri Satyannarayana
#  Description: This function attempts to open an Excel file using the openpyxl library. It checks if the
#               specified Excel file exists. If the file exists, it loads the workbook and returns it. If
#               there's an error while opening the file, the function prints an error message, waits for a
#               short duration, and then retries. If the file does not exist, the function also waits for a
#               short duration before retrying.
#  Input Parameters:excel_filename (str): The path to the Excel file to be opened.
#  Output Parameters: Returns the loaded workbook object if successful, otherwise None.
#  How to invoke?: workbook = open_excel_file("path/to/your/excel/file.xlsx")
#    if workbook:
#        # Perform operations on the workbook
#  Date created: <14/08/2023>
#  Date last modified & Changes done: <14/08/2023>
# =============================================================================
def open_excel_file(excel_filename):
    while True:
        if os.path.exists(excel_filename):
            try:
                wb = openpyxl.load_workbook(excel_filename)
                return wb
            except Exception as e:
                print(f"An error occurred while opening the Excel file: {e}.")
        else:
            print(f"The Excel file '{excel_filename}' does not exist.")


