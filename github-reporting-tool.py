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



print(f"::set-output name=org::org")

#Get list of repos
try: 
    repos = org.get_repos()
    repo_lines = []
    # repo_lines = "Repos\n"
    for r in repos:
        # repo_lines += "  " + r.git_url + "\n"
        repo_lines.append(r.git_url)
    print(f"::set-output name=repos::{repo_lines}")
except:
    message = "[]\n"
    print(f"::set-output name=repos::{message}")


#Get list of teams
try:
    teams = org.get_teams()
    team_lines = {}
    for t in teams:
        # team_lines += "  " +  + "\n"
        team_lines[t.name] = []
        team_repos = t.get_repos()
        for r in team_repos:
            team_lines[t.name].append(r.git_url)
            # team_lines += "    " + r.git_url + "\n"
    print(f"::set-output name=teams::{json.dumps(team_lines)}")
except:
    message = "failed to list teams\n"
    print(f"::set-output name=teams::{message}")

#Get list of team members
try:
    membership_lines = "\nMembers\n"
    teams = org.get_teams()
    for t in teams:
        membership_lines += "  " + t.name + " Team Members:\n"
        print("  ",t.name," Team Members:")
        for m in t.get_members():
            #print("      Name: ",m.name,", Email: ",m.email,", ID: ",m.id,", Login: ",m.login)
            membership_lines += "    " + m.login + "\n"
    print(f"::set-output name=members::{membership_lines}")
except:
    message = "failed to list members\n"
    print(f"::set-output name=members::{message}")

#Get list of repos
try: 
    rights_lines = "\nRights\n"
    repos = org.get_repos()
    for r in repos:
        rights_lines += "  " + r.git_url + "\n"
        collaborators = r.get_collaborators()
        for c in collaborators:
            #print("      Name: ",c.name,", Email: ",c.email,", ID: ",c.id,", Login: ",c.login)
            rights_lines += "  " + c.login + "\n"
    print(f"::set-output name=rights::{rights_lines}")
except:
    message = "failed to list rights\n"
    print(f"::set-output name=rights::{message}")