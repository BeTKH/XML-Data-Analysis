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
Prism = "RRID: ?SCR_002798|(?!RRID:) ?SCR_002798"
ImageJ = "RRID: ?SCR_003070|(?!RRID:) ?SCR_003070"
Matlab = "RRID: ?SCR_001622|(?!RRID:) ?SCR_001622"
Fiji = "RRID: ?SCR_002285|(?!RRID:) ?SCR_002285"
R = "RRID: ?SCR_001905|(?!RRID:) ?SCR_001905"

Pattern_Prism = re.compile(Prism, re.IGNORECASE)
Pattern_ImageJ = re.compile(ImageJ, re.IGNORECASE)
Pattern_Matlab = re.compile(Matlab, re.IGNORECASE)
Pattern_Fiji = re.compile(Fiji, re.IGNORECASE)
Pattern_R = re.compile(R, re.IGNORECASE)

data_s = []
dict_missing = {}

for dir_ in list(RRIDs_final_Result):

    xml_path = path+dir_         #creates path to the directory that contains xml files

    for xml_file in os.listdir(xml_path):
        if xml_file in all_xml_list_with_rrid:
            xml_file_path = os.path.join(xml_path, xml_file)

            #parse the xml file in xml_file_path
            with open(xml_file_path, "r") as file:

                # Read the XML file specified at xml_file_path
                content = file.readlines()

                # Combine the lines in the list into a string
                content = "".join(content)
                xml_content = bs(content, "lxml")
                xml_str = str(xml_content)

                Prism_match = re.findall(Pattern_Prism, xml_str)
                ImageJ_match = re.findall(Pattern_ImageJ, xml_str)
                Matlab_match = re.findall(Pattern_Matlab, xml_str)
                Fiji_match = re.findall(Pattern_Fiji, xml_str)
                R_match = re.findall(Pattern_R, xml_str)


                if (len(Prism_match) != 0 or len(ImageJ_match) != 0 or len(Matlab_match) != 0 or len(Fiji_match) != 0 or len(R_match) != 0):

                    if dir_ != 'eLife':

                        epub_date = xml_content.find_all("pub-date",{"pub-type": "epub"})
                        article_title = xml_content.find("article-title").text

                        for date in epub_date:
                            date_x = '{}-{}-{}'.format(*[a.contents[0] for a in list(date.children)])

                            print( f'{date_x}|{dir_}|Prism_match = {len(Prism_match)}|ImageJ_match = {len(ImageJ_match)}|Matlab_match = {len(Matlab_match)}|Fiji_match = {len(Fiji_match)}|R_match = {len(R_match)}\n')

                            data = [date_x, dir_, xml_file, article_title, len(Prism_match), len(ImageJ_match),
                                   len(Matlab_match),len(Fiji_match),len(R_match) ]
                        data_s.append(data)

                    elif dir_ == 'eLife':

                        epub_date = xml_content.find_all("pub-date",{"date-type": "pub"})

                        article_title = xml_content.find("article-title").text
                        for date in epub_date:
                            date_x = '{}-{}-{}'.format(*[a.contents[0] for a in list(date.children)])

                            print( f'{date_x}|{dir_}|Prism_match = {len(Prism_match)}|ImageJ_match = {len(ImageJ_match)}|Matlab_match = {len(Matlab_match)}|Fiji_match = {len(Fiji_match)}|R_match = {len(R_match)}\n')

                            data = [date_x, dir_, xml_file, article_title, len(Prism_match), len(ImageJ_match),
                                   len(Matlab_match),len(Fiji_match),len(R_match) ]
                        data_s.append(data)
    #break
# Save the csv file as _4.Popular softwares citation count in journals.csv                

with open('/home/bk378/t20201023-RRID_analysis-BK/Files/CSVs/_4.Popular softwares citation count in journals.csv', "w", newline = "") as f:
    header = ['epub_Date','Journal','xml_file_name','article_title',
             'Prism','ImageJ', 'Matlab', 'Fiji', 'R']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data_s)
