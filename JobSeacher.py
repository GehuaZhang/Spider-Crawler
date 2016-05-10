#!/usr/bin/python
# -*- coding:utf-8 -*-
#Author: Gehua Zhang

import urllib
import urllib2
import re
import webbrowser
import cookielib
import time
import datetime
import wx
import os
import sys

global WXPrint
WXPrint = []

class JobInfo:

	#Login and save Cookies
	def __init__(self,name,password):
		self.loginUrl = 'https://baruch-csm.symplicity.com/students/'
		self.starrInfoUrl = 'https://baruch-csm.symplicity.com/students/index.php?s=jobs&ss=jobs&sss=&mode=list&_ksl=1'
		#'https://baruch-csm.symplicity.com/students/index.php?s=jobs&ss=jobs&sss=&mode=list&_ksl=1'
		self.headers = {'Referer':'https://baruch-csm.symplicity.com/students/',
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}
		self.cookie = cookielib.CookieJar()
		self.postdata = urllib.urlencode({'username':str(name),'password':str(password)})
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))

	#Grab info
	def getPage(self):
		self.request = urllib2.Request(url = self.loginUrl, data = self.postdata, headers = self.headers) 
		
		result = self.opener.open(self.request)
		result = self.opener.open(self.starrInfoUrl)
		return result.read()
	
	#Regular Expression Matching
	def getInfo(self):

		content = self.getPage()
		pattern_1 = re.compile('<a.*?href=".*?ss=jobs".*?class="ListPrimaryLink">(.*?)</a>',re.S)
		pattern_employer = re.compile('s=employers&ss=list&mode.*?class="ListPrimaryLink">(.*?)</a>',re.S)
		pattern_2 = re.compile('<div.*?class="list-secondary-action">\t        \n\t\t\t\t\t(.*?)\n\t\t\t\t</div>',re.S)
		pattern_Type = re.compile('</div>.*?<div.*?class="list-data-columns">\n\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t(.*?)\n\t\t\t\t</div>',re.S)
		pattern_3 = re.compile('<div.*?class="list-item-title">.*?<a.*?href="(.*?)".*?class="ListPrimaryLink">.*?</a>',re.S)

		self.items_1 = re.findall(pattern_1,content)
		self.items_employer = re.findall(pattern_employer,content)
		self.items_2 = re.findall(pattern_2,content)
		self.items_Type = re.findall(pattern_Type,content)
		global items_3
		items_3 = re.findall(pattern_3,content)

		self.deadLine = [ ]
		for item in self.items_2:
			self.deadLine.append(item + ' 2016')

		self.formatDeadLine = [ ]
		self.nowTime = datetime.datetime.now()
		self.timeLeft = [ ]

		for m in range (0,len(self.items_1)):
			self.formatDeadLine.append(datetime.datetime.strptime(self.deadLine[m],'%b %d %Y'))
			self.timeLeft.append((self.nowTime-self.formatDeadLine[m]).days+1)
			m = m+1

		for m in range (0,len(self.items_1)):
			WXPrint.append(str(self.timeLeft[m]) + " days left - "+str(self.items_Type[m])+' - '+str(self.items_1[m])+" - Employer : "+str(self.items_employer[m]))


class LoginGui(wx.Dialog):

	def __init__(self):
		wx.Dialog.__init__(self,None,title='Job Search',size=(350,130))
		panel=wx.Panel(self)

		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

		if os.path.isfile('LogInFormation.txt'):
			self.openTxtValue()
		else:
			self.txtInfo = ['Enter Username','']

		username_label=wx.StaticText(self,label='Username:')
		self.username_input=wx.TextCtrl(self,value=str(self.txtInfo[0]))
		self.setParallel(username_label,self.username_input)

		password_label=wx.StaticText(self,label='Password:')
		self.password_input=wx.TextCtrl(self,value=str(self.txtInfo[1]),style=wx.TE_PASSWORD)
		self.setParallel(password_label,self.password_input)

		ok_button = wx.Button(self,label='OK')
		cancel_button = wx.Button(self,label='Cancel')
		
		buttonSizer.Add(ok_button, 0, wx.CENTER|wx.ALL, 5)
		buttonSizer.Add(cancel_button, 0, wx.CENTER|wx.ALL, 5)

		ok_button.Bind(wx.EVT_BUTTON,self.Execute)
		cancel_button.Bind(wx.EVT_BUTTON,self.closeWindow)
		#self.Bind(wx.EVT_TEXT_ENTER,self.Execute)

		self.mainSizer.Add(buttonSizer, 0, wx.CENTER)
		self.SetSizer(self.mainSizer)

		self.Centre()

	def setParallel(self,labelInfo,inputInfo):
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(labelInfo, 0, wx.ALL|wx.CENTER, 5)
		sizer.Add(inputInfo, 1, wx.EXPAND|wx.ALL, 5)
		self.mainSizer.Add(sizer, 0, wx.EXPAND)


	def storeValue(self,event):
		self.k=self.username_input.GetValue()
		self.m=self.password_input.GetValue()
		if self.k and self.m != None:
			self.Close()
			storeInTxt = open('LogInFormation.txt','wb')
			self.Stored = True
			storeInTxt.write('username:'+self.k+'<>'+'password:'+self.m+'<>')
			storeInTxt.close()
		return self.k,self.m


	def openTxtValue(self):
		f = open('LogInFormation.txt')
		fileRead = f.read()
		patt = r'username:(.*?)<>password:(.*?)<>'
		textxxx=re.findall(patt,fileRead)
		self.txtInfo = []
		for i in (0,1):
			self.txtInfo.append(textxxx[0][i])
		f.close()
		return self.txtInfo


	def closeWindow(self,event):
		sys.exit()


	def Execute(self,event):
		TransLogInfo = JobInfo(self.storeValue(1)[0],self.storeValue(1)[1])
		TransLogInfo.getInfo()
		originWeb = 'https://baruch-csm.symplicity.com/students/index.php'
		if WXPrint == []:			
			warnDlg=wx.MessageDialog(None,message="Wrong Username or Password, Please Login Again!", caption="Sorry!", style= wx.OK | wx.ICON_WARNING)
			warnDlg.ShowModal()
			JobSearchGui()
		elif WXPrint != []:
			self.Centre()
			choiceList=wx.SingleChoiceDialog(None,"Application Time Left - Job Type -Job Title - Employer \n Double-Click to View Details","Job Search Result",WXPrint)
			if choiceList.ShowModal()==wx.ID_OK:
				choiceIndex = choiceList.GetSelection()
				targetWeb=originWeb+items_3[int(choiceIndex)]
				webbrowser.open(targetWeb)
			else:
				sys.exit(0)

class JobSearchGui(wx.Frame):

	def __init__(self):
		wx.Frame.__init__(self,None,title="Job Search Result",size=(700,300))

		dlg=LoginGui()
		dlg.ShowModal()


if __name__ == "__main__":
    app = wx.App(False)
    frame = JobSearchGui()
    app.MainLoop()

