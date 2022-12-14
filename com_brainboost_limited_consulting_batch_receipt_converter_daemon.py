import os
import glob

from com_brainboost_limited_consulting_ocr_receipts.PDF2ImageConverter import PDF2ImageConverter
from com_brainboost_limited_consulting_ocr_receipts_config.Config import Config
import time



def check_if_pdf_was_converted_else_convert_it(file_to_check_if_was_converted):
    if not '_was_converted' in file_to_check_if_was_converted and '.pdf' in file_to_check_if_was_converted:
        PDF2ImageConverter.convert(file_to_check_if_was_converted)


def normalize_file_names_before_processing(file_name):
    parts = file_name.split('.')
    extension = parts[-1]
    name = '.'.join(parts[:-1])
    bad_characters = [' ','.','(',')','[',']','*','+',',']
  
    for bad_char in bad_characters:
        name = name.replace(bad_char,'_')

    return (name + '.' + extension)
    
    
list_of_files_old = []
list_of_files_new = os.listdir()


while True:
    
    list_of_files_new = os.listdir()

    while list_of_files_old != list_of_files_new: 

        receipts_dir = 'receipts'

        os.chdir(receipts_dir)
        list_of_files_new = os.listdir()
        dirlist = list(set(list_of_files_new) - set(list_of_files_old))

    
        dirlist = list_of_files_new
        os.chdir('..')
        for x in dirlist:
            not_normalized_file_name = (x)
            normalized_file_name = normalize_file_names_before_processing(not_normalized_file_name)
            if normalized_file_name != not_normalized_file_name:
                os.rename(receipts_dir + '/' + not_normalized_file_name,receipts_dir + '/' + normalized_file_name)
            try:
                check_if_pdf_was_converted_else_convert_it(normalized_file_name)
            except (Exception):
                print('Could not open the pdf file to convert into image as could not count amount of pages.' + normalized_file_name)

        list_of_files_old = list_of_files_new
        print('executing')
        time.sleep(int(Config.get('new_files_update_frequency')))