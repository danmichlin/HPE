import urllib
import json
import paramiko
import os
from time import sleep
from os import environ as parameter
from cloudshell.api.cloudshell_api import CloudShellAPISession

connectivity = json.loads(parameter["QUALICONNECTIVITYCONTEXT"])
reservation = json.loads(parameter["RESERVATIONCONTEXT"])
resource = json.loads(parameter["RESOURCECONTEXT"])

jenkins_ip = resource['deployedAppData']['address']


api = CloudShellAPISession(connectivity["serverAddress"], connectivity["adminUser"], connectivity["adminPass"], 'Global')
reservation_details = api.GetReservationDetails(reservation["id"]).ReservationDescription
addresses = {(resource.ResourceModelName, resource.FullAddress) for resource in reservation_details.Resources if resource.ResourceModelName in ['model1','model2','model3' ]}


ssh = paramiko.SSHClient()
#for attribute in resource['deployedAppData']['attributes']:
#    if attribute['name'] == 'User':
#        username = attribute['value']
#    if attribute['name'] == 'Password':
#        password = api.DecryptPassword(attribute['value']).Value
ssh.connect(jenkins_ip, username='root', password='Xy6stqZ')

script_execute='ssh-keyscan'+tomcat_ip+'>> /root/jenkins/known_hosts'
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(script_execute)
script_execute='cd  /root/jenkins'
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(script_execute)

command1="sed -i 's/POSTGRES_IP/" + addresses['model1'] +"'/g' /root/jenkins/jobs/DEMOAPP-PIPLINE.xml"
command2="sed -i 's/TOMCAT_IP/"+ addresses['model2'] +"/g' /root/jenkins/jobs/DEMOAPP-PIPLINE.xml"
command3="sed -i 's/GITLAB_IP/"+addresses['model3']+"/g' /root/jenkins/jobs/DEMOAPP-PIPLINE.xml"
command4='docker build -t jenkinsaosdemo .'
command5='docker run --name  jenkins -d -p 8080:8080 -p 50000:50000 jenkinsaosdemo'
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command1)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command2)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command3)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command4)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command5)
