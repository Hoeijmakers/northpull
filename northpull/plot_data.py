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
import matplotlib.pyplot as plt
from astropy.time import Time
from astropy.time import TimezoneInfo
import astropy.units as u
from matplotlib.dates import DateFormatter, HourLocator, DayLocator
from matplotlib.ticker import FixedLocator
import pytz
from datetime import datetime, timezone, timedelta


coloury = False
data_in = np.load('data.npy')

nt = datetime.now()#This assumes that your code is run from the CET/CEST timezone.


# Convert times to Astropy Time objects
t = Time(data_in[0],format='mjd')
y = data_in[1]*100/1000
# Convert Astropy Time objects to Matplotlib format
t_plot = t.plot_date
dt = t.to_datetime()

mean30 = np.nanmean(y[-30*24:])#30-day trailing average.

# alphas=y*0.0+0.5
i_now = np.argmin(np.abs(dt+timedelta(hours=0.5)-datetime.now()))




if coloury:
    #Defining colours and remapping y linearly onto a colour range
    #Such that the colour goes from c0 to c1 as y goes from y0 to y1.
    cmap = 'gist_rainbow'
    y_norm = y/mean30
    c0 = 0.4
    c1 = 0.0
    y0 = 0.5
    y1 = 2
    #y=ax+b:
    A = (c0-c1)/(y0-y1)
    B = c0-A*y0
    colours = plt.cm.get_cmap(cmap)(np.clip(A*y_norm+B,np.min([c0,c1]),np.max([c0,c1])))
else:
    colours = ['steelblue' for i in y]


fig, ax = plt.subplots(figsize=(15,5))
# ax.axvline(datetime.now(),color='red')
# ax.scatter(dt+timedelta(hours=1), y,alpha=0.7,cmap=cmap,c=colours)
ax.bar(dt+timedelta(hours=0.5),height=y,align='center',width=1/24*0.9,color=colours,alpha=0.4)
ax.bar(dt[i_now]+timedelta(hours=0.5),height=y[i_now],align='center',width=1/24*0.9,color=colours[i_now],alpha=0.7)
ax.axhline(mean30,color='black',alpha=0.7,linestyle='--')
ax.text(max(dt)+timedelta(hours=1.9),mean30+0.1*np.std(y),'30-day trailing mean',fontsize=9,ha='right',va='center')
# ax.plot(dt, y,color='yellow',alpha=0.7)
date_form = DateFormatter('%d-%b')
hour_form = DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(date_form)
ax.xaxis.set_minor_formatter(hour_form)
# Set the major ticks at the start of each day and the minor ticks at each hour
ax.xaxis.set_major_locator(DayLocator())
ax.xaxis.set_minor_locator(HourLocator(byhour=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],interval=1))
ax.set_xlim(max(dt)-timedelta(hours=37),max(dt)+timedelta(hours=2))
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
plt.setp(ax.get_xticklabels(minor=True), rotation=45, ha='right',fontsize=8)
fig.tight_layout()
plt.show()



# pdb.set_trace()
