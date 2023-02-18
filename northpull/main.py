import sys
import requests
from bs4 import BeautifulSoup
import numpy as np
import pdb
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from html.parser import HTMLParser
# import matplotlib.pyplot as plt
from astropy.time import Time

#Define a custom HTML parser to extract table data
class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = []
        self.current_row = []
        self.in_table = False

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.in_table = True
        elif self.in_table and tag == "td":
            self.current_row.append(None)

    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False
        elif self.in_table and tag == "tr":
            self.data.append(self.current_row)
            self.current_row = []

    def handle_data(self, data):
        if self.in_table:
            data = data.strip()
            if data:
                self.current_row.append(str(data))

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)


# Step 1: Retrieve the HTML content of the website
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = "https://www.example.com"

driver.get(url)
wait = WebDriverWait(driver, 2.0)
time.sleep(2)
# data_elements = driver.find_elements_by_css_selector("div.some-class > span")

table_id = "datatable"
table = wait.until(EC.presence_of_element_located((By.ID, table_id)))

parser = TableParser()
parser.feed(table.get_attribute("outerHTML"))
data = parser.data
driver.quit()
data_clean = []
dd,mm,yy = str(data[0][0]).split('-')


times = []
P = []
h = []
for i in range(1,len(data)-8):
    times.append(f'{yy}-{mm}-{dd}T{str(data[i][1].split()[0])}:00:00')
    t = Time(times, format='isot', scale='utc')
    h.append(float(str(data[i][1].split()[0])))
    P.append(float(data[i][-1].replace(',','.')))

# print(np.array(P))
data_clean = np.array([t.mjd,np.array(P)])


try:
    data_in = np.load('data.npy')
    data_out = np.hstack((data_in, data_clean))
except FileNotFoundError:
    # if the file doesn't exist, create an empty array
    data_out = data_clean

# save the concatenated data to file
np.save('data.npy', data_out)

# plt.plot(h,P)
# plt.title(f'{yy}-{mm}-{dd}')
# plt.show()
