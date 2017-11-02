#-*- coding:utf-8 -*-
from __future__ import with_statement
from contextlib import closing
import sqlite3
import re
import hashlib

from flask import Flask
from flask import g, render_template
from flask import session, request, redirect, url_for

app = Flask(__name__)

'''
주의 : 정상 작동을 안 함
'''

def connect_db():
	return sqlite3.connect('.db', check_same_thread = False)
	
class WebPage(object):
	'''
	사용자에게 page를 직접적으로 표현하는 클래스

	'''
	@app.before_request
	def before_request():
		g.db = connect_db()

	@app.teardown_request
	def teardown_request(exception):
		g.db.close()
		
	@app.route('/short', methods=['GET', 'POST'])
	def urlshortener():
		'''
		url 단축 페이지.
		'''
		shorten = None
		error = None
		if request.method == 'POST':
			try:
				if session['logged_in']:
					if request.form['url'] != None:
						a = UrlShortener()
						shorten = a.url2short(request.form['url'])
						del(a)
				else: 
					error = u"로그인한 사용자만 단축 URL을 만드실 수 있습니다!"
			except: #로그인을 하지 않으면 session['logged_in'] 값이 없어서 예외가 발생함.
				error = u"로그인한 사용자만 단축 URL을 만드실 수 있습니다!"
		
		return render_template('shortener.html', shorten = shorten, error = error)
		
	@app.route('/s/<u>', methods = ['GET'])
	def short2url(u):
		if u is not None:
			a = UrlShortener()
			url = a.short2url(u)
			if url != "-1":
				return redirect(url, code=302)
			else: 
				return render_template('error.html')
		else:
			return render_template('error.html')
		
	@app.route('/login', methods = ['GET', 'POST'])
	def login():
		error = None
		if request.method == 'POST':
			if request.form['username'] == '' or request.form['password'] == '':
				error = u'아이디나 비밀번호를 입력하지 않았습니다.'
			else:
				id = request.form['username']
				pw = request.form['password']
				
				u = User(id)
				r = u.login(hashlib.md5(pw).hexdigest())
				if r == None:
					g.user = u
					return redirect(url_for('start'))
				else:
					error = r
		return render_template('login.html', error=error)

	@app.route('/logout')
	def logout():
		'''
		로그아웃을 하는 페이지.
		'''
		session.pop('username', None)
		session.pop('logged_in', None)
		return redirect(url_for('start'))

	@app.route('/register', methods = ['GET', 'POST'] )
	def register():
		'''
		사용자 등록을 하게 해 주는 페이지
		'''
		error = None
		if request.method == 'POST':
			username = request.form['username']
			pw = request.form['password']
			pw2 = request.form['password2']
			email = request.form['email']
			nickname = request.form['nickname']
			if username == '':
				error = u"사용자명을 입력하지 않으셨습니다."
			elif pw == '':
				error = u"비밀번호를 입력하지 않으셨습니다."
			elif pw != pw2:
				error = u"비밀번호가 다르니 다시 한번 입력해 주십시오."
			elif email == '':
				error = u"이메일을 입력하지 않으셨습니다."
			elif nickname == '':
				error = u"닉네임을 입력하지 않으셨습니다."
			else: #검증이 다 끝남
				u = User(username)
				r = u.register(hashlib.md5(pw).hexdigest(), email, nickname)
				if r == 1:
					error = u"아이디가 중복됩니다."
				elif r == 0:
					return redirect(url_for('start'))
		return render_template('register.html', error=error)
		
	@app.route('/e')
	def entries_list():
		elist = entry_board.entries_list()
		return render_template('entry_list.html', entries = elist)
		
	@app.route('/e/<a>')
	def load_entry(a):
		try:
			entry = entry_board.entry(a)
			id = entry[0]
			title = entry[1]
			username = entry[2]
			tag = entry[3]
			url = entry[4]
			text = entry[5]
			return render_template('entry.html', id = id, title = title, username = username, tag = tag, url = url, text = text)
		except: return render_template('error.html', msg = "올바르지 않은 게시글 번호 : %s" % (a, ))
		
	@app.route('/write', methods = ['POST', 'GET'])
	def write_entry():
		'''
		게시판에 글을 쓸 때 호출되는 부분.
		
		'''
		error = None
		if request.method == 'POST':
			title = request.form['title']
			tag = request.form['tag']
			url = request.form['url']
			text = request.form['entry_text']	
			if title == '' or text == '':
				error = u"다시 확인하세요. title : %s, text = %s" % (title, text, )
				return render_template('entry_write.html', error = error)
			else:
				entry_board.input_entry(title, tag, url, text) # flask에서 자체적으로 XSS를 방어하므로 딱히 내용을 신경쓰지 않는다
				return render_template('entry_list.html')
		return render_template('entry_write.html')
		
	@app.route('/change_info', methods = ['POST', 'GET'])
	def change_info():
		error = None
		if request.method == 'POST':
			username = request.form['username']
			pw = request.form['password']
			pw2 = request.form['password2']
			email = request.form['email']
			nickname = request.form['nickname']
			if username == '':
				error = u"사용자명을 입력하지 않으셨습니다."
			elif pw == '':
				error = u"비밀번호를 입력하지 않으셨습니다."
			elif pw != pw2:
				error = u"비밀번호가 다르니 다시 한번 입력해 주십시오."
			elif email == '':
				error = u"이메일을 입력하지 않으셨습니다."
			elif nickname == '':
				error = u"닉네임을 입력하지 않으셨습니다."
			else: #검증이 다 끝남
				u = User(username) # 사용자의 이름을 받아서
				r = u.change_info(hashlib.md5(pw).hexdigest(), email, nickname) #업데이트를 한다
	
		return render_template('change_info.html', error = error, username=session['username'])
				
	@app.route('/')
	def start():
		#return u'Now working'
		return redirect('/short')
		
class EntryBoard(object):
	'''
	게시판!!!. DB의 entries 테이블에 해당하는 게시판!!!
	'''
	def __init__(self):
		self.db = connect_db()
		self.cur = self.db.cursor() #추후 개시판을 여러개 사용할 경우를 대비. board_name은 DB 테이블명과 동일하다
		
	def entries_list(self):
		'''
		게시물 전체를 통째로
		반환 형식. 리스트로 묶인 튜플 : (id, title, username, tag, url)
		'''
		c = self.db.cursor()
		c.execute('select title, text, id, username, tag from entries order by id desc')
		return c.fetchall()
		
	def entry_info(self, id):
		'''
		id를 주면 정보를 얻어옴. (제목, 사용자명) 튜플 반환.
		'''
		c = self.db.cursor()
		c.execute(u"SELECT title, username, tag, url FROM entries WHERE id = ?", (id, ) )
		try:
			r = c.fetchone()
			title = r[0]
			username = r[1]
			tag = r[2]
			url = r[3]
			return (id, title, username, tag, url)
		except:
			raise IDError(u"id에 해당하는 글이 없습니다.")
			return (-1, -1, -1, -1)
		
	def entry(self, id):
		'''
		id를 주면 정보를 얻어옴. (제목, 사용자명, 태그, url, 본문) 튜플 반환.
		'''
		c = self.db.cursor()
		c.execute(u"SELECT title, username, tag, url, text FROM entries WHERE id = %s" % (id, ) ) 
		try:
			r = c.fetchone()
			title = r[0]
			username = r[1]
			tag = r[2]
			url = r[3]
			text = r[4]
			return (id, title, username, tag, url, text)
		except:
			raise # 정보가 없으면 예외가 발생함
			return (-1, -1, -1, -1, -1)
		
	def input_entry(self, title, tag, url, text):
		'''
		주어진 정보에 따라 게시물을 입력한다. 정상적으로 처리되면 양수인 게시물 번호를 반환한다. 오류가 발생한 경우 음수의 오류 코드를 반환한다. 
		오류 코드의 절대값이 가장 작은 것만 반환한다.
		
		-1 : 로그인을 안 함
		-2 : 제목이 없음
		-3 : 내용이 없음
		
		'''
		if not session['logged_in']:
			return -1
		elif title == None or title == '':
			return -2
		elif text == None or text == '':
			return -3
		# 예외 처리 끝
		c = self.db.cursor()
		c.execute(u"INSERT INTO entries(title, tag, url, text, username) VALUES (?, ?, ?, ?, ?)", (title, tag, url, text, session['username']) ) # DB에 게시물을 집어넣고
		self.db.commit() #Commit을 해야 적용이 된다
		c.execute(u"SELECT MAX(id) FROM entries")
		return int(c.fetchone()[0]) # 마지막 게시물 번호...
	
	@property
	def entry_number(self):
		'''
		이 게시판에 있는 전체 게시물 수를 반환한다
		'''
		c = self.db.cursor()
		c.execute(u"SELECT MAX(id) FROM entries" )
		try:
			return int(c.fetchone()[0])
		except:
			return 0 #게시글이 하나도 없으면 예외가 발생함
		
	#지우는 것도 일단 생략.
	def delete_entry(self, id):
		pass
	
	# 수정도 일단 생략.
	def edit_entry(self, id, titie, tag, url, text):
		pass
	# 복잡하니 검색은 생략
	def search(self, mode, query):
		pass
		
	def _search_id(self, id):
		pass
		
	def _search_tag(self, tag):
		pass
		
	def _search_title(self, title):
		pass
		
class UrlShortener(object):
	'''
	URL 단축 서비스를 제공하는 객체.
	'''
	def __init__(self):
		self.db = connect_db()
		self.cur = self.db.cursor()
	
	def __del__(self):
		self.db.commit()
	
	def url2short(self, url):
		'''
		제시된 인터넷 주소를 단축 url로 바꿔준다.
		'''
		if not(url[0:6] == "http://" or url[0:7] == "https://"):
			url = u"http://" + unicode(url)
		return self._url2short(url)
	
	def _url2short(self, url):
		'''
		주소를 주면 줄임 주로를 반환
		'''
		self.cur.execute(u"INSERT INTO urlshortener(url) VALUES (?)", (url, ) )
		self.cur.execute(u"SELECT MAX(id) FROM urlshortener")
		maxnum = self.cur.fetchone()[0]
		return self._short_encode(maxnum)
		
	def short2url(self, short):
		'''
		단축 URL을 원래 URL으로 바꿔준다.
		'''
		num = self._short_decode(short)
		self.cur.execute("SELECT url FROM urlshortener WHERE id = ?", (str(num), ) )
		a = self.cur.fetchone()
		try:
			return a[0]
		except:
			return "-1"
		
	def _short_encode(self, num):
		'''
		주어진 숫자를 Base62(비표준)으로 인코딩.
		'''
		
		TABLE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
		a = ''
		try:
			num = int(num)
		except:
			raise # 숫자를 입력하지 않는 등 공격에 대비
			
		while True:
			t = num % 62
			a = a + TABLE[t]
			num = num // 62
			if num == 0: break
		
		return a
		
	def _short_decode(self, text):
		'''
		주어진 Base62(비표준) 문자열을 숫자로 디코딩.
		'''
		out = 0
		for i in range(0, len(text)):
			a = ord(text[i])
			if a >= 65 and a <= 90: # A~Z
				a = a - 65
			elif a >= 97 and a <= 122: # a~z
				a = a - 71
			elif a >= 48 and a <= 57: # 0~9
				a = a + 4
			else:
				raise ShortDecodeError
			out = out + ( a * (64 ** i) )
		return out

	def commit(self):
		self.cur.commit()
		return

class User(object):
	'''
	어느 한 사용자를 나타내는 객체이다. 단, 로그아웃은 해당하지 않는다.
	
	pw : 패스워드. sha512 해시 함수를 이용한 값을 전달해야 함. User 객체 내에서는 평문으로 된 패스워드를 다루지 않습니다.
	'''

	def __init__(self, id):
		self.LOGGEDIN = False
		self.id = id
		self.db = connect_db()
		
	def login(self, pw):
		'''
		로그인을 하는 과정. 로그인에 성공하면 None을, 실패하면 오류 메시지를 반환.
		
		pw : 항상 SHA512로 처리된 패스워드를 입력해야 한다. 평문을 입력하면 정상 처리가 되지 않는다.
		'''

		idpw_error = u"아이디나 비밀번호가 잘못되었습니다."	# 공통된 에러 메시지를 내보내기 위함
		c = self.db.cursor()
		c.execute(u"SELECT EXISTS ( SELECT username FROM user where username = %s)" %s (self.id, ) )
		t = c.fetchone()
		if t[0] == 0:
			error = idpw_error
		else:
			c.execute(u"SELECT userpassword FROM user WHERE username = %s)" %s (self.id, ) ) #암호 해시값을 읽어들인다
			if c.fetchone()[0] == pw: # DB에 저장된 값과 입력 값이 같으면 통과.
				session['username'] = self.id
				session['logged_in'] = True
				error = None
			else:
				error = idpw_error			
		return error
		
	@property
	def email(self):
		c = self.db.cursor()
		c.execute('SELECT email FROM user WHERE username = ?', (self.id, ))
		return c.fetchone()[0]
		
	def change_info(self, pw, email, nickname):
		c = self.db.cursor()
		c.execute('UPDATE user SET userpassword = ?, email = ?, nickname = ? WHERE username = ?', (pw, email, nickname, self.id, ))
		self.db.commit()
		return
		
	def register(self, pw, email, nickname):
		'''
		해당 객체에 해당하는 사용자를 등록한다. 
		
		주의 : pw는 무조건 SHA512로 처리해야 하며 그렇지 않는 경우 DB에 평문 패스워드가 저장된다. 대충 처리를 하긴 했지만 조심.
		
		오류코드
		0 : 정상적으로 처리됨
		1 : 해당 아이디가 이미 존재함
		'''
		c = self.db.cursor()
		c.execute(u"SELECT EXISTS (SELECT username FROM user WHERE username = ?)", (self.id, ) )
		r = c.fetchone()
		if r[0] != 0:
			return 1
		else:
			usermode = ''
			c.execute(u"INSERT INTO user(username, userpassword, email, usermode, nickname) VALUES (?, ?, ?, ?, ?)", (self.id, pw, email, usermode, nickname) )
			self.db.commit()
			return 0

	@property
	def nickname(self):
		return self._nickname

	def _nickname(self):
		pass
	

if __name__ == '__main__':
	#session 기능을 쓰려면 필요한 부분. secret_key와 type을 지정해 줘야 한다고 함.
	app.secret_key = 'E1DDB724D4CCB990D97F6387BA006106D525969D38F36C0A2AC4227869E3C12252569A06A07BA8B2C436D6754A0373F88394AFF15F72A1B91DD7F749DB80211A'
	app.config['SESSION_TYPE'] = 'filesystem'
	entry_board = EntryBoard()
	app.debug = True # 디버그 정보가 필요함.
	app.run()