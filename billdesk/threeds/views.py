from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages


def home(request):
    import mysql.connector
    my_db = mysql.connector.connect(host="192.168.1.74", user="root", password="password", database="deploy")
    mycursor = my_db.cursor()
    select_data = "select * from deploy.3ds order by id desc limit 1"
    mycursor.execute(select_data)
    records = mycursor.fetchall()
    for row in records:
        git_url = (row[1])
        git_branch = (row[2])
        time = (row[3])
        commit = (row[4])
        author = (row[5])
    select_data = "select * from deploy.preparatory order by id desc limit 1"
    mycursor.execute(select_data)
    records = mycursor.fetchall()
    for row in records:
        git_urlp = (row[1])
        git_branchp = (row[2])
        timep = (row[3])
        commitp = (row[4])
        authorp = (row[5])
    return render(request, 'home.html', {'git_url': git_url, 'git_branch':git_branch, 'git_urlp':git_urlp, 'git_branchp':git_branchp, 'time': time, 'commit':commit, 'author':author, 'timep': timep, 'commitp':commitp, 'authorp':authorp})

def clone(request):
    import os, git, shutil
    filename = request.GET['repo']
    branch = request.GET['branch']
    os.chdir('/tmp/projects/')
    if os.path.isdir('/tmp/projects/three-ds-server-2.0'):
        shutil.rmtree('/tmp/projects/three-ds-server-2.0')
        print(filename)
        print(branch)
        git.Git("/tmp/projects/").clone(filename)
        os.chdir('/tmp/projects/three-ds-server-2.0/')
        os.system('/usr/bin/git fetch')
        fetch = '/usr/bin/git checkout ' + branch
        print(fetch)
        os.system(fetch)
        os.system('cp /home/anand/Documents/JKS/threeDSServer.jks /tmp/projects/three-ds-server-2.0/src/main/resources/threeDSServer.jks')
        os.system('mvn package -DskipTests')
        print('Build of Three-Ds-Server jar file Complete')
    filename2 = request.GET['repo2']
    branch2 = request.GET['branch2']
    os.chdir('/tmp/projects/')
    if os.path.isdir('/tmp/projects/preparatory_info_server'):
        shutil.rmtree('/tmp/projects/preparatory_info_server')
        print(filename2)
        print(branch2)
        git.Git("/tmp/projects/").clone(filename2)
        os.chdir('/tmp/projects/preparatory_info_server/')
        os.system('/usr/bin/git fetch')
        fetch = '/usr/bin/git checkout ' + branch2
        print(fetch)
        os.system(fetch)
        os.system('cp /home/anand/Documents/JKS/threeDSServer.jks /tmp/projects/preparatory_info_server/src/main/resources/threeDSServer.jks')
        os.system('mvn package -DskipTests')
        print('Build of preparatory_info_server jar file Complete')
    jarstatus = "Jar File Build Suceesfully"
    return render(request, 'home.html', {'jarstatus': jarstatus})

def cleardb(requests):
    import paramiko, os
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_DB')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    stdin, stdout, stderr = ssh.exec_command("/bin/bash /home/billdesk/scripts/clear3dsdb.sh")
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        print("Backup Complete")
        cleardb3ds = "Cleared 3ds Database"
        return render(requests, 'home.html', {'cleardb3ds': cleardb3ds})
        ssh.close()
    else:
        print("Error", exit_status)
        cleardb3ds = "Error in Clearing Database"
        return render(requests, 'home.html', {'cleardb3ds': cleardb3ds})
        ssh.close()

def clearprepdb(requests):
    import paramiko, os
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_DB')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    stdin, stdout, stderr = ssh.exec_command("/bin/bash /home/billdesk/scripts/clearprepdb.sh")
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        print("Backup Complete")
        cleardbprep = "Cleared Preparatory Database"
        return render(requests, 'home.html', {'cleardbprep': cleardbprep})
        ssh.close()
    else:
        print("Error", exit_status)
        cleardbprep = "Error in Clearing Database"
        return render(requests, 'home.html', {'cleardbprep': cleardbprep})
        ssh.close()

def clearredis(request):
    import paramiko, os
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_PREPARATORY')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    print('Backup and Clear Redis')
    stdin, stdout, stderr = ssh.exec_command("redis-cli save && sudo cp /var/lib/redis/dump.rdb /data/redis/dump.$(date +%Y%m%d%H%M).rdb && redis-cli FLUSHALL")
    cleardbredisdb = []
    for i in range(0, 1):
        cleardbredisdb.append(stdout.readlines(i))
    print(cleardbredisdb)
    ssh.close()
    cleardbredis = "Cleared Redis Database."
    return render(request, 'home.html', {'cleardbredis': cleardbredis})

def updateconfig(request):
    messages.success(request, 'Redirecting to Config Editor')
    return redirect('http://192.168.1.104:7001/')

def deployapp(requests):
    import paramiko, os, mysql.connector
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_3DS')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    sftp = ssh.open_sftp()
    print('SSH Connection Established')
    print('Uploading')
    sftp.put('/tmp/projects/three-ds-server-2.0/target/emvco-0.0.1-SNAPSHOT.jar', '/home/billdesk/deploy/threeds/emvco-0.0.1-SNAPSHOT.jar')
    print('Jar file copying complete')
    sftp.close()
    deployapp="Copied 3DS Jar file to deploy folder"
    threeds = '/tmp/projects/three-ds-server-2.0'
    os.chdir(threeds)
    os.system("cat .git/config |grep url |awk '{print $3}' > /tmp/3ds_git_log.txt")
    os.system("git branch |grep '*' |awk '{print $2}' >> /tmp/3ds_git_log.txt")
    os.system('git log -1 >> /tmp/3ds_git_log.txt')
    f = open('/tmp/3ds_git_log.txt', "r")
    threedsurl = f.readline()
    threedsbranch = f.readline()
    threedscommit = f.readline()
    threedsauthor = f.readline()
    threedsdate = f.readline()
    my_db = mysql.connector.connect(host="192.168.1.74", user="root", password="password", database="deploy")
    mycursor = my_db.cursor()
    mycursor.execute("create table IF NOT EXISTS deploy.3ds (id int NOT NULL AUTO_INCREMENT, git_url varchar(75), git_branch varchar(50), deploytime DATETIME DEFAULT CURRENT_TIMESTAMP, commitid varchar(50), author varchar(100), committime varchar(50), PRIMARY KEY (id))")
    my_db.commit()
    insert_data = "insert into deploy.3ds (git_url, git_branch, commitid, author, committime) values  ( %s, %s, %s, %s, %s)"
    recordTuple = (threedsurl.strip(), threedsbranch.strip(), threedscommit[7:].strip(), threedsauthor[8:].strip(), threedsdate[8:].strip())
    mycursor.execute(insert_data, recordTuple)
    my_db.commit()
    return render(requests, 'home.html', {'deployapp': deployapp})

def deploypreparatoryapp(requests):
    import paramiko, os, mysql.connector
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_PREPARATORY')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    sftp = ssh.open_sftp()
    print('SSH Connection Established')
    print('Uploading')
    sftp.put('/tmp/projects/preparatory_info_server/target/emvco.preparatory.info.server-0.0.1-SNAPSHOT.jar', '/home/billdesk/deploy/preparatory-info-server/emvco.preparatory.info.server-0.0.1-SNAPSHOT.jar')
    print('Jar file deployed Complete')
    sftp.close()
    deployprep="Copied Preparatory Jar file to deploy folder"
    preparatory= '/tmp/projects/preparatory_info_server/'
    os.chdir(preparatory)
    os.system("cat .git/config |grep url |awk '{print $3}' > /tmp/preparatory_git_log.txt")
    os.system("git branch |grep '*' |awk '{print $2}' >> /tmp/preparatory_git_log.txt")
    os.system('git log -1 >> /tmp/preparatory_git_log.txt')
    f = open('/tmp/preparatory_git_log.txt', "r")
    threedsurl = f.readline()
    threedsbranch = f.readline()
    threedscommit = f.readline()
    threedsauthor = f.readline()
    threedsdate = f.readline()
    my_db = mysql.connector.connect(host="192.168.1.74", user="root", password="password", database="deploy")
    mycursor = my_db.cursor()
    mycursor.execute("create table IF NOT EXISTS deploy.preparatory (id int NOT NULL AUTO_INCREMENT, git_url varchar(75), git_branch varchar(50), deploytime DATETIME DEFAULT CURRENT_TIMESTAMP, commitid varchar(50), author varchar(100), committime varchar(50), PRIMARY KEY (id))")
    my_db.commit()
    insert_data = "insert into deploy.preparatory (git_url, git_branch, commitid, author, committime) values  ( %s, %s, %s, %s, %s)"
    recordTuple = (threedsurl.strip(), threedsbranch.strip(), threedscommit[7:].strip(), threedsauthor[8:].strip(), threedsdate[8:].strip())
    mycursor.execute(insert_data, recordTuple)
    my_db.commit()
    return render(requests, 'home.html', {'deployprep': deployprep})

def stopservicesthreedsapp(requests):
    import paramiko, os
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_3DS')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    print('Stoping Services')
    stdin, stdout, stderr = ssh.exec_command("/bin/bash /home/billdesk/scripts/stopservices.sh")
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        print("Services Stoped")
        ssh.close()
        stop3ds = 'ThreeDS Services Stopped'
        return render(requests, 'home.html', {'stop3ds': stop3ds})
    else:
        print("Error in Stopping ThreeDS Services")
        ssh.close()
        stop3ds = 'Error in Stopping 3DS Services'
        return render(requests, 'home.html', {'stop3ds': stop3ds})

def stopservicespreparatorapp(requests):
    import paramiko, os
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_PREPARATORY')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    print('Stoping Services')
    stdin, stdout, stderr = ssh.exec_command("/bin/bash /home/billdesk/scripts/stopservices.sh")
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        print("Preparatory Services Stoped")
        ssh.close()
        stopprep = 'Preparatory Services Stopped'
        return render(requests, 'home.html', {'stopprep': stopprep})
    else:
        print("Error in Stopping Preparatory Services")
        ssh.close()
        stopprep = 'Error in Stopping Preparatory Services'
        return render(requests, 'home.html', {'stopprep': stopprep})


def startservicesthreedsapp(requests):
    import paramiko, os
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_3DS')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    print('Starting Services')
    stdin, stdout, stderr = ssh.exec_command("/bin/bash /home/billdesk/scripts/startservices.sh")
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        print("ThreeDS Services Started")
        ssh.close()
        status3ds='ThreeDS Services Started'
        return render(requests, 'home.html', {'status3ds': status3ds})
    else:
        print("Error in Starting ThreeDS Services")
        status3ds = 'ERROR IN STARTING 3DS Services'
        return render(requests, 'home.html', {'status3ds': status3ds})
        ssh.close()

def startservicespreparatorapp(requests):
    import paramiko, os
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_PREPARATORY')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    print('Starting Services')
    stdin, stdout, stderr = ssh.exec_command("/bin/bash /home/billdesk/scripts/startservices.sh")
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        print("Preparatory Services Started")
        ssh.close()
        statusprep = 'Preparatory Services Started'
        return render(requests, 'home.html', {'statusprep': statusprep})
    else:
        print("Error in Starting Preparatory Services")
        return HttpResponse("Error in Starting Preparatory Services")
        ssh.close()

def servicestatusthreedsapp(request):
    import paramiko, os
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_3DS')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    print('Status of Services')
    stdin, stdout, stderr = ssh.exec_command("sudo netstat -ntpl |grep java  | cut -c 24-29")
    output3ds = []
    for i in range(0, 2):
        output3ds.append(stdout.readlines(i))
    print(output3ds)
    return render(request, 'home.html', {'output3ds': output3ds})
    ssh.close()

def servicesstatuspreparatorapp(request):
    import paramiko, os
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_PREPARATORY')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    print('Status of Services')
    stdin, stdout, stderr = ssh.exec_command("sudo netstat -ntpl |grep java  | cut -c 24-29")
    outputprep = []
    for i in range(0, 2):
        outputprep.append(stdout.readlines(i))
    print(outputprep)
    return render(request, 'home.html', {'outputprep': outputprep})
    ssh.close()

def refreshconfigapp(request):
    import paramiko, os
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_3DS')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    stdin, stdout, stderr = ssh.exec_command(
        'curl 127.0.0.1:8000/actuator/refresh -d {} -H "Content-Type: application/json"')
    x = stdout.readlines()
    val = x[0]
    if len(val) == 2:
        print('Config Updated', val)
        outputconfig3ds = 'Config Updated'
    else:
        print('Config No update, Error:', val)
        outputconfig3ds = 'Error in Updating Config'
    ssh.close()
    return render(request, 'home.html', {'outputconfig3ds': outputconfig3ds})

def refreshconfigpreparatorapp(request):
    import paramiko, os
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_PREPARATORY')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    stdin, stdout, stderr = ssh.exec_command('curl 127.0.0.1:8000/actuator/refresh -d {} -H "Content-Type: application/json"')
    x = stdout.readlines()
    val = x[0]
    if len(val) == 2:
        print('Config Updated', val)
        outputconfigprep = 'Config Updated'
    else:
        print('Config No update, Error:', val)
        outputconfigprep = 'Error in Updating Config'
    ssh.close()
    return render(request, 'home.html', {'outputconfigprep': outputconfigprep})

def healthcheckapp(request):
    import paramiko, os
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_3DS')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    stdin, stdout, stderr = ssh.exec_command('curl 127.0.0.1:8000/actuator/health')
    x = stdout.readlines()
    outputhealth3ds = x[0]
    if outputhealth3ds == '{"status":"UP"}':
        print('Config Server is Up', outputhealth3ds)
    else:
        print('Config Server is having issues', outputhealth3ds)
        outputhealth3ds = '"status": ERROR.'
    ssh.close()
    return render(request, 'home.html', {'outputhealth3ds': outputhealth3ds})

def healthcheckpreparatorapp(request):
    import paramiko, os
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_PREPARATORY')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    stdin, stdout, stderr = ssh.exec_command('curl 127.0.0.1:8000/actuator/health')
    x = stdout.readlines()
    outputhealthprep = x[0]
    if outputhealthprep == '{"status":"UP"}':
        print('Config Server is Up', outputhealthprep)
    else:
        print('Config Server is having issues', outputhealthprep)
        outputhealthprep = '"status": ERROR.'
    ssh.close()
    return render(request, 'home.html', {'outputhealthprep': outputhealthprep})

def loadthreedsapp(request):
    import paramiko, os, time
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_3DS')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    timer = 0
    while timer < 5:
        stdin, stdout, stderr = ssh.exec_command("tail -n1 /tmp/cpu_usage.out")
        outputapp = []
        for i in range(0, 1):
            outputapp.append(stdout.readlines(i))
            print(outputapp)
            return render(request, 'home.html', {'outputapp': outputapp})
        timer += 1
        time.sleep(30)
    ssh.close()

def loadpreparatorapp(request):
    import paramiko, os, time
    from dotenv import load_dotenv
    dotenv_path = '/home/anand/Documents/Scripts/Python/.envssh'
    load_dotenv(dotenv_path)
    hostip = os.getenv('HOSTIP_PREPARATORY')
    user = os.getenv('USERSSH')
    password = os.getenv('PASSWORD')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostip, port=22, username=user, password=password)
    timer = 0
    while timer < 5:
        stdin, stdout, stderr = ssh.exec_command("tail -n1 /tmp/cpu_usage.out")
        output = []
        for i in range(0, 1):
            output.append(stdout.readlines(i))
            print(output)
            return render(request, 'home.html', {'output': output})
        timer += 1
        time.sleep(30)
    ssh.close()