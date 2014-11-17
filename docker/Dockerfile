FROM ubuntu:14.04

MAINTAINER Alexander Skjolden alex@plastboks.net

RUN apt-get update
#RUN apt-get upgrade
RUN apt-get -y install build-essential
RUN apt-get -y install git 
RUN apt-get -y install python-virtualenv
RUN apt-get -y install virtualenvwrapper

VOLUME /pyrtos/shared

RUN mkdir -p /opt/virtualenvs
ENV WORKON_HOME /opt/virtualenvs
RUN chmod +x /usr/share/virtualenvwrapper/virtualenvwrapper.sh
RUN /bin/bash -c "/usr/share/virtualenvwrapper/virtualenvwrapper.sh"
#RUN mkvirtualenv venv
#RUN workon venv
#WORKDIR venv
#RUN git clone https://github.com/plastboks/Pyrtos.git app
