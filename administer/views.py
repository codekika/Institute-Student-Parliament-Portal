from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.contrib import messages
import MySQLdb
import datetime
from dateutil.parser import parse as parse_date
db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
cur=db.cursor()

def administer(request):
	if request.session.has_key('admin'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		query="select * from notices natural join committee"
		cur.execute(query)
		m=cur.fetchall()
		return render(request,"administer/homee.html",{"user_id":'admin','newsb':m})
	return render(request,'administer/login.html')

def adminlogin(request):
	email_id=request.POST.get('email')
	password=request.POST.get('pwd')
	print email_id,password
	if email_id and password:
		if email_id=='admin' and password=='qwerty123':
			request.session['admin']=1
			query="select * from notices natural join committee"
			cur.execute(query)
			m=cur.fetchall()
			return render(request,"administer/homee.html",{"user_id":'admin','newsb':m})
		else:
			return render(request, 'administer/login.html',{'messagee':'Invalid Details'})	
	else:
		return render(request, 'administer/login.html')

def adminlogout(request):
	if request.session.has_key('admin'):
		del request.session['admin']
		return render(request, 'administer/login.html')	
	return render(request, 'administer/login.html')	

def adminhome(request):
	if request.session.has_key('admin'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		query="select * from notices natural join committee"
		cur.execute(query)
		m=cur.fetchall()
		return render(request,"administer/homee.html",{"user_id":'admin','newsb':m})
	else:
		return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})	

def admingrievance(request):
	if request.session.has_key('admin'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		query="select * from grievance natural join committee"
		cur.execute(query)
		grievances=cur.fetchall()
		return render(request,'administer/grievances.html',{'grievances':grievances})
	return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})

def delete(request,pk):
	if request.session.has_key('admin'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		query="delete from grievance where id='%s'"%(pk)
		cur.execute(query)
		db.commit()
		return redirect("admingrievance")
	return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})

def adminsuggestion(request):
	db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
	cur=db.cursor()
	if request.session.has_key('admin'):
		query="select * from suggestion natural join committee"
		cur.execute(query)
		suggestions=cur.fetchall()
		return render(request,'administer/suggestions.html',{'suggestions':suggestions	})
	return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})

def deletesuggestion(request,pk):
	if request.session.has_key('admin'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		query="delete from suggestion where id='%s'"%(pk)
		cur.execute(query)
		db.commit()
		return redirect("adminsuggestion")
	return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})	

def adminelections(request):
	if request.session.has_key('admin'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		query="select * from election where startdt>curdate()";
		cur.execute(query)
		futu=cur.fetchall()
		query="select * from election where enddt<curdate()";
		cur.execute(query)
		pas=cur.fetchall()
		query="select * from election where enddt>=curdate() and startdt<=curdate()";
		cur.execute(query)
		pres=cur.fetchall()
		return render(request, 'administer/election.html',{'cur_election':pres,'pas_election':pas,'fut_election':futu})
	return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})	

def deleteelection(request,pk):
	if request.session.has_key('admin'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		query="delete from election where id='%s'"%(pk)
		cur.execute(query)
		db.commit()
		return redirect("adminelections")
	return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})	

def elecresults(request,pk):
	if request.session.has_key('admin'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		query="select * from candidates where electionid='%s' order by votes desc"%(pk)
		cur.execute(query)
		candidates=cur.fetchall()
		return render(request,'administer/eleresults.html',{'polls':candidates})
	else:	
		return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})

def addelection(request):
	if request.session.has_key('admin'):
		name=request.POST.get('desc')
		startdt=request.POST.get('stdate')
		enddt=request.POST.get('enddate')
		ishostel=request.POST.get('hop')
		startdt=datetime.datetime.strptime(startdt, '%Y-%m-%d').date()
		enddt=datetime.datetime.strptime(enddt, '%Y-%m-%d').date()
		if startdt>=datetime.date.today() and enddt>=startdt:
			db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
			cur=db.cursor()
			if ishostel=='1':
				hostel=request.POST.get('hostel')
				print hostel
				query="insert into election(descr,startdt,enddt,ishostel,type) values('%s','%s','%s',1,'%s')"%(name,startdt,enddt,hostel)
				cur.execute(query)
				db.commit()
				query="select max(id) from election"
				cur.execute(query)
				electionid=cur.fetchone()
				electionid=int(electionid[0])
				query="select type from election where id='%d'"%(electionid)
				cur.execute(query)
				hostel=cur.fetchone()
				query="select rollno,hostel from student"
				cur.execute(query)
				voters=cur.fetchall()
				for i in voters:
					print hostel,i
					if i[1]==hostel[0]:
						print i,hostel
						query="insert into voters(voter,electionid) values('%d','%d')"%(int(i[0]),electionid)
						cur.execute(query)
						db.commit()	
			else:
				year=request.POST.get('year')
				print year
				query="insert into election(descr,startdt,enddt,ishostel,type) values('%s','%s','%s',0,'%s')"%(name,startdt,enddt,year)
				cur.execute(query)
				db.commit()
				query="select max(id) from election"
				cur.execute(query)
				electionid=cur.fetchone()
				electionid=int(electionid[0])
				query="select type from election where id='%d'"%(electionid)
				cur.execute(query)
				hostel=cur.fetchone()
				query="select rollno,year from student"
				cur.execute(query)
				voters=cur.fetchall()
				for i in voters:
					print i[1], year[0]
					if i[1]==int(year[0]):
						query="insert into voters(voter,electionid) values('%d','%d')"%(int(i[0]),electionid)
						cur.execute(query)
						db.commit()	
			query="select max(id) from election"
			cur.execute(query)
			electionid=cur.fetchone()
			electionid=int(electionid[0])
			query="select * from election where startdt>curdate()";
			cur.execute(query)
			futu=cur.fetchall()
			query="select * from election where enddt<curdate()";
			cur.execute(query)
			pas=cur.fetchall()
			query="select * from election where enddt>=curdate() and startdt<=curdate()";
			cur.execute(query)
			pres=cur.fetchall()
			return render(request, 'administer/election.html',{'cur_election':pres,'pas_election':pas,'fut_election':futu,'messagee':'Successfully added election!!'})
		else:
			db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
			cur=db.cursor()
			query="select * from election where enddt<curdate()";
			cur.execute(query)
			pas=cur.fetchall()
			query="select * from election where enddt>=curdate() and startdt<=curdate()";
			cur.execute(query)
			pres=cur.fetchall()
			query="select rollno from student"
			cur.execute(query)
			query="select * from election where startdt>curdate()";
			cur.execute(query)
			futu=cur.fetchall()
			voters=cur.fetchall()
			return render(request, 'administer/election.html',{'cur_election':pres,'pas_election':pas,'fut_election':futu,'messagee':"Invalid details. Start date should be after today's date and end date should be greater or equal to start date!!"})		
	else:
		return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})

def candidates(request,pk):
	if request.session.has_key('admin'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		query="select * from student,candidates where electionid='%s' and cand_id=rollno" %(pk)
		cur.execute(query)
		candidates=cur.fetchall()
		return render(request,'administer/candidates.html',{'candidates':candidates})
	else:
		return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})	

def adminpolls(request):
	if request.session.has_key('admin'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		query="select * from polls natural join committee"
		cur.execute(query)
		candidates=cur.fetchall()
		return render(request,'administer/polls.html',{'polls':candidates})
	else:
		return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})

def deletepolls(request,pk):
	if request.session.has_key('admin'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		query="delete from polls where id='%s'"%(pk)
		cur.execute(query)
		db.commit()
		return redirect("adminpolls")
	return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})

def pollresults(request,pk):
	if request.session.has_key('admin'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		query="select * from polloption where pollid='%s' order by votes desc"%(pk)
		cur.execute(query)
		candidates=cur.fetchall()
		return render(request,'administer/pollresults.html',{'polls':candidates})
	else:
		return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})

def addpolls(request):
	if request.session.has_key('admin'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		desc=request.POST.get('desc')
		committee=request.POST.get('committee')
		query="select committeeid from committee where name='%s'"%(committee)
		cur.execute(query)
		committee=cur.fetchone()
		committee=int(committee[0])
		query="insert into polls(committeeid,description) values('%d','%s')"%(committee,desc)
		cur.execute(query)
		db.commit()
		query="select max(id) from polls"
		cur.execute(query)
		pollid=cur.fetchone()
		pollid=int(pollid[0])
		query="select rollno from student"
		cur.execute(query)
		voters=cur.fetchall()
		option1=request.POST.get('option1')
		option2=request.POST.get('option2')
		query="insert into polloption(answer,votes,pollid) values('%s',0,'%d')"%(option1,pollid)
		cur.execute(query)
		db.commit()
		query="insert into polloption(answer,votes,pollid) values('%s',0,'%d')"%(option2,pollid)
		cur.execute(query)
		db.commit()
		for i in voters:
			query="insert into pollers(poller,poll) values('%d','%d')"%(int(i[0]),pollid)
			cur.execute(query)
			db.commit()
		return render(request,'administer/addoption.html',{'polls':pollid})
	else:
		return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})

def addoptions(request,pk):
	if request.session.has_key('admin'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		ans=request.POST.get('option')
		if ans:
			query="insert into polloption(answer,votes,pollid) values('%s',0,'%d')"%(ans,int(pk))
			cur.execute(query)
			db.commit()
			return render(request,'administer/addoption.html',{'polls':pk})
	else:
		return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})

def addnews(request):
	if request.session.has_key('admin'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		ans=request.POST.get('desc')
		committee=request.POST.get('committee')
		if ans and committee:
			query="select committeeid from committee where name='%s'"%(committee)
			cur.execute(query)
			committee=cur.fetchone()
			committee=int(committee[0])
			query="insert into notices(notice,committeeid) values('%s','%s')"%(ans,committee)
			cur.execute(query)
			db.commit()
			query="select * from notices"

			return redirect("adminhome")
	else:
		return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})

def deletenews(request,pk):
	if request.session.has_key('admin'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		query="delete from notices where id='%s'"%(pk)
		cur.execute(query)
		db.commit()
		return redirect("administer")
	return render(request,'administer/login.html',{'messagee':"Logged in people only can view. Login"})
