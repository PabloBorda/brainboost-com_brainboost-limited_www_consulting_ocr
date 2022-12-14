from pdf2image import convert_from_path, convert_from_bytes


from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

class PDF2ImageConverter:
    
    @classmethod
    def document_is_a_pdf(cls,document_relative_path):
        return '.pdf' == document_relative_path[-4:]
    
    @classmethod
    def convert(cls,document_relative_path,prefix_for_output_filename=None):
        prefix = ''
        document_relative_path = document_relative_path
        if prefix_for_output_filename==None:
            prefix = '_was_converted'
        else:
            prefix = prefix_for_output_filename
            
                        
        if cls.document_is_a_pdf(document_relative_path):
            print('converting pdf to image...')
            output_folder = 'receipts'
            output_file = document_relative_path.split('.')[-2].split('/')[0]+prefix + '-'
            
            image = convert_from_path(output_folder + '/' + document_relative_path, output_folder=output_folder,fmt='jpeg',output_file=output_file)
            return
    
            
            
                        
            