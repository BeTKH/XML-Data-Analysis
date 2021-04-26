# creating csv file for software resources
# extraction publication Date and article title, list of software resources and their count

import csv
import os
import re
import xml.etree.ElementTree as ET
from os import listdir
from bs4 import BeautifulSoup as bs
path = '/mnt/storage1/nlp/pubmed_xml/'

# regx pattern used for _2.Journal_xml_SCR_RRID_with_article_title.csv
SCR_search = "RRID: ?SCR_[0-9]{4,}|(?!RRID:) ?SCR_[0-9]{4,}"
Pattern_SCR = re.compile(SCR_search, re.IGNORECASE)

data_s = []
dict_missing = {}

for dir_ in list(RRIDs_final_Result):
    xml_path = path+dir_         #creates path to the directory that contains xml files
    for xml_file in os.listdir(xml_path):
        if xml_file in all_xml_list_with_rrid:
            xml_file_path = os.path.join(xml_path, xml_file)

            print(xml_file_path)
            #parse the xml file in xml_file_path
            with open(xml_file_path, "r") as file:

                # Read each line in the file, readlines() returns a list of lines

                content = file.readlines()

                # Combine the lines in the list into a string
                content = "".join(content)
                xml_content = bs(content, "lxml")
                xml_str = str(xml_content)
                match = re.findall(Pattern_SCR, xml_str)

                if (dir_ != 'eLife') and (match != 0):
                    epub_date = xml_content.find_all("pub-date",{"pub-type": "epub"})

                    article_title = xml_content.find("article-title").text

                    for date in epub_date:
                        date_x = '{}-{}-{}'.format(*[a.contents[0] for a in list(date.children)])
                        print( f'{dir_}: {xml_file} :{date_x} :{len(match)}: {article_title}\n')
                        data = [dir_, xml_file, article_title, date_x, match, len(match) ]
                    data_s.append(data)

                elif (dir_ == 'eLife') and (match != 0):
                    epub_date = xml_content.find_all("pub-date",{"date-type": "pub"})

                    article_title = xml_content.find("article-title").text
                    for date in epub_date:
                        date_x = '{}-{}-{}'.format(*[a.contents[0] for a in list(date.children)])
                        print( f'{dir_}: {xml_file} :{date_x} :{len(match)}: {article_title}\n')
                        data = [dir_, xml_file, article_title, date_x, match, len(match) ]
                    data_s.append(data)

# Save the csv file as _2.Journal_xml_SCR_RRID_with_article_title.csv

with open('/home/bk378/t20201023-RRID_analysis-BK/Files/CSVs/_2.Journal_xml_SCR_RRID_with_article_title.csv', "w", newline = "") as f:
    header = ['Journal','xml_file_name','article_title','epub_Date',
             'RRID mentions','RRID Count']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data_s)
