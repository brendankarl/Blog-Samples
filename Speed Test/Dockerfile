FROM clowa/powershell-core:latest

SHELL ["/bin/sh", "-c"]
RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install speedtest-cli
RUN update-ca-certificates --fresh

SHELL ["pwsh", "-command"]
RUN mkdir speedtest
COPY ./SpeedTest.ps1 /speedtest/SpeedTest.ps1
WORKDIR /speedtest
ENTRYPOINT ["pwsh"]
CMD ["SpeedTest.ps1"]
# https://www.fosstechnix.com/dockerfile-instructions/
# docker build -t speedtest
# docker run speedtest
