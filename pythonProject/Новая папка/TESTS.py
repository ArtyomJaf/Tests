import csv
from pprint import pprint
import re
import os

dialogue = 0
clients = dict()
info = dict()
managers_name = ['', 'анастасия', 'ангелина', 'максим', '']


def demand(info):
    if info['a_greeting'] != False and info['e_farewell'] != False:
        info['f_demand'] = 'Требования соблюдены'
    else:
        info['f_demand'] = 'Требования не соблюдены'
    return info


def farewell(id, line_n, manager, text, insight, file_writer, info):
    if manager == 'manager' and 'до свидания' in text.lower():
        info['e_farewell'] = text
        insight += 'farewell = True'
    else:
        try:
            if info['e_farewell']:
                pass
        except KeyError:
            info['e_farewell'] = False
    file_writer.writerow([id, line_n, manager, text, insight])


def company(id, line_n, manager, text, insight, file_writer, info):
    if manager == 'manager' and 'бизнес' in text:
        try:
            if info['d_company'] == False:
                info['d_company'] = \
                    ''.join([text.split()[index - 1] + ' бизнес'
                             if text.split()[index] == 'бизнес'
                             else text.split()[index]
                             for index in range(len(text.split()))
                             if bool(re.search('(?:{})'.format('|'.join(['ваш', 'свой',
                                                                         'любой', 'твой', 'чужой'])),
                                               text.split()[index - 1],
                                               flags=re.I)) == False
                             and 'бизнес' in text.split()[index]])
                insight += ' company = True'
        except KeyError:
            info['d_company'] = \
                ''.join([text.split()[index - 1] + ' бизнес'
                         if text.split()[index] == 'бизнес'
                         else text.split()[index]
                         for index in range(len(text.split()))
                         if bool(re.search('(?:{})'.format('|'.join(['ваш', 'свой', 'любой',
                                                                     'твой', 'чужой'])),
                                           text.split()[index - 1],
                                           flags=re.I)) == False
                         and 'бизнес' in text.split()[index]])
            insight += ' company = True'
    else:
        try:
            if info['d_company']:
                pass
        except KeyError:
            info['d_company'] = False

    if info['d_company'] == '':
        info['d_company'] = False
    farewell(id, line_n, manager, text, insight, file_writer, info)


def greeting(id, line_n, manager, text, insight, file_writer, info):
    if manager == 'manager' and 'здравствуйте' in text.lower() or manager == 'manager' and 'добрый' in text.lower():
        info['a_greeting'] = text
        insight += 'greeting = True '
    else:
        try:
            if info['a_greeting']:
                pass
        except KeyError:
            info['a_greeting'] = False
    strings_manager_name(id, line_n, manager, text, insight, file_writer, info)


def strings_manager_name(id, line_n, manager, text, insight, file_writer, info):
    if manager == 'manager' and bool(
            re.search("mis{}sing_value".format('|'.join(managers_name)), text.lower(), flags=re.I)) is True:
        try:
            if not info['c_name_manager']:
                info['b_string_with_name_manager'] = text
                info['c_name_manager'] = ''.join([name for name in managers_name if name in text.lower()]).title()
                insight += ' name_manager = True'
        except KeyError:
            info['b_string_with_name_manager'] = text
            info['c_name_manager'] = ''.join([name for name in managers_name if name in text.lower()]).title()
            insight += ' name_manager = True'
        else:
            pass
    else:
        try:
            if info['c_name_manager']:
                pass
        except KeyError:
            info['c_name_manager'] = False
            info['b_string_with_name_manager'] = False
    company(id, line_n, manager, text, insight, file_writer, info)


with open("newtest_data.csv", mode="w", encoding='utf-8') as w_file:
    with open("test_data.csv", encoding='utf-8', newline='') as csvfile:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        reader = csv.DictReader(csvfile, delimiter=",")
        file_writer.writerow(['\ufeffdlg_id', 'line_n', 'role', 'text', 'insight'])

        for row in reader:
            insight = ''
            if dialogue == int(row['\ufeffdlg_id']):
                greeting(row['\ufeffdlg_id'], row['line_n'], row['role'], row['text'], insight, file_writer, info)
            else:
                clients[dialogue] = demand(info)
                info = dict()
                dialogue += 1
                greeting(row['\ufeffdlg_id'], row['line_n'], row['role'], row['text'], insight, file_writer, info)
        clients[dialogue] = demand(info)
    os.remove("test_data.csv")
os.rename("newtest_data.csv", "test_data.csv")
pprint(clients)
