from datetime import datetime
import os
# Για τα log files
import logging
import sys
today_obj = datetime.today()
today = datetime.today().strftime('%d/%m/%Y')
today_str = today.replace("/", "-")
now = datetime.now()
now_str = now.strftime("%H-%M-%S")
VERSION = "V 1.1.0"
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
print("BASE_DIR", BASE_DIR)
SPARE_PARTS_ROOT = os.path.join(BASE_DIR, "SpareParts_images/")

log_file_name = f"{today_str}.log"
log_file = os.path.join(log_dir, log_file_name)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # or whatever

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)  # or whatever
handler = logging.FileHandler(log_file, 'a', 'utf-8')  # or whatever

handler.setFormatter(formatter)  # Pass handler as a parameter, not assign
root_logger.addHandler(handler)
sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info