#Written by Ben Francom (benfran.com) for EISMGard LLC (eismgard.com) under the MIT License
import os
import json
from unicodedata import name
from github import Github

# using an access token
g = Github(os.environ['INPUT_TOKEN'])
org = g.get_organization(os.environ['INPUT_ORG'])

#env chiggity check
if os.environ.get('INPUT_TOKEN') is None:
    print('!!! missing INPUT_TOKEN environment variable !!!')
if os.environ.get('INPUT_ORG') is None:
    print('!!! missing INPUT_ORG environment variable !!!')



print(f"::set-output name=org::{os.environ['INPUT_ORG']}")

errors = {}
#Get list of repos
repo_lines = []
try: 
    repos = org.get_repos()
    # repo_lines = "Repos\n"
    for r in repos:
        # repo_lines += "  " + r.git_url + "\n"
        repo_lines.append(r.git_url)
except:
    message = "[]"
    print(f"::set-output name=repos::{message}")
print(f"::set-output name=repos::{repo_lines}")

#Get list of teams
team_lines = {}
try:
    teams = org.get_teams()
    for t in teams:
        # team_lines += "  " +  + "\n"
        team_lines[t.name] = []
        team_repos = t.get_repos()
        for r in team_repos:
            team_lines[t.name].append(r.git_url)
            # team_lines += "    " + r.git_url + "\n"
except:
    message = "failed to list teams"
    errors["teams"] = message
print(f"::set-output name=teams::{json.dumps(team_lines)}")

#Get list of team members
membership_lines = {}
try:
    teams = org.get_teams()
    for t in teams:
        membership_lines[t.name] = []
        for m in t.get_members():
            #print("      Name: ",m.name,", Email: ",m.email,", ID: ",m.id,", Login: ",m.login)
            membership_lines[t.name].append(m.login)
except:
    message = "failed to list members"
    errors["members"] = message
print(f"::set-output name=members::{json.dumps(membership_lines)}")

#Get list of repos
rights_lines = {}
try: 
    repos = org.get_repos()
    for r in repos:
        rights_lines[r.git_url] = []
        collaborators = r.get_collaborators()
        for c in collaborators:
            rights_lines[r.git_url].append(c.login)
            #print("      Name: ",c.name,", Email: ",c.email,", ID: ",c.id,", Login: ",c.login)
except:
    message = "failed to list rights"
    errors["rights"] = message

print(f"::set-output name=rights::{json.dumps(rights_lines)}")

print(f"::set-output name=errors::{json.dumps(errors)}")