#write a function that finds only files matching a specific date range in a folder

import os
import re
import datetime
import time
import sys
import argparse
import glob
import shutil

def main():
    parser = argparse.ArgumentParser(description='Find files in a folder matching a specific date range')
    parser.add_argument('-f', '--folder', help='Folder to search', required=True)
    parser.add_argument('-s', '--startdate', help='Start date (YYYY-MM-DD)', required=True)
    parser.add_argument('-e', '--enddate', help='End date (YYYY-MM-DD)', required=True)
    parser.add_argument('-o', '--output', help='Output folder', required=True)
    args = parser.parse_args()
    folder = args.folder
    startdate = args.startdate
    enddate = args.enddate
    output = args.output

    #convert startdate and enddate to datetime objects
    startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')

    #get list of files in folder
    files = os.listdir(folder)
    
    #loop through files
    for file in files:
        #get file creation date from file name
        filedate = file.split('_')[0]
        filedate = datetime.datetime.strptime(filedate, '%Y%m%d')
        #if file creation date is between startdate and enddate, copy file to output folder
        if filedate >= startdate and filedate <= enddate:
            shutil.copy(os.path.join(folder, file), output)
            
    