import subprocess
from datetime import datetime

date = datetime.today()
date_str = date.strftime("%d-%m-%y_%H-%M")

subprocess.call('C:\\Program Files\\MySQL\\MySQL Server 5.7\\bin\\mysqldump.exe -uroot -p088011 --single-transaction avi_crm -r C:\\Users\\Alexandr\\Desktop\\bacup_sql\\dump_%s.sql'
                % date_str)
subprocess.call('rar a -ep1 C:\\Users\\Alexandr\\Desktop\\rarDump_%s.rar C:\\Users\\Alexandr\\Desktop\\bacup_sql\\dump_%s.sql' % (date_str, date_str))