FROM ubuntu:16.04 AS ubuntu__mogp

LABEL maintainer="cecilia@gmail.com"

RUN apt-get update
# RUN DEBIAN_FRONTEND=noninteractive apt-get install -y vim python2.7 git python-pip openjdk-8-jdk ant curl texlive-latex-base texlive-latex-extra dvipng python-enchant
RUN apt-get update && \
    apt-get install -y \
        vim \
        git \
        curl \
        python \
        python-pip \
        python-enchant \
        openjdk-8-jdk \
        texlive-latex-base \
        texlive-latex-extra \
        ant \
        dvipng

# RUN ln -fs /usr/share/zoneinfo/America/Argentina/Buenos_Aires /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

RUN pip install --upgrade pip
RUN pip install -U setuptools

RUN adduser --disabled-password --gecos "" ubuntu

ENV MOGPPATH=/home/ubuntu/mogp/mogp_with_terms

RUN mkdir -p $MOGPPATH
RUN mkdir -p $MOGPPATH/index
RUN mkdir -p /opt/pylucene

WORKDIR $MOGPPATH

#Python requirements
COPY ./requirements.txt $MOGPPATH
RUN cd $MOGPPATH && \
	pip install --requirement requirements.txt

#build PyLucene
RUN cd /opt/pylucene && \
	curl https://www.apache.org/dist/lucene/pylucene/pylucene-6.5.0-src.tar.gz \
    	| tar -xz --strip-components=1

RUN cd /opt/pylucene/jcc && JCC_JDK=/usr/lib/jvm/java-8-openjdk-amd64 python setup.py install
RUN cd /opt/pylucene && make all install JCC='python -m jcc' ANT=ant PYTHON=python NUM_FILES=8
RUN rm -rf /opt/pylucene


COPY . $WORKDIR
RUN chown -R 1000:1000 /home/ubuntu

# Use ubuntu user by default
USER ubuntu

CMD ["bash"]
