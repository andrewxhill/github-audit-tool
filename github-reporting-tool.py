#Written by Ben Francom (benfran.com) for EISMGard LLC (eismgard.com) under the MIT License
import os
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


#Get list of repos
print("Repo List:")
repos = org.get_repos()
for r in repos:
    print("  ",r.git_url)
    

#Get list of teams
print("\nTeam List:")
teams = org.get_teams()
for t in teams:
    print("   ",t.name)
    team_repos = t.get_repos()
    for repos in team_repos:
        print("     ",repos.git_url)

#Get list of team members
print("\nTeam Membership List:")
teams = org.get_teams()
for t in teams:
    print("  ",t.name," Team Members:")
    for m in t.get_members():
        #print("      Name: ",m.name,", Email: ",m.email,", ID: ",m.id,", Login: ",m.login)
        print("      ",m.login)

#Get list of repos
print("\nDirect Repo Rights:")
repos = org.get_repos()
for r in repos:
    print("  ",r.git_url)
    collaborators = r.get_collaborators()
    for c in collaborators:
        #print("      Name: ",c.name,", Email: ",c.email,", ID: ",c.id,", Login: ",c.login)
        print("      ",c.login)