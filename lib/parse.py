from bs4 import BeautifulSoup
import re
import pandas as pd
import geopandas as gpd


def parse_html(row, dic="None"):
    html_str = row["Description"]
    parsed_html = BeautifulSoup(html_str)
    array = parsed_html.body.find_all("td")
    array = array[2:]
    array = [clean_html(str(tag)) for tag in array]
    dic = dict(array[i : i + 2] for i in range(0, len(array), 2))
    if not (dic["FID"]):
        print(dic)
    return pd.Series(dic)


def clean_html(raw_html):
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext
