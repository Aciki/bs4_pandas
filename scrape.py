import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
from os import listdir
from os.path import isfile, join
import pathlib
print(pathlib.Path(__file__).parent.resolve())
import pandas as pd




#########################################################################################
url = "https://www.rfzo.rs/index.php/osiguranalica/lekovi-info/lekovi-actual"

response =  requests.get(url)
content =  BeautifulSoup(response.text, 'lxml')

all_urls = content.find_all('a')

pdf_urls = []

for url in all_urls:
	link_url = ''
	try :
		if ( "xls" in url['href']) and 'http' not in url['href']:
			link_url = 'https://www.rfzo.rs' + url['href']
			# print(link_url)
			no_repeat = ()
			no_repeat = link_url
			pdf_response  =requests.get(no_repeat)
			print(no_repeat)
			file_name = urllib.parse.unquote(no_repeat.split('/')[-1].replace(".." ,".").replace(" ","_").replace(" ", "_"))

			with open("./pdf_docs/" + file_name , "wb") as f :
				f.write(pdf_response.content)


			pdf_url = requests.get(url['href'])
			print(pdf_url)
			
	except Exception as e:
		print(e)



def all_files():
	path = "/home/alek/scrape1_pdf_/pdf_docs"
	files  =  os.listdir(path)
	print(files)
	
	for f in files:
		print(path+"/"+f)
		df = pd.read_excel(path+"/"+f)
		print(df[:10])
		return df

df =  all_files()
all_data = pd.DataFrame()

all_data = all_data.append(df,ignore_index=True)
print(all_data)

for col in all_data.columns:
    print(col)

all_data.to_excel("new_combined_file.xlsx")
cleaned_data = all_data.drop_duplicates(subset=['ATC '])

gk = cleaned_data.groupby('Država proizvodnje leka')
print(gk.sum())




