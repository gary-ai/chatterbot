FROM nandotk/tflearn-nltk:0.1
MAINTAINER nandotk <victor@dekalee.fr>

#RUN apt-get update \
#    && apt-get dist-upgrade
ADD ./requirements.txt /bot/requirements.txt
WORKDIR /bot
RUN pip install -r requirements.txt
EXPOSE 5000
CMD /usr/bin/python2.7 api.py
#CMD tail -f /dev/null
