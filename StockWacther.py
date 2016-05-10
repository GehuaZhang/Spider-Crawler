# -*- coding:utf-8 -*-
#Aunthor: Gehua Zhang

import urllib,sys,time,os

def Input():
	print ''
	print '*'*50
	print 'Note: This program is for Chinese stock market, so the stock code must be choosen from China A-shares.'
	print '-'*30
	print 'Please enter the stock code, split by SPACE :'
	print 'For Example: 601988 000166 600021 600016'
	stockCode = raw_input(': ')
	allCode = stockCode.split()
	f = open('stkcd.txt','wr')
	for i in range(len(allCode)):
		f.write(allCode[i])
		f.write('\n')
	f.close

def title():
	temp="%- 10s %- 10s %- 10s %- 10s %- 10s %- 10s"
	print temp % ("Name","Current","Change","Open","High","Low")
	print '-'*65
def getstklib():
	f=open('stkcd.txt','r')
	stkcd=f.read()
	stkcd=stkcd.split(None)
	return stkcd

def getconfig():
	f=open('config.txt','r')
	f=f.read()
	f=f.split(None)
	return f

def filter():
	f=open('stkcd.txt','r')
	stkcd=f.read()
	f.close()
	f=open('stkcd.txt','w')
	stkcd=stkcd.split(None)
	for i in range(len(stkcd)-1,-1,-1):
		if stkcd[i][0]=='0' or stkcd[i][0]=='3':
			temp='sz'+stkcd[i]
		elif stkcd[i][0]=='6':
			temp='sh'+stkcd[i]
		else:
			temp=stkcd[i]
		stkcd[i]=temp
		url='http://hq.sinajs.cn/list='+temp
		temp=urllib.urlopen(url)
		html=temp.read()
		temp=html.split(',')
		if len(temp)==33:
			f.write(stkcd[i]+'\n')

class stock:
	def geturl(self,a):
		if a[0]=='0' or a[0]=='3':
			temp='sz'+a
		elif a[0]=='6':
			temp='sh'+a
		else:
			temp=a
		self.url='http://hq.sinajs.cn/list='+temp
		self.code=temp[2:]

	def gethtml(self):
		temp=urllib.urlopen(self.url)
		html=temp.read()
		temp=html.split(',')
		return temp

	def getinfo(self):
		temp=self.gethtml()
		self.name=temp[0][21:].decode('gbk').encode('utf-8')
		self.open=temp[1]
		self.yestday=temp[2]

	def initia(self,a):
		self.geturl(a)
		self.getinfo()

	def getquote(self):
		temp=self.gethtml()
		self.current=temp[3]
		self.high=temp[4]
		self.low=temp[5]
		self.change=str((float(self.current)/float(self.yestday)-1)*100)[0:5]+'%'
		self.time=temp[31]#+' '+temp[32]

	def getvol(self):
		temp=self.gethtml()
		self.bidprice=temp[11:20:2] #buy1 to buy5
		self.askprice=temp[21:30:2] #sell1 to sell5
		self.bidvol=temp[10:19:2]
		self.askvol=temp[20:29:2]
		self.vol=temp[9]

	def printquote(self):
		_format="%- 10s %- 10s %- 10s %- 10s %- 10s %- 10s"
		print _format % (self.name,self.current,self.change,\
			self.open,self.high,self.low)
		print '-'*65

	def record(self):		
		filename=time.strftime('%Y-%m-%d')+'_'+self.code+'.txt'
		f=open(filename,'a')
		f.write(self.time+' ')
		f.write(self.current+' ')
		f.write(self.change+' ')
		f.write(self.open+' ')
		f.write(self.high+' ')
		f.write(self.low+' ')
		# self.getvol()
		# for i in range(5):
		# 	f.write(self.bidprice[i]+' ')
		# 	f.write(self.bidvol[i]+' ')
		# for i in range(5):
		# 	f.write(self.askprice[i]+' ')
		# 	f.write(self.askvol[i]+' ')
		f.write("\n")
		f.close

Input()

filter()
config=getconfig()
freq=float(config[0][5:])
stklib=getstklib()
ls=len(stklib)
lib=['none']*ls
for i in range(ls):	
 	temp='lib['+str(i)+']'+'='+'stock()'
	exec(temp)
	lib[i].initia(stklib[i])


while True:
	#ii=os.system('cls')

	title()
	for i in range(ls):
		lib[i].getquote()
		lib[i].printquote()
		#lib[i].record()
	print " "*40+"Time:"+time.strftime('%Y-%m-%d %H:%M:%S')


	time.sleep(freq)
