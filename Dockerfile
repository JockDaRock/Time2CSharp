FROM microsoft/dotnet

ENV TMPDIR /tmp

ADD https://github.com/alexellis/faas/releases/download/0.5.8-alpha/fwatchdog /usr/bin

RUN apt-get update && apt-get -y upgrade && apt-get install -y python3-pip

RUN chmod +x /usr/bin/fwatchdog

WORKDIR /tmp/

RUN dotnet new console
RUN dotnet restore

WORKDIR /root/

COPY time2CSharp.py .

ENV fprocess="python3 time2CSharp.py"

HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

CMD ["/usr/bin/fwatchdog"]