FROM python:3

RUN apt-get update \
    && apt-get install -y locales \
    && locale-gen ja_JP.UTF-8
RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

RUN apt-get update \
    && apt-get install -y zsh vim sed git

RUN git clone --recursive https://github.com/sorin-ionescu/prezto.git \
		/etc/zsh/prezto && \
	cd /etc/zsh/prezto; git checkout --detach 8a967fc && \
	echo "source /etc/zsh/prezto/runcoms/zlogin" > /etc/zsh/zlogin && \
	echo "source /etc/zsh/prezto/runcoms/zlogout" > /etc/zsh/zlogout && \
	echo "source /etc/zsh/prezto/runcoms/zshenv" > /etc/zsh/zshenv && \
	echo "source /etc/zsh/prezto/runcoms/zpreztorc" >> /etc/zsh/zshrc && \
	echo "source /etc/zsh/prezto/runcoms/zshrc" >> /etc/zsh/zshrc && \
	echo "source /etc/zsh/prezto/runcoms/zprofile" >> /etc/zsh/zprofile && \
	echo "ZPREZTODIR=/etc/zsh/prezto" >> "/etc/zsh/zshrc" && \
	echo "source \${ZPREZTODIR}/init.zsh" >> "/etc/zsh/zshrc" && \
	sed -ri "s/theme 'sorin'/theme 'skwp'/g" \
		/etc/zsh/prezto/runcoms/zpreztorc && \
	sed -ri '/directory/d' /etc/zsh/prezto/runcoms/zpreztorc && \
	sed -ri "s/'prompt'/'syntax-highlighting' \
		'history-substring-search' 'prompt'/g" /etc/zsh/prezto/runcoms/zpreztorc

RUN echo "export LANG=ja_JP.UTF-8" >> /etc/zsh/zshrc
RUN zsh
ENTRYPOINT ["zsh"]
CMD ["prompt", "pure"]


ENV DOCKERIZE_VERSION v0.6.1
RUN apt-get update && apt-get install -y wget \
    && wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD requirements.txt .

RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

RUN rm requirements.txt

WORKDIR /code