# "Continous Integration" Script
import pysvn 
import commands
import smtplib


def notify_failure(msg_body):
  smtpserver = 'localhost'
  smtpport = 25
  
  toaddrs = ['fernando@popego.com', 'mariano@popego.com', 'victor@popego.com', 'manuel@popego.com', 'santiago@popego.com']
  fromaddr = 'noreply@popego.com'

  # Add the From: and To: headers at the start!
  msg = ("From: %s\r\nTo: %s\r\nSubject: [Popego-CI] Test Failure :(\r\n\r\n"
         % (fromaddr, ", ".join(toaddrs)))
  msg = msg + msg_body
  
  server = smtplib.SMTP(smtpserver, smtpport)
  #server.set_debuglevel(1)
  smtpresult = server.sendmail(fromaddr, toaddrs, msg)
  server.quit()
  
  if smtpresult:
      errstr = ""
      for recip in smtpresult.keys():
          errstr = """Could not delivery mail to: %s
  
  Server said: %s
  %s
  
  %s""" % (recip, smtpresult[recip][0], smtpresult[recip][1], errstr)
      raise smtplib.SMTPException, errstr


# Actualizamos el repo
client = pysvn.Client()
print "Updating sources..."
rev = client.update('../..')

# Corremos los test
print "Running Tests..."
cmd = '(cd ..; nosetests popserver/tests)'
(exitstatus, outtext) = commands.getstatusoutput(cmd)

cmd2 = '(cd ../..; nosetests webapitests)'
(exitstatus2, outtext2) = commands.getstatusoutput(cmd2)

# Notificamos la falla
if exitstatus != 0:
  msg_body = 'Tests Failed on revision %s\n\n' % rev[0].number
  msg_body = msg_body + outtext
  print msg_body
  notify_failure(msg_body)

if exitstatus2 != 0:
  msg_body = 'Webapitests Failed on revision %s\n\n' % rev[0].number
  msg_body = msg_body + outtext2
  print msg_body
  notify_failure(msg_body)

if exitstatus != 0 and exitstatus2 != 0:
  print "All tests run successfully"
