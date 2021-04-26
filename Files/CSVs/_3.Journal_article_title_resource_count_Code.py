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
AB_search  = "RRID: ?AB_[0-9]{4,}|(?!RRID:) ?AB_[0-9]{4,}"
CVCL_search = "RRID: ?CVCL_[0-9]{4,}|(?!RRID:) ?CVCL_[0-9]{4,}|RRID: ?CVCL_[A-Z]+[0-9]+|(?!RRID:) ?CVCL_[A-Z]+[0-9]+"
BDSC_search = "RRID: ?BDSC_[0-9]{4,}|(?!RRID:) ?BDSC_[0-9]{4,}"
IMSR_search = "RRID: ?IMSR_JAX:[0-9]{6,}|(?!RRID:) ?IMSR_JAX:[0-9]{6,}"
Addgene_search = "RRID: ?Addgene_[0-9]{4,}|(?!RRID:) ?Addgene_[0-9]{4,}"

Pattern_SCR = re.compile(SCR_search, re.IGNORECASE)
Pattern_AB = re.compile(AB_Search, re.IGNORECASE)
Pattern_CVCL = re.compile(CVCL_search, re.IGNORECASE)
Pattern_BDSC = re.compile(BDSC_search, re.IGNORECASE)
Pattern_IMSR = re.compile(IMSR_search, re.IGNORECASE)
Pattern_Addgene = re.compile(Addgene_search, re.IGNORECASE)


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

                AB_match = re.findall(Pattern_AB, xml_str)
                SCR_match = re.findall(Pattern_SCR, xml_str)
                CVCL_match = re.findall(Pattern_CVCL, xml_str)
                BDSC_match = re.findall(Pattern_BDSC, xml_str)
                IMSR_match = re.findall(Pattern_IMSR, xml_str)
                Addgene_match = re.findall(Pattern_Addgene, xml_str)

                if (SCR_match != 0 or AB_match != 0 or CVCL_match != 0 or BDSC_match or IMSR_match or Addgene_match):

                    if dir_ != 'eLife':

                        epub_date = xml_content.find_all("pub-date",{"pub-type": "epub"})


                        article_title = xml_content.find("article-title").text

                        for date in epub_date:
                            date_x = '{}-{}-{}'.format(*[a.contents[0] for a in list(date.children)])

                            print( f'{date_x}|{dir_}|AB = {len(AB_match)}|SCR = {len(SCR_match)}|CVCL = {len(CVCL_match)}|BDSC = {len(BDSC_match)}|IMSR = {len(IMSR_match)}|Addgene = {len(Addgene_match)}\n')

                            data = [date_x, dir_, xml_file, article_title, len(AB_match), len(SCR_match),
                                   len(CVCL_match),len(BDSC_match),len(IMSR_match),len(Addgene_match) ]
                        data_s.append(data)

                    elif dir_ == 'eLife':
                        print(dir_)
                        epub_date = xml_content.find_all("pub-date",{"date-type": "pub"})

                        article_title = xml_content.find("article-title").text
                        for date in epub_date:
                            date_x = '{}-{}-{}'.format(*[a.contents[0] for a in list(date.children)])
                            print( f'{date_x}|{dir_}|AB = {len(AB_match)}|SCR = {len(SCR_match)}|CVCL = {len(CVCL_match)}|BDSC = {len(BDSC_match)}|IMSR = {len(IMSR_match)}|Addgene = {len(Addgene_match)}\n')
                            data = [date_x, dir_, xml_file, article_title, len(AB_match), len(SCR_match),
                                   len(CVCL_match),len(BDSC_match),len(IMSR_match),len(Addgene_match) ]
                        data_s.append(data)
    #break

# Save the csv file as _3.Journal_article_title_resource_count.csv

with open('/home/bk378/t20201023-RRID_analysis-BK/Files/CSVs/_3.Journal_article_title_resource_count.csv', "w", newline = "") as f:
    header = ['epub_Date','Journal','xml_file_name','article_title',
             'AB Count','SCR Count', 'CVCL count', 'BDSC Count', 'IMSR Count', 'Addgene Count']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data_s)
