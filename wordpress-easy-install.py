#!/usr/bin/python
import commands, os, MySQLdb, random
def cmd(str):
	return commands.getoutput(str)
if cmd('whoami')== 'root': 
	print "checking with root privilegies"
	l=[]
	a='sudo yum install'
	print "checking necessary packages...."
	
	if 'httpd' in cmd('rpm -qa httpd'): #checking apache installation
		print "Apache installed"
	else:
		l.append(' httpd') #appending in list to install as list of packages at final
		print "Apache not installed"
	
	if 'mysql' or 'mariadb' in cmd('rpm -qa mysql'):
		print "Mysql installed"
	else:
		l.append(' mysql-server') #appending in list to install as list of packages at final
		print "MySQL not installed"
	if 'php' in cmd('rpm -qa php'):
		print "php installed"
	else:
		l.append(' php') #appending in list to install as list of packages at final
		print "php not installed"
	if os.access('/var/www/html/wordpress',os.F_OK):
		if os.listdir('/var/www/html/wordpress'):
			print "wordpress exists"
	else:
		print "Installing wordpress with wget"
		print cmd('sudo yum install wget')
		os.chdir('/tmp')
		print cmd('wget http://wordpress.org/latest.tar.gz')		
		print cmd('tar -xvzf latest.tar.gz -C /var/www/html')
		print 'wordpress installed'
	if l:
		for i in l:
			a+=i	
		print cmd(a)
	print "#############################################"
	print "creating MySQL database for wordpress..."  #Need python-mysql connectivity
	def create_db():
		db = MySQLdb.connect("localhost","root",raw_input('Enter MySQL root password: '),"" )
        	db_password=raw_input('Creating new user: wordpress \nEnter new password:')
		cursor=db.cursor()
		sql="CREATE USER wordpress@localhost IDENTIFIED BY '%s'" %db_password
		cursor.execute(sql)
		cursor.execute('CREATE DATABASE wordpress_db')
		cursor.execute('GRANT ALL ON wordpress_db.* TO wordpress@localhost')
		cursor.execute('FLUSH PRIVILEGES')
		db.commit()
		db.close()
	if 'MySQL-python' in cmd('rpm -qa MySQL-python'):
		create_db()
	else:
		print cmd('sudo yum install MySQL-python')
		create_db()
	print "############################################"
	print "configuring wordpress.."
	os.chdir('/var/www/html/wordpress')
	fo=open('wp-config-sample.php','r')
	f_data=fo.read()
	fo.close()
	if 'database_name_here' in f_data:
		 f_data=f_data.replace('database_name_here','wordpress_db')
	if 'username_here' in f_data:
		 f_data=f_data.replace('username_here','wordpress')
	if 'password_here' in f_data:
		 f_data=f_data.replace('password_here',db_password)
	for i in xrange(f_data.count('put your unique phrase here')):
		 f_data=f_data.replace('put your unique phrase here',hex(random.randint(12674898745234566,896547324871260876453))[2:],1)
	fw=open('wp-config.php','w')
	fw.write(f_data)
	fw.close()
	print "Success.. Wordpress is ready to run"
	print cmd('service httpd restart')
	print cmd('service mysqld start')
	print "launching firefox..."
	cmd("/usr/bin/firefox -new-window localhost:80/wordpress")
else:
	print "Need root access"	
