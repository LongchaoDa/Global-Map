import requests
import numpy as np
from bs4 import BeautifulSoup

# input_box = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
# input_box = [2015, 2016]
input_box = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
base_url = "https://eogdata.mines.edu/nighttime_light/"
base_page = requests.get(base_url)
base_page.encoding = "utf-8"
base_html = base_page.text
base_soup = BeautifulSoup(base_html, features="html.parser")
main_table = base_soup.findAll("td", class_="indexcolicon").remove("td")
print(main_table)
accumulation = 0.
#
# for input in input_box:
#     # page = requests.get('https://eogdata.mines.edu/nighttime_light/annual/v21/'+str(input))
#     # page = requests.get('https://eogdata.mines.edu/nighttime_light/monthly/v10/'+str(input))
#     # page = requests.get('https://eogdata.mines.edu/nighttime_light/nightly/cloud_cover')
#     page = requests.get('https://eogdata.mines.edu/nighttime_light/nightly/rade9d/')
#     page.encoding = "utf-8"
#     html = page.text
#     soup = BeautifulSoup(page.text, features="html.parser")
#     all_items = soup.find_all("td", class_="indexcolsize")
#     all_list = []
#     all_G = []
#     all_M = []
#     for item in all_items:
#         temp_string = item.text
#         all_list.append(temp_string)
#         # print(item.text)
#         if temp_string.find("-") != -1:
#             pass
#         elif temp_string.find("G") != -1:
#             all_G.append(float(temp_string.replace("G", "")) * 1024)
#         else:
#             all_M.append(float(temp_string.replace("M", "")))
#
#     result = all_M + all_G
#     result = np.array(result)
#     sum = np.sum(result)
#     accumulation += sum
#     print("----" + str(input) + "----")
#     print(sum)
#
# print("accumulation(M):" + str(accumulation))
