import pandas as pd
import numpy as np
import column_names_mapping as mapper


from openpyxl import Workbook
from openpyxl import load_workbook
from timeit import default_timer as timer


# to do
# naprawic mergowanie, dzialalo dobrze dla dwoch kolumn
# trzeba zrobic zeby dzialalo dobrze dla wielu kolumn



def excel_write(df, sheet_name, startrow, startcol):
    file = mapper.file_paths['output_file']
    wb = load_workbook(file)
    writer = pd.ExcelWriter(file, mode='a')
    writer.book = wb
    writer.sheets = dict((ws.title, ws) for ws in wb.worksheets)
    df.to_excel(
        excel_writer=writer,
        sheet_name=sheet_name,
        startrow=startrow,
        startcol=startcol,
        header=False,
        index=False,
    )
    writer.save()


def action_check(df, value):
    actions = {
    'merge': merge,
    'svc': svc,
    'move': move,
    }
    return actions[value.action](df, value)


def move(df, value):
    return df
# https://stackoverflow.com/questions/19377969/combine-two-columns-of-text-in-dataframe-in-pandas-python

def merge(df, value):
    first_col = value.old_position[0]
    if len(value.old_position)
    df['merged'] = df[first_col].str.cat(
        df[[value.old_position[1:]]], sep=value.sep, na_rep='None'
    )
    return df['merged']


def svc(df, value):
    cities = {
    'Oklahoma City': 'Echelon Medical',
    'Oklahoma City BP': 'The Brace Place',
    'Oklahoma City FS': 'First Steps Orthotics',
    'Tulsa': 'Echelon Medical',
    'Tulsa BP': 'The Brace Place',
    'Tulsa FS': 'First Steps Orthotics',
    'Medical Motion': 'Medical Motion',
    }
    df = df.replace(cities)
    return df


for key, value in mapper.relationships.items():
    start = timer()
    df = pd.read_excel(
        io=mapper.file_paths['input_file'],
        header=None,
        names=value.old_position,
        skiprows=mapper.settings['first_rows_skipped'],
        usecols=value.old_position,
    )
    print(df)
    df = action_check(df, value)
    excel_write(
        df=df,
        sheet_name='Parsed data', 
        startrow=mapper.settings['first_writing_row'], 
        startcol=value.new_position,
    )
    end = timer()
    print(end - start)

print('DONE')