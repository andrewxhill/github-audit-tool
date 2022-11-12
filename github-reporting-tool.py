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

audit = {
    "org": os.environ['INPUT_ORG']
}

print(f"::set-output name=org::{os.environ['INPUT_ORG']}")

errors = {}
#Get list of repos
repo_lines = []
try: 
    repos = org.get_repos()
    for r in repos:
        repo_lines.append(r.git_url)
except:
    errors["repos"] = "failed ot get repos"

print(f"::set-output name=repos::{repo_lines}")
audit["repos"] = repo_lines

#Get list of teams
team_lines = {}
try:
    teams = org.get_teams()
    for t in teams:
        team_lines[t.name] = []
        try:
            team_repos = t.get_repos()
            for r in team_repos:
                team_lines[t.name].append(r.git_url)
        except:
            errors[t.name] = "failed ot get team"

except:
    message = "failed to list teams"
    errors["teams"] = message
print(f"::set-output name=teams::{json.dumps(team_lines)}")
audit["teams"] = team_lines

#Get list of team members
membership_lines = {}
try:
    teams = org.get_teams()
    for t in teams:
        membership_lines[t.name] = []
        try:
            for m in t.get_members():
                membership_lines[t.name].append(m.login)
        except:
            errors[t.name] = "failed to get members"
except:
    message = "failed to list members"
    errors["members"] = message
print(f"::set-output name=members::{json.dumps(membership_lines)}")
audit["members"] = membership_lines

#Get list of repos
rights_lines = {}
try: 
    repos = org.get_repos()
    for r in repos:
        rights_lines[r.git_url] = []
        try:
            collaborators = r.get_collaborators()
            for c in collaborators:
                rights_lines[r.git_url].append(c.login)
        except:
            errors[r.git_url] = "failed ot get collaborators"
except:
    message = "failed to list rights"
    errors["rights"] = message

print(f"::set-output name=rights::{json.dumps(rights_lines)}")
audit["rights"] = rights_lines

print(f"::set-output name=errors::{json.dumps(errors)}")
audit["errors"] = errors



pth = os.environ['INPUT_PATH']
if pth != "":
    gt = os.environ['GITHUB_WORKSPACE']
    pt = os.path.join(gt, pth)
    dr = os.path.split(pth)
    if dr[0] != "":
        if not os.path.exists(dr[0]):
            print("making pth")
            print(os.path.abspath(dr[0]))
            os.makedirs(os.path.abspath(dr[0]), exist_ok=True)

    json.dump(audit, open(pth, "w+"), sort_keys=True, indent=4, separators=(',', ': '))
