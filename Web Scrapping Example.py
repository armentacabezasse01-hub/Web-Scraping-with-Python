#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 01:25:24 2025

Sergio Armenta , Assignment 7 , November 9th, 2025

@author: sergioarmenta
"""

import urllib.request as ur
import json
import pandas as pd
import re

def scrap_website(url, headers):
    """ In this function I'm creating a connection to the website to then scrape using json."""
    req       = ur.Request(url, headers=headers)
    response  = ur.urlopen(req)
    data      = response.read().decode()
    response.close()
    data_json = json.loads(data)
    return data_json

def extract_teams(data_json): 
    """ In this function I'm are scrapping the website, and placing data in a python
    dictionary to then be able to perform a regex function and retrieve only the desired data"""
    teams_list = []
    for team in data_json["teams"]:
        teams_list.append({"Team": team["name"], "Venue": team["venue"]})
    df = pd.DataFrame(teams_list)
    return df

def regex_extraction(df, pattern, filename):
    """ In this function I'm using regex where I will then append into a 
    dictionary and then save into a file with the users desired name. """ 
    regex       = re.compile(pattern, re.IGNORECASE)
    filtered_df = df[df["Team"].str.contains(regex, na = False)]
    
    data_dict   = []
    for _, row in filtered_df.iterrows():
        data_dict.append({"Team": row["Team"], "Venue": row["Venue"]})
    
    f = open(filename, "w")
    f.write("Team\t\tVenue\n")
    for item in data_dict:
        f.write(f"{item['Team']}\t{item['Venue']}\n")
    f.close()
    
    return filtered_df

def main():
    url      = "https://api.football-data.org/v4/competitions/PD/teams"
    headers  = {"X-Auth-Token": "c1f1acc554374cee94d4362c0676bcb2"} # <-- My personal token
    data     = scrap_website(url, headers)
    df       = extract_teams(data)

    pattern  = r"CF$"
    fn_input = input("What would you like the filename to be? ")
    filename = fn_input + ".txt"
    file     = regex_extraction(df, pattern, filename)
    print("\nTeams that end with 'CF':")
    print(file)
    
main()