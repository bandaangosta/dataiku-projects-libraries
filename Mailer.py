import dataiku
import os
import mailer
import re

EMAIL_REGEX = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
REPORT_FILE_NAME = 'Default-dashboard.pdf'

# Get reports folder data and predefined e-mail recipients
projectConfig = dataiku.get_custom_variables()
reportFolder = dataiku.Folder(projectConfig["REPORT_FOLDER_ID"])
reportFolderInfo = reportFolder.get_info()
reportFolderAbsPath = reportFolderInfo['path']

def sendReport(subject,
               body,
               recipientList = projectConfig["REPORT_RECIPIENTS"].split(','),
               pathToReport = os.path.join(reportFolderAbsPath, REPORT_FILE_NAME),
               bodyAlt = ''):

    if isinstance(recipientList, list):
        checkedList = []
        for recipient in recipientList:
            if re.match(EMAIL_REGEX, recipient.strip()) is None:
                print('Invalid recipient e-mail address: {}'.format(recipient))
            else:
                checkedList.append(recipient.strip())
        recipientList = checkedList
    else:
        if re.match(EMAIL_REGEX, recipientList) is None:
            print('Invalid recipient e-mail address: {}'.format(recipientList))
            return False

    sender = mailer.Mailer(projectConfig["EMAIL_SERVER"])
    message = mailer.Message(From='projectConfig["EMAIL_FROM"],
                             To=recipientList,
                             Subject=subject)
    message.attach(pathToReport)
    message.Html = body
    message.Body = bodyAlt
    sender.send(message)
    return True
