from django.shortcuts import render,redirect
from django.contrib import messages
import MySQLdb;
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
import hashlib


db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
cur=db.cursor()
# Create your views here.
def home(request):
	if request.session.has_key('user_id'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		rollno=request.session.get('user_id')
		query="select * from notices natural join committee"
		cur.execute(query)
		m=cur.fetchall()
		return render(request, 'blog/homee.html',{'user_id':rollno,'newsb':m})
	else:
		return render(request,'blog/aboutus.html')

def aboutus(request):
	if request.session.has_key('user_id'):
		rollno=request.session.get('user_id')
		return render(request, 'blog/aboutus.html',{'user_id':rollno})
	else:
		return render(request,'blog/aboutus.html')

def grievances(request):
	if request.session.has_key('user_id'):
		grievance=request.POST.get('comment')
		committee=request.POST.get('committee')
		rollno=request.session.get('user_id')
		if grievance and committee:
			rollno=request.session.get('user_id')
			query="select committeeid from committee where name='%s'"%(committee)
			cur.execute(query)
			committee=cur.fetchone()
			committee=int(committee[0])
			query="insert into grievance(committeeid,data,filer) values ('%d','%s','%d')" %(committee,grievance,rollno)
			cur.execute(query)
			db.commit()
			return render(request, 'blog/grievances.html',{'messagee':"Successfully submitted grievance!!",'user_id':rollno})
		return render(request, 'blog/grievances.html',{'user_id':rollno})
	else:
		return render(request,'blog/login.html',{'messagee':'Only Logged-in students can view. Log-In'})

def polls(request):
	if request.session.has_key('user_id'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		rollno=request.session.get('user_id')
		query="select * from polls natural join committee"
		cur.execute(query)
		l=cur.fetchall()
		return render(request, 'blog/polls.html',{'user_id':rollno,'polls':l})
	else:
		return render(request,'blog/login.html',{'messagee':'Only Logged-in students can view. Log-In'})

def suggestions(request):
	if request.session.has_key('user_id'):
		suggestion=request.POST.get('comment')
		committee=request.POST.get('committee')
		rollno=request.session.get('user_id')
		print suggestion,committee
		if suggestion and committee:
			rollno=request.session.get('user_id')
			query="select committeeid from committee where name='%s'"%(committee)
			cur.execute(query)
			committee=cur.fetchone()
			print committee
			committee=int(committee[0])
			query="insert into suggestion(committeeid,data,filer) values ('%d','%s','%d')" %(committee,suggestion,rollno)
			cur.execute(query)
			db.commit()
			return render(request, 'blog/suggestions.html',{'messagee':"Successfully submitted suggestion!!",'user_id':rollno})
		return render(request, 'blog/suggestions.html',{'user_id':rollno})
	else:
		return render(request,'blog/login.html',{'messagee':'Only Logged-in students can view. Log-In'})

def elections(request):
	if request.session.has_key('user_id'):	
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		rollno=request.session.get('user_id')
		query="select * from election where startdt>curdate()";
		cur.execute(query)
		futu=cur.fetchall()
		query="select * from election where enddt<curdate()";
		cur.execute(query)
		pas=cur.fetchall()
		query="select * from election where enddt>=curdate() and startdt<=curdate()";
		cur.execute(query)
		pres=cur.fetchall()
		return render(request, 'blog/election.html',{'user_id':rollno,'cur_election':pres,'pas_election':pas,'fut_election':futu})
	else:
		return render(request,'blog/login.html',{'messagee':'Only Logged-in students can view. Log-In'})

def elevote(request,pk):
	if request.session.has_key('user_id'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		rollno=request.session.get('user_id')
		query="select * from election where id='%s'"%(pk)
		cur.execute(query)
		election=cur.fetchone()
		query="select * from voters where electionid='%s'"%(pk)
		cur.execute(query)
		voters=cur.fetchall()
		for i in voters:
			if i[1]==rollno:
				query="select * from candidates where electionid='%s'"%(pk)
				cur.execute(query)
				candidates=cur.fetchall()
				return render(request,'blog/elevote.html',{'election':election,'options':candidates})
		return render(request,'blog/eledone.html',{'user_id':rollno,'messagee':"You have either voted or not eligible for voting!"})		
	else:
		return render(request,'blog/login.html',{'messagee':'Only Logged-in students can view. Log-In'})

def eledone(request,pk):
	if request.session.has_key('user_id'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		rollno=request.session.get('user_id')
		answer=request.POST.get('answers')
		if answer:
			query="update candidates set votes=votes+1  where electionid='%s' and id='%s'"%(pk,answer)
			cur.execute(query)
			db.commit()
			query="delete from voters where voter='%s' and electionid='%s'"%(rollno,pk)
			cur.execute(query)
			db.commit()
			return render(request,'blog/eledone.html',{'user_id':rollno,'messagee':'You have successfully voted!'})
		return render(request,'blog/eledone.html',{'user_id':rollno,'messagee':'You have either voted or not eligible for voting!'})
	else:
		return render(request,'blog/login.html',{'messagee':'Only Logged-in students can view. Log-In'})

def nominate(request,pk):
	if request.session.has_key('user_id'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		rollno=request.session.get('user_id')
		query="select * from candidates where electionid='%s'"%(pk)
		cur.execute(query)
		candidates=cur.fetchall()
		for i in candidates:
			print i[3],rollno
			if i[3]==rollno:
				return render(request,'blog/nominationdone.html',{'user_id':rollno,'messagee':'You have already nominated yourself for the election'})
		return render(request,'blog/nominate.html',{'user_id':rollno,'election':pk})
	else:
		return render(request,'blog/login.html',{'messagee':'Only Logged-in students can view. Log-In'})

def eleresults(request,pk):
	if request.session.has_key('user_id'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		rollno=request.session.get('user_id')
		query="select * from candidates where electionid='%s' order by votes desc"%(pk)
		cur.execute(query)
		candidates=cur.fetchall()
		return render(request,'blog/eleresults.html',{'user_id':rollno,'polls':candidates})
	else:
		return render(request,'blog/login.html',{'messagee':'Only Logged-in students can view. Log-In'})

def nominationdone(request,pk):
	if request.session.has_key('user_id'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		rollno=request.session.get('user_id')
		query="select * from student where rollno='%d'"%(int(rollno))
		cur.execute(query)
		student=cur.fetchone()
		query="select * from election where id='%d'"%(int(pk))
		cur.execute(query)
		election=cur.fetchone()
		query="select * from candidates where electionid='%d'"%(int(pk))
		cur.execute(query)
		candidates=cur.fetchall()
		for i in candidates:
			if i[3]==int(rollno):
				return render(request,'blog/nominationdone.html',{'user_id':rollno,'messagee':'You have already nominated yourself'})
		name=student[1]+' '+student[2]
		if rollno:
			if election[4]==1:
				if student[6]==election[5]:
					rollno=int(rollno)
					pk=int(pk)
					query="insert into candidates(name,votes,cand_id,electionid) values('%s',0,'%d','%d')"%(name,rollno,pk)
					cur.execute(query)
					db.commit()
					return render(request,'blog/nominationdone.html',{'user_id':rollno, 'messagee':"You have successfully registered yourself for the candidacy"})
				else:
					return render(request,'blog/nominationdone.html',{'user_id':rollno,'messagee':'You are not eligible for nominating yourself as you are not in the same year or hostel'})
			else:
				print election[5],student[4]
				if int(election[5])==student[4]:
					rollno=int(rollno)
					pk=int(pk)
					query="insert into candidates(name,votes,cand_id,electionid) values('%s',0,'%d','%d')"%(name,rollno,pk)
					cur.execute(query)
					db.commit()
					return render(request,'blog/nominationdone.html',{'user_id':rollno, 'messagee':"You have successfully registered yourself for the candidacy"})
				else:
					return render(request,'blog/nominationdone.html',{'user_id':rollno,'messagee':'You are not eligible for nominating yourself as you are not in the same year or hostel'})
		else:
			return render(request,'blog/nominationdone.html',{'user_id':rollno,'messagee':'Invalid Details! Nominations could not be filed!'})
	else:
		return render(request,'blog/login.html',{'messagee':'Only Logged-in students can view. Log-In'})

def poll(request, pk):
	if request.session.has_key('user_id'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		rollno=request.session.get('user_id')
		query="select * from polls where id='%s'"%(pk)
		cur.execute(query)
		l=cur.fetchone()
		query="select poller from pollers where poll='%s'"%(pk)
		cur.execute(query)
		p=cur.fetchall()
		for i in p:
			if i[0]==rollno:
				query="select answer from polloption where pollid='%s'"%(pk)
				cur.execute(query)
				m=cur.fetchall()
				return render(request, 'blog/poll.html',{'user_id':rollno,'poll': l,'options':m})
		return render(request,"blog/polldone.html",{'user_id':rollno,'messagee':'You have either voted or not eligible for voting'})
	else:
		return render(request,'blog/login.html',{'messagee':'Only Logged-in students can view. Log-In'})


def polldone(request,pk):
	if request.session.has_key('user_id'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		rollno=request.session.get('user_id')
		answer=request.POST.get('answers')
		if answer:
			print answer
			query="update polloption set votes=votes+1  where pollid='%s' and answer='%s'"%(pk,answer)
			cur.execute(query)
			db.commit()
			query="delete from pollers where poller='%s' and poll='%s'"%(rollno,pk)
			cur.execute(query)
			db.commit()
			return render(request,'blog/polldone.html',{'user_id':rollno,'messagee':'You have successfully voted'})
		return render(request,'blog/polldone.html',{'user_id':rollno,'messagee':'You have either voted or not eligible for voting'})
	else:
		return render(request,'blog/login.html',{'messagee':'Only Logged-in students can view. Log-In'})

def signup(request):
	if request.method == 'POST':
		email_id=request.POST.get('email')
		if email_id:
			if "@itbhu.ac.in" in email_id or "@iitbhu.ac.in" in email_id:
				current_site = get_current_site(request)
				message = render_to_string('acc_active_email.html', { 
				    'domain':current_site.domain,
				    'uid': urlsafe_base64_encode(force_bytes(email_id)),
				    'token': account_activation_token.make_token(email_id),
				})
				mail_subject = 'Activate your Parliament account.'
				to_email = email_id
				email = EmailMessage(mail_subject, message, to=[to_email])
				try:
					email.send()
					return render(request,'blog/signup.html',{'messagee':'You have to confirm your email id.'})	 
				except:
					return render(request,'blog/signup.html',{'messagee':'There is no network at the server side to send email!!'})
			else:
				return render(request,'blog/signup.html',{'messagee':'Only students with official Email-ID of IIT(BHU) can signup'})

def activate(request, uidb64,token):
	if request.session.has_key('user_id'):
		rollno=request.session.get('user_id')
		return render(request,'blog/homee.html',{'user_id':rollno,'messagee':'Logout from current account to activate other account!!'})
	else:
		uid = force_text(urlsafe_base64_decode(uidb64))
		uid=uid.encode('utf-8')
		if uid and account_activation_token.check_token(uid, token):
			return render(request,'blog/signup3.html',{'email':uid})
		else:
			return render(request,'blog/signup.html',{'messagee':'Account is not activated'})

def signup2(request):
	return render(request, 'blog/signup.html')

def signup3(request,pk):
	fname=request.POST.get('fname')
	sname=request.POST.get('sname')
	email_id=pk
	dept=request.POST.get('dept')
	hostel=request.POST.get('hostel')
	contact_no=(request.POST.get('pno'))
	rollno=(request.POST.get('rno'))
	password=request.POST.get('pwd')
	year=(request.POST.get('year'))
	course=(request.POST.get('course'))
	if fname and sname and contact_no and password and dept and hostel and year and email_id and rollno:
	 	db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
	 	year=int(year)
	 	rollno=int(rollno)
		contact_no=int(contact_no)
	 	query="select rollno,email from student"
	 	cur.execute(query)
	 	l=cur.fetchall()
	 	for i in l:
	 		if i[0]==rollno or i[1]==email_id:
	 			return render(request, 'blog/signup.html',{'messagee':'Account exists for this ID'})
	 	password=hashlib.sha512(password).hexdigest()
	 	query="INSERT INTO student(rollno,firstname,lastname,phoneno,year,department,hostel,email,password,course) values('%d','%s','%s','%d','%d','%s','%s','%s','%s','%s')"%(rollno,fname,sname,contact_no,year,dept,hostel,email_id,password,course)
		cur.execute(query);
		db.commit();
		query="select * from student where rollno='%d'"%(rollno)
		cur.execute(query)
		student=cur.fetchone()
		query="select * from election"
		cur.execute(query)
		elections=cur.fetchall()
		for i in elections:
			if i[4]=='0':
				if student[4]==int(i[5]):
					query="insert into voters(voter,electionid) values('%d','%d')"%(rollno,i[0])
					cur.execute(query)
					db.commit()
			else:
				if student[6]==i[5]:
					query="insert into voters(voter,electionid) values('%d','%d')"%(rollno,i[0])
					cur.execute(query)
					db.commit()
		query="select * from polls"
		cur.execute(query)
		polls=cur.fetchall()
		for i in polls:
			query="insert into pollers(poller,poll) values('%d','%d')"%(rollno,i[0])
			cur.execute(query)
			db.commit()
	 	return render(request, 'blog/signup.html',{'messagee':'Successful Signup'})
	else:
		return render(request, 'blog/signup.html',{'messagee':'Invalid Details. Please enter valid details.'})

def login(request):
	if request.session.has_key('user_id'):
		return redirect("home")
	else:
		return render(request, 'blog/login.html')

def login2(request):
	if request.session.has_key('user_id'):
		return redirect("home")
	else:
		rollno=request.POST.get('rno')
		password=request.POST.get('pwd')
		if rollno and password:
			db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
			cur=db.cursor()
			password=hashlib.sha512(password).hexdigest()
			query="select rollno,email,password from student where rollno='%s' and password='%s'"%(rollno,password)
			cur.execute(query)
			l=cur.fetchall()
			query="select * from notices natural join committee"
			cur.execute(query)
			m=cur.fetchall()
			if l:
				messages.success(request,"Successful Login")
				request.session['user_id']=l[0][0]
				return render(request,"blog/homee.html",{"user_id":l[0][0],'newsb':m,'messagee':'Successful Login!!	'})
			else:
				messages.error(request,"Invalid Email-Id or Password!")
				return render(request, 'blog/login.html',{'messagee':'Invalid Details'})	
		else:
			return redirect("login")

def logout(request):
	if request.session.has_key('user_id'):
		del request.session['user_id']
		return redirect("home")
	return redirect("home")

def profile(request):
	if request.session.has_key('user_id'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		rollno=request.session.get('user_id')
		query="select * from student where rollno='%s'"%(rollno)
		cur.execute(query)
		profile=cur.fetchone()
		return render(request,'blog/profile.html',{'profile':profile,'user_id':rollno})
	else:
		return render(request, 'blog/login.html',{'messagee':'Only Logged-in students can view. Log-In'})

def update(request,pk):
	if request.session.has_key('user_id'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		query="select * from student where rollno='%s'"%(pk)
		cur.execute(query)
		profile=cur.fetchone()
		return render(request,'blog/updateprof.html',{'user':profile,'user_id':pk})
	else:
		return render(request, 'blog/login.html',{'messagee':'Only Logged-in students can view. Log-In'})

def updatedprof(request,pk):
	if request.session.has_key('user_id'):
		db=MySQLdb.connect(host="localhost",user="root",passwd="Qwerty123@",db="parliament")
		cur=db.cursor()
		hostel=request.POST.get('hostel')
		contact_no=(request.POST.get('pno'))
		rollno=(request.POST.get('rno'))
		password=request.POST.get('pwd')
		year=(request.POST.get('year'))
		query="update student set hostel='%s',phoneno='%s',password='%s',year='%s' where rollno='%s'"%(hostel,contact_no,password,year,pk)			
		cur.execute(query)
		db.commit()
		query="select * from student where rollno='%s'"%(rollno)
		cur.execute(query)
		profile=cur.fetchone()
		return render(request,'blog/profile.html',{'messagee':'Profile Updated!!','user_id':rollno,'profile':profile})
	else:
		return render(request, 'blog/login.html',{'messagee':'Only Logged-in students can view. Log-In'})	