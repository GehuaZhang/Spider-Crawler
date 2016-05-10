#!/usr/bin/python
# -*- coding:utf-8 -*-
#Author: Gehua Zhang

import urllib	
import urllib2
import re
import webbrowser
import cookielib


#********************************************************************

print ' '
logininfo = raw_input('Enter Your CUNYfirst Username: ')
passwordinfo = raw_input('Enter Your CUNYfirst password: ')
print 'Please Wait, Processing your request..'
postdata = urllib.urlencode({
'login':logininfo,
'password':passwordinfo})

#——————————————————————————————————————————————————————————————————————————————————————————————————————————————
#Login and save Cookies

loginUrl = 'https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/EMPL/h/?tab=DEFAULT'
AfterLoginUrl = 'https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_MY_CRSEHIST.GBL?PORTALPARAM_PTCNAV=HC_SSS_MY_CRSEHIST_GBL&amp;EOPP.SCNode=HRMS&amp;EOPP.SCPortal=EMPLOYEE&amp;EOPP.SCName=CO_EMPLOYEE_SELF_SERVICE&amp;EOPP.SCLabel=Self%20Service&amp;EOPP.SCPTfname=CO_EMPLOYEE_SELF_SERVICE&amp;FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HCCC_ACADEMIC_RECORDS.HC_SSS_MY_CRSEHIST_GBL&amp;IsFolder=false&amp;PortalActualURL=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_MY_CRSEHIST.GBL&amp;PortalContentURL=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_MY_CRSEHIST.GBL&amp;PortalContentProvider=HRMS&amp;PortalCRefLabel=My%20Course%20History&amp;PortalRegistryName=EMPLOYEE&amp;PortalServletURI=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsp%2fcnyhcprd%2f&amp;PortalURI=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd%2f&amp;PortalHostNode=HRMS&amp;NoCrumbs=yes&amp;PortalKeyStruct=yes'
headers = {'Referer':'https://home.cunyfirst.cuny.edu/oam/Portal_Login1.html',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}
cookies = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))

#——————————————————————————————————————————————————————————————————————————————————————————————————————————————
#Get page info

request = urllib2.Request(url = loginUrl,data = postdata, headers = headers) 
result = opener.open(request)
result = opener.open(AfterLoginUrl)
content = result.read()#.decode('utf-8')

#——————————————————————————————————————————————————————————————————————————————————————————————————————————————
#Regular Expression

pattern = re.compile("<span.*?class=.*?PSEDITBOX_DISPONLY.*?id='CRSE_NAME.*?'>(.*?)</span>.*?<span.*?class=.*?PSEDITBOX_DISPONLY.*?id='CRSE_GRADE.*?'>(.*?)</span>.*?<span.*?class=.*?PSEDITBOX_DISPONLY.*?id='CRSE_UNITS.*?'>(.*?)</span>",re.S)
items = re.findall(pattern,content)
for item in items:
	print item[0]+"  "+item[1]+"  "+item[2]

#——————————————————————————————————————————————————————————————————————————————————————————————————————————————
#Grab GPA and credit weights

length = len(items)
allGrade = [ ]
credit = [ ]
for item in items:
	allGrade.append(item[1])
	credit.append(item[2])
print " "


#——————————————————————————————————————————————————————————————————————————————————————————————————————————————
#Calculate Weighted GPA

GPA = 0
allCredit = 0
for i in range(length):
	if allGrade[i] == 'A':
		GPA=GPA+4.0*float(credit[i])
		allCredit = float(credit[i])+allCredit
	elif allGrade[i] == 'A-':
		GPA=GPA+3.7*float(credit[i])
		allCredit = float(credit[i])+allCredit
	elif allGrade[i] == 'B+':
		GPA=GPA+3.3*float(credit[i])
		allCredit = float(credit[i])+allCredit
	elif allGrade[i] == 'B':
		GPA=GPA+3.0*float(credit[i])
		allCredit = float(credit[i])+allCredit
	elif allGrade[i] == 'B-':
		GPA=GPA+2.7*float(credit[i])
		allCredit = float(credit[i])+allCredit
	elif allGrade[i] == 'C+':
		GPA=GPA+2.3*float(credit[i])
		allCredit = float(credit[i])+allCredit
	elif allGrade[i] == 'C':
		GPA=GPA+2.0*float(credit[i])
		allCredit = float(credit[i])+allCredit
	elif allGrade[i] == 'C-':
		GPA=GPA+1.7*float(credit[i])
		allCredit = float(credit[i])+allCredit
	elif allGrade[i] == 'D+':
		GPA=GPA+1.3*float(credit[i])
		allCredit = float(credit[i])+allCredit
	elif allGrade[i] == 'D':
		GPA=GPA+1.0*float(credit[i])
		allCredit = float(credit[i])+allCredit
	elif allGrade[i] == 'F':
		GPA=GPA+0.0*float(credit[i])
		allCredit = float(credit[i])+allCredit

avgGPA = 0
avgGPA = round(GPA/allCredit,3)

print "Your GPA is:" + "  "+ str(avgGPA)



