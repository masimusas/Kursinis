from docxtpl import DocxTemplate
import jinja2
from docx import Document
from datetime import date, datetime, timedelta
import os
# darbuotojas = "Jonas"
basedir = os.path.abspath(os.path.dirname(__file__))
doc = DocxTemplate( os.path.join(basedir, 'temp.docx'))

date_start = '2021-10-20'
date_end = '2022-2-20'
date_start_format = datetime.strptime(date_start, "%Y-%m-%d")

date_end_format = datetime.strptime(date_end, "%Y-%m-%d")
days_sum = date_end_format - date_start_format  
# days_format = days_sum.days("%d")
# days_format = '{} days'.format(days_sum.days)
days_format2 = (f'{days_sum.days} "%d"') 
context = {'darbuotojas': "Martynas Zaksas",
           'prasymo_data': date.today(),
           'atostogu_tipas': "Kasmetinės atostogos",
           'atostogu_pradzia': '2021-10-20',
           'atostogu_pabaiga': '2021-10-20',
           'atostogu_trukme': '45',
           'pavaduojantis_darbuotojas': "Martynas Zaksas",
           'vadovas': "Giedrius Žilėnas"
           }
doc.render(context)

doc.save(os.path.join(basedir, "generated_doc.docx"))

