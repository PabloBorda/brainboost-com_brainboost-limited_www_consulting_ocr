#
#   Author: Pablo Tomas Borda
#   Email:  pablo@digitzs.com
#


There is the global.config file for paths and parameters.

Then you can define new string patterns in the regexes.py file following the two samples I supplied to parse numbers and order IDs from text.

There are two processes, one consumes the images that the other produce.

    *   digitzs_batch_receipt_converter_service.py:         This process  turns a pdf into its corresponding image works even if multipages.
    *   process digitzs_receipts_processor_service.py:      This is the main one you have to execute when there are new receipts in the receipts folder. 

Then there are the two daemon versions as linux services for both previous processes

    *   digitzs_batch_receipt_converter_daemon.py
    *   process digitzs_receipts_processor_daemon.py



You can execute the two processes as a daemon. They check every for a defined interval if there are new files to process

To configure the previous as linux services you can do as follows:


    Copy the services in the linux folder so they are recognized as services 

        cp /com_brainboost_limited_consulting_ocr_receipt_ocr_linux_service/*.service /etc/systemd/system

        systemctl daemon-reload         # To make changes efective 

        service digitzs_batch_receipt_converter_service start
        servcie digitzs_receipts_processor_service start


    Once they are executing they will continue to populate the JSON TinyDb local database with the obtained data. 
