
from ftplib import FTP

ftp = FTP()
ftp.set_debuglevel(2)  # Show detailed connection logs

try:
    ftp.connect("ftp.3gpp.org")  # Try a long timeout
    ftp.set_pasv(True)
    ftp.login()  # Anonymous login (or use credentials)
    ftp.cwd("/tsg_sa/TSG_SA/TSGS_12/Docs/")  # Navigate to the target folder
    print("Connected successfully!")
    print("Files:", ftp.nlst())  # List files
except Exception as e:
    print(f"FTP error: {e}")
finally:
    pass