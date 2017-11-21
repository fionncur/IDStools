# Import modules
import os, smtplib, fnmatch, re, pwd
from email.mime.text import MIMEText
import datetime as dt

# Present time and previous time to inquire
now = dt.datetime.now()
ago = now-dt.timedelta(minutes=1)

# Files to exclude in the recursive search
#includes = ['*.watcher']
includes = ['*']
excludes = ['*~','*.o']

# Transform glob patterns to regular expressions
includes = r'|'.join([fnmatch.translate(x) for x in includes])
excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

# Global folder where to search for modifications
scenario_folder = '/work/imas/shared/iterdb/3'

# Recursive search in the scenario folder of the file(s) that have changed
msg_per_file = []
msg_per_watcher_file = []
for root,dirs,files in os.walk(scenario_folder):  

    # Exclude/include files
    files = [f for f in files if not re.match(excludes, f)]
    files = [f for f in files if re.match(includes, f)]

    # Loop on selected files\
    for fname in files:

        # Absolute path
        fullpathfile = os.path.join(root, fname)

        # To ignore symlinks
        if os.path.isfile(fullpathfile):

            # Take actions only if the file has recently been modified
            st = os.stat(fullpathfile)
            mtime = dt.datetime.fromtimestamp(st.st_mtime)
            if mtime > ago:
                owner = pwd.getpwuid(os.stat(fullpathfile).st_uid).pw_name
                if fullpathfile.endswith('.watcher'):
                    msgfile = '\n'
                    msgfile = 'The WATCHER file %s has been modified on %s.\n \n'%(fullpathfile, mtime)
                    msgfile = msgfile + '----> Please update the related watcher maling list.\n \n'
                    msg_per_watcher_file.append(msgfile)
                    msg_per_watcher_file.append('----> New list of watchers:\n')
                    msg_per_watcher_file.append(os.popen('cat '+fullpathfile).read())
                    
                else:
                    msgfile = '- The file %s has been added or modified on %s by %s \n'%(fullpathfile, mtime, owner)
                    msg_per_file.append(msgfile)

# Configure sender and recipient(s)
me  = 'noreply@iter.org' # sender
you = ['mireille.schneider@iter.org','simon.pinches@iter.org'] # recipient
#you = ['mireille.schneider@iter.org'] # recipient

# If a file has changed, send an email
if len(msg_per_file) > 0:

    # Message to be sent
    message = ''
    for i in range(len(msg_per_file)):
        message = message + msg_per_file[i]
    
    # Convert the text to something that can be sent by email
    msg = MIMEText(message)
    
    # E-mail fields
    msg['Subject'] = 'File(s) has/have been added or updated in the scenario folder'
    msg['From'] = me
    msg['To'] = ", ".join(you)

    # Send the message via our own SMTP server
    s = smtplib.SMTP('localhost')
    s.sendmail(me, you, msg.as_string())
    s.quit()

# Specific treatement of watcher files
if len(msg_per_watcher_file) > 0:

    # Message to be sent
    message = ''
    for i in range(len(msg_per_watcher_file)):
        message = message + msg_per_watcher_file[i]
    
    # Convert the text to somethimg that can be sent by email
    msg = MIMEText(message)
    
    # E-mail fields
    msg['Subject'] = 'A WATCHER file has been updated!'
    msg['From'] = me
    msg['To'] = ", ".join(you)

    # Send the message via our own SMTP server
    s = smtplib.SMTP('localhost')
    s.sendmail(me, you, msg.as_string())
    s.quit()

