# action will be run in python3 container
FROM python:3

RUN pip install --upgrade pip
RUN adduser -D myuser
USER myuser
WORKDIR /home/myuser

# copying requirements.txt and install the action dependencies
COPY --chown=myuser:myuser requirements.txt /requirements.txt
# COPY requirements.txt /requirements.txt

RUN pip install --user -r /requirements.txt
# script.py is the file that will contain the codes that we want to run for this action.
COPY script.py /script.py
# we will just run our script.py as our docker entrypoint by python script.py
CMD ["python", "/github-reporting-tool.py"]



$ git clone https://github.com/EISMGard/github-audit-tool
$ cd github-audit-tool
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ export GITHUB_ORG_NAME=<your github org name>
$ export  GITHUB_TOKEN=<your github token>
$ python github-reporting-tool.py