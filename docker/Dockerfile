FROM victorbalssa/tflearn-nltk:latest
MAINTAINER victorbalssa <balssa_v@etna-alternance.net>

#RUN apt-get update \
#    && apt-get dist-upgrade
ADD ./requirements.txt /bot/requirements.txt
WORKDIR /bot
RUN pip install -r requirements.txt
EXPOSE 5000
CMD /usr/bin/python2.7 api.py
#CMD tail -f /dev/null
