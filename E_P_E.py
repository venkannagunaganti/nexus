import sys

from userfunctions import ExtractAndWriteToExcel
return_code=(ExtractAndWriteToExcel.
             ExtractJesLog('C:/Users/vgunaganti/PycharmProjects/match/J0032069.x',
                                     'C:/Users/vgunaganti/PycharmProjects/match/J0032069.xlsx'))
sys.exit(return_code)
