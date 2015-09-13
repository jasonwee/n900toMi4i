#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
import sqlite3
import os.path
import csv
from datetime import datetime
 
if len(sys.argv) != 3:
  print ""
  print "Usage:"
  print "%s [path to el-v1.db] [path to csv file]" % sys.argv[0]
  print ""
  sys.exit(1)
 
dbFileName  = sys.argv[1].strip()
csvFileName = sys.argv[2].strip()
 
if not os.path.exists(dbFileName):
  print ""
  print "Error:"
  print "Could not open '%s'" % dbFileName
  print ""
  sys.exit(1)
 
with sqlite3.connect(dbFileName) as connection, open(csvFileName, 'wb') as csvFd:
  cursor = connection.cursor()
  writer = csv.writer(csvFd, delimiter = ',', quotechar = '"', quoting =
                      csv.QUOTE_MINIMAL, lineterminator='\n')
  writer.writerow(["Date/Time","Number","Name","Type","Message","thread_id","person","date","date_sent","protocol","read","status","type","reply_path_present","subject","service_center","locked","error_code","seen","timed","deleted","sync_state","marker","source","bind_id","mx_status","mx_id","out_time","account","sim_id","block_type","advanced_seen"])
 
  sql = "SELECT start_time, remote_uid, free_text, outgoing, storage_time, end_time FROM Events WHERE event_type_id = 7"
  for record in cursor.execute(sql):
    startTime, phoneNumber, textMessage, outGoing, storageTime, endTime = record
     
    startDateTime = datetime.fromtimestamp(startTime).strftime('%b %d, %Y %H:%M:%S');
    phoneNumber   = phoneNumber.encode('utf-8')
    if textMessage:
        textMessage   = textMessage.encode('utf-8')

    # n900 1 android Sent
    # n900 0 android Received
    messageType='Received'
    messageTypeN='1'
    protocol=0
    status = -1
    replyPathPresent=0
    serviceCenter=60120000015
    if outGoing == 1:
        messageType='Sent'
        protocol='null'
        status = 0
        messageTypeN=2
        replyPathPresent='null'
        serviceCenter='null'

    threadId=1

    person='null'

    storageTime=storageTime * 1000

    dateSent=endTime * 1000

    read=1

    subject='null'

    locked=0

    errorCode=0

    seen=1

    timed=0

    deleted=0

    syncState=0

    marker=0

    source='null'

    bindID=0

    mxStatus=0

    mxID='null'

    outTime=0

    account='null'

    simID=1

    blockType=0

    advancedSeen=3
 
    #writer.writerow([startTime, startDateTime, phoneNumber, textMessage])
    writer.writerow([startDateTime, phoneNumber, phoneNumber, messageType, 
                     textMessage, threadId, person, storageTime, dateSent,
                     protocol, read, status, messageTypeN, replyPathPresent,
                     subject, serviceCenter, locked, errorCode, seen, timed,
                     deleted, syncState, marker, source, bindID, mxStatus,
                     mxID, outTime, account, simID, blockType, advancedSeen])
 
connection.close()
csvFd.close()

