import re
import pdfplumber
import sys
from os import listdir
from os.path import isfile, join
import csv

"""
date = report[1]
hawb = report[2]
mawb = report[3]
dest = report[4]
chargeable = report[5]
charges = report[6]
unit_price = report[7]
packages = report[8]
weight = report[9]
"""
def read_pdf_as_text(file_name):
    pdf = pdfplumber.open(file_name)
    page = pdf.pages[0]
    text = page.extract_text()
    pdf.close()
    return text

def parse_report(text):
    d = {}

    lines = text.splitlines()
    date_and_invoice = lines[2].split()
    d[0] = date_and_invoice[0]
    d[1] = date_and_invoice[1]
    
    # AWB number
    awb_line = lines[4]
    d[2] = awb_line.split()[-1]
    
    # Destination
    dest_line = lines[15].split()
    d[3] = ' '.join(dest_line[3:-1])
    
    # 5 6 7 10 11
    desc = lines[19].split()
    d[10] = desc[2]
    d[11] = desc[6]
    d[5] = desc[7]
    d[6] = desc[8]
    d[7] = desc[-1]
    
    
    # total
    total_line = lines[-1].split()
    d[12] = total_line[1]
    
    
    return d
    
def run():
    text = read_pdf_as_text('input/test1.pdf')
    #print(text)
    report = parse_report(text)
    print(report)

def eval_folder(folder='input'):
    onlyfiles = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
    reports = []
    for f in onlyfiles:
        print('Processing..', f)
        report = parse_report(read_pdf_as_text(f))
        #print(report)
        reports.append(report)
    
    return reports

def csv_writer(reports):
    with open('output/result.csv', "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        # write headers
        header = ['日期','Invoice No.','总运单号','清关公司','Chargable Weight','Freight','单价','麻袋数',
            '毛重','泡重产生的额外费用','提单重量','重量差','提单号']
        writer.writerow(header)
        
        # contents
        for report in reports:
            l = []
            for i in range(1, 10):
                l.append(report[i])
                
            # writerow requires a list
            writer.writerow(l)
    
#reports = eval_folder()
#csv_writer(reports)

run()