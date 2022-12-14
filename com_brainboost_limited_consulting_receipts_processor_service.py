from curses import keyname
import os
from com_brainboost_limited_consulting_ocr_receipts_config.Config import Config
from com_brainboost_limited_consulting_ocr_receipts.OCRExtractor import OCRExtractor
import re

from tinydb import TinyDB, Query

db = TinyDB(Config.get('database_path'))


receipts_dir = Config.get('path_to_receipts_that_can_be_images_or_pdfs')

os.chdir(receipts_dir)
dirlist = os.listdir()
os.chdir('..')
for d in dirlist:
    if '.jpg' in d[-4:]:
        print('processing ' + d)
        wordset = OCRExtractor.image_to_text(receipts_dir + '/' + d)
        wordset_with_no_coordinates = [w[4] for w in wordset]
        join_big_string_of_words =  ' '.join(wordset_with_no_coordinates)
        print(d + ' DONE: inserting text')
        
        from com_brainboost_limited_consulting_ocr_receipts_regex.regexes import my_regexes
        keys_for_interesting_text = my_regexes.keys()
        obtain_important_texts = []
        for k in keys_for_interesting_text:
            current_detected_text = re.search(my_regexes[k][0],join_big_string_of_words)
            if current_detected_text != None:
                select_text_from_detected_pattern = current_detected_text.group(int(my_regexes[k][1]))
                obtain_important_texts.append({ k : select_text_from_detected_pattern})
        db.insert({'receipt_name': d ,'original_ocr_text': join_big_string_of_words,'obtain_important_texts': obtain_important_texts})


