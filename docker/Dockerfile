FROM victorbalssa/tflearn-nltk:latest
MAINTAINER victorbalssa <balssa_v@etna-alternance.net>

RUN apt-get update -y \
    && apt-get dist-upgrade -y
ADD ./requirements.txt /bot/requirements.txt
WORKDIR /bot
RUN pip install -r requirements.txt
# fixture mongo (dev)
EXPOSE 5000
CMD /usr/bin/python2.7 fixture.py && /usr/bin/python2.7 training.py && /usr/bin/python2.7 api.py
#CMD tail -f /dev/null
