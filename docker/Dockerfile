FROM victorbalssa/tflearn-nltk:latest
MAINTAINER victorbalssa <balssa_v@etna-alternance.net>

ADD ./requirements.txt /bot/requirements.txt
WORKDIR /bot
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
# use ignored .dist config file
RUN mv ./fixtures/config.json.dist ./fixtures/config.json
CMD /usr/bin/python2.7 fixture.py && /usr/bin/python2.7 training.py && /usr/bin/python2.7 api.py
#CMD tail -f /dev/null
