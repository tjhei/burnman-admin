import os
import re

# github access token to set commit status
# fill in here or create token.txt with it
token  = ""
if os.path.isfile('token.txt'):
    token = open('token.txt').read().replace("\n","")

# name of the user/organization on github
github_user = "geodynamics"

# name of the repo on github
github_repo = "burnman"

# directory where the aspect git repo sits
repodir = os.getcwd()+"/"+github_repo

# number of tests to go back in time when doing "run-all" default 10
n_old_tests = 10

# if a user that is_allowed() posts a comment that has
# has_hotword(text) return True, the PR is tested
def has_hotword(text):
    if "/run-tests" in text:
        return True
    return False

# return true if user is trusted
def is_allowed(username):
    trusted = ['tjhei', 'bangerth', 'jdannberg', 'sannecottaar', 'ian-r-rose', 'bobmyhill']

    if username in trusted:
        return True
    
    return False

# make a nice link for a test result:
def make_link(sha):
    return "http://www.math.clemson.edu/~heister/burnman-logs/{}/summary".format(sha)


# for a given line l of the test output return
# "good", "bad", or "neutral"
def status_of_output_line(l):
    status = "neutral"
    if re.match(r'... ok$', l):
        status = "good"
    elif re.match(r'^OK$', l):
        status = "good"
    #if re.match(r'^([ ]*)0 Compiler errors$', l):
    #    status = "good"
    #elif re.match(r'^([ ]*)(\d+) Compiler errors$', l):
    #    status = "bad"
    #elif re.match(r'^100% tests passed, 0 tests failed out of (\d+)$', l):
    #    status = "good"
    #elif re.match(r'^(\d+)% tests passed, (\d+) tests failed out of (\d+)$', l):
    #    status = "bad"
    elif re.match(r'.*FAIL', l):
        status = "bad"
    elif re.match(r'^ERROR', l):
        status = "bad"
    return status
