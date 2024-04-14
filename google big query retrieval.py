# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 15:47:17 2024

@author: Taha
"""
##### SET-UP
import pandas
from google.cloud import bigquery
import csv

client = bigquery.Client()
project_id = 'your_project_id'
dataset_id = 'your_dataset'