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



data_in = np.load('data.npy')

nt = datetime.now()#This assumes that your code is run from the CET/CEST timezone.


# Convert times to Astropy Time objects
t = Time(data_in[0],format='mjd')
y = data_in[1]
# Convert Astropy Time objects to Matplotlib format
t_plot = t.plot_date
dt = t.to_datetime()

fig, ax = plt.subplots(figsize=(15,5))
ax.axvline(datetime.now(),color='red')
ax.plot(dt, y,color='navy',alpha=0.7)
date_form = DateFormatter('%d-%b')
hour_form = DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(date_form)
ax.xaxis.set_minor_formatter(hour_form)
# Set the major ticks at the start of each day and the minor ticks at each hour
ax.xaxis.set_major_locator(DayLocator())
ax.xaxis.set_minor_locator(HourLocator(byhour=[3,6,9,12,15,18,21],interval=1))

plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
plt.setp(ax.get_xticklabels(minor=True), rotation=45, ha='right',fontsize=8)
plt.show()
