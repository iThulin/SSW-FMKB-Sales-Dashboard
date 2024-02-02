import pandas as pd
import os
import altair as alt
import panel as pn
#from vega_datasets import data

pn.extension('vega')

# Constants 
IMPORT_PATHS = {
    '2024': 'Z:/Commission - Job Cost/2024/2024 Job Cost Summary.xlsx',
    '2023': 'Z:/Commission - Job Cost/2023/2023 Job Cost Summary.xlsx',
    '2022': 'Z:/Commission - Job Cost/2022/2022 Job Cost Summary.xlsx',
    '2021': 'Z:/Commission - Job Cost/2021/2021 Job Cost Summary.xlsx',
    '2020': 'Z:/Commission - Job Cost/2020/2020 Job Cost Summary with Analysis.xlsx',
    '2019': 'Z:/Commission - Job Cost/2019/2019 Job Cost Summary with Analysis.xlsx',
    '2018': 'Z:/Commission - Job Cost/2018/2018 Job Cost Summary with Analysis.xlsx'
}

COLS_TO_KEEP = [
    'City',
    'Designer',
    'Installer',
    'Contract Date',
    'Customer',
    'Product',
    'Net Sale',
    'Direct Costs',
    'Margin',
    'Comm $',
    'Comm %',
    'Over (Under) Par',
    'Addtl Incent'
]

# Variables
update_bool = False

# Functions
def import_dataset(path, export_name):
    raw = pd.read_excel(path, sheet_name='Raw Data', header= 3)

    #df = raw.drop(labels=['Unnamed: 0', 'Notes', 'Unnamed: 17', 'Unnamed: 18'], axis=1)

    df = raw.loc[:, COLS_TO_KEEP]

    df = df.dropna(axis=0, subset='City')

    file_path = 'Data/' + export_name + 'sales.txt'

    df.to_csv(file_path, index=False)

def combine_dataset():
    data_files = []
    for filename in os.listdir('Data/'):
        file = os.path.join('Data/', filename)
        if os.path.isfile(file):
            data_files.append(file)

    df_concat = pd.concat([pd.read_csv(f) for f in data_files ], ignore_index=True)

    df_concat.to_csv('Data/Combined/Combined data.txt', index=False)

if update_bool == True:

    # Import and combine datasets
    for entry in IMPORT_PATHS:
        import_dataset(IMPORT_PATHS[entry], entry)

    combine_dataset()

# Load data and sort by date
data = pd.read_csv('Data/Combined/Combined data.txt')   
data['Contract Date'] = pd.to_datetime(data['Contract Date'])
data.sort_values(by='Contract Date')


#print(data)

base = alt.Chart(data).mark_point().encode(
    x='Contract Date',
    y='Net Sale',
    color='Product',
).properties(
    height=500,
    width=500
).interactive()

altair_pane = pn.panel(base)
altair_pane