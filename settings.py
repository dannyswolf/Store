from datetime import datetime
import os
# Για τα log files

import sys
today_obj = datetime.today()
today = datetime.today().strftime('%d/%m/%Y')
today_str = today.replace("/", "-")
now = datetime.now()
now_str = now.strftime("%H-%M-%S")
VERSION = "V 1.1.3"
log_dir = "logs" + "/" + today.replace("/", "_") + "/"
BASE_PATH = "\\\\192.168.1.200\\Public\\GOOGLE-DRIVE\\ΕΓΓΡΑΦΑ"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

mlshop = 1

if mlshop:
    # ML Shop dbases
    DB = os.path.join(BASE_PATH, "2.  ΑΠΟΘΗΚΗ\\3. ΚΑΙΝΟΥΡΙΑ_ΑΠΟΘΗΚΗ.db")
else:  # VPN
    DB = "3. ΚΑΙΝΟΥΡΙΑ_ΑΠΟΘΗΚΗ.db"  # Local Dbase
    # dbase = "\\\\10.8.0.1\\Public\\GOOGLE-DRIVE\\ΕΓΓΡΑΦΑ\\6.  ΒΙΒΛΙΟ SERVICE\\Service_book.db"  #  VPN Windows


# DB = "3. ΚΑΙΝΟΥΡΙΑ_ΑΠΟΘΗΚΗ.db"
BASE_DIR = os.path.dirname(os.path.abspath(DB))
# print("BASE_DIR", BASE_DIR)
SPARE_PARTS_ROOT = os.path.join(BASE_DIR, "SpareParts_images/")

