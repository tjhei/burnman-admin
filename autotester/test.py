# timo.heister@gmail.com

import os
import sys
import subprocess
import simplejson
from datetime import datetime

repodir = os.path.abspath("burnman")

color_green = "#99ff99"
color_red = "#ff0000"

def date_to_epoch(dt):
    epoch = datetime.utcfromtimestamp(0)
    return (dt-epoch).total_seconds()

def epoch_to_date(seconds):
    return datetime.utcfromtimestamp(seconds)

def text_to_html(text):
    lines = text.split("\n")
    outlines = []
    for l in lines:
        if l.endswith(" ... ok"):
            outlines.append("<p style='background-color:{0}'>{1}</p>".format(color_green, l))
        elif l.endswith(" ... FAIL"):
            outlines.append("<p style='background-color:{0}'>{1}</p>".format(color_red, l))
        else:
            outlines.append("{0}<br/>".format(l))
    
    return "".join(outlines)

class history:
    def __init__(self):
        self.data = dict()
        self.dbname = "test.db"
        self.timeformat = "%Y-%m-%d %H:%M:%S"
        #self.data
        
    def load(self):
        f = open(self.dbname, 'r')
        text = f.read()
        f.close()
        self.data = simplejson.loads(text)
        #print "loading {0} entries...".format(len(self.data))

    def save(self):
        text = simplejson.dumps(self.data)
        print "saving {0} entries...".format(len(self.data))
        f = open(self.dbname, 'w')
        f.write(text)
        f.close()

    def sort_keys(self):
        keys = []
        for x in self.data.values():
            timeint = 0
            try:
                timeint = int(x['time'])
            except:
                pass
            keys.append((x['sha'], timeint))
        
        return sorted(keys, key=lambda x: x[1], reverse=True)


    def dump(self):
        print "dumping {0} entries".format(len(self.data))

        sorted_keys = self.sort_keys()

        print "SHA pass fail time:"
        for sha in sorted_keys:
            x = self.data[sha[0]]
            timestr = "?"
            try:
                dt = epoch_to_date(x['time'])
                timestr = dt.strftime(self.timeformat)
            except:
                pass
            print "{0} {2} {3} ({1})".format(x['sha'], timestr, x['npass'], x['nfail'])
    
    def render(self):
        f = open ("results.html", "w")

        f.write("<html><body><h1>Test Results</h1><br/>\n")

        f.write("<script>function toggle(id) {var o = document.getElementById(id);if (o.style.display=='none') o.style.display='table-row'; else o.style.display='none'; }</script>\n")
        f.write("<table border=1 width='100%' style='border-collapse:collapse'>\n")
        
        sorted_keys = self.sort_keys()

        f.write("<tr><td width='1%'>SHA1</td><td>PASS</td><td>FAIL</td><td>Time</td><td>Comment</td><td>Details</td></tr>\n")
        for sha in sorted_keys:
            x = self.data[sha[0]]
            timestr = "?"
            try:
                dt = epoch_to_date(x['time'])
                timestr = dt.strftime(self.timeformat)
            except:
                pass
            
            details = "<a href='#' onclick='toggle(\"sha{0}\")'>click</a>".format(x['sha'])
            failtext = "<p style='background-color:#99ff99'>{0}</p>".format(x['nfail'])
            if x['nfail']>0:
                failtext = "<p style='background-color:#ff0000'>{0}</p>".format(x['nfail'])
            comment = ""
            if 'comment' in x.keys():
                comment = x['comment']
            f.write("<tr><td>{0}</td><td>{2}</td><td>{3}</td><td>{1}</td><td>{4}</td><td>{5}</td></tr>\n".format(x['sha'][0:10], timestr, x['npass'], failtext, comment, details))
            text = text_to_html(x['text'])
            f.write("<tr id='sha{0}' style='display: none'><td colspan='6'>{1}<br/>{2}</td></tr>\n".format(x['sha'], x['sha'], text))

        f.write("</table>\n")

        f.write("</body></html>")

        f.close()

    def have(self, sha):
        return sha in self.data.keys()

    def delete(self, sha):
        if sha in self.data.keys():
            self.data.pop(sha)
            return

        count = 0
        for k in self.data.keys():
            if k.startswith(sha):
                count = count + 1

        if count==0:
            print "ERROR: sha1 not found."
        elif count==1:
            for k in self.data.keys():
                if k.startswith(sha):
                    self.data.pop(k)
                    return
        else:
            print "ERROR: sha1 is not unique"
            

    def add(self, sha, text, comment):
        time = date_to_epoch(datetime.now())
        npass = 0
        nfail = 0
        for l in text.split("\n"):
            if l.endswith(" ... ok"):
                npass = npass + 1
            elif l.endswith(" ... FAIL"):
                nfail = nfail + 1

        #print time
        entry = dict(sha=sha, time=time, npass=npass, nfail=nfail, text=text, comment=comment)
        self.data[sha] = entry


def test(repodir, h, comment=""):
    sha1 = subprocess.check_output("cd {0};git rev-parse HEAD".format(repodir),
                                   shell=True).replace("\n","")
    print "running", sha1
    answer = subprocess.check_output("cd {0};./test.sh".format(repodir, sha1),
                                     shell=True,stderr=subprocess.STDOUT)

    answer.replace(repodir,"$BURNMAN")
    h.add(sha1, answer, comment)
    h.render()
    h.save()


whattodo = ""

if len(sys.argv)<3:
    print "usage:"
    print "test.py run all"
    print "test.py delete <sha1>"
    print "test.py render it"    
    print "test.py new db"
    print "test.py pull requests"
    print "test.py test user/repo:ref"
else:
    whattodo = sys.argv[1]
    arg1 = sys.argv[2]

if whattodo=="new" and arg1=="db":
    h = history()
    h.save()

if whattodo != "":
    h = history()
    h.load()
    
if whattodo == "delete":
    h.delete(arg1)
    h.render()
    h.save()

if whattodo == "pull" and arg1 == "requests":
    import urllib2
    #r = requests.get("https://api.github.com/repos/burnman-project/burnman/pulls").content
    r = urllib2.urlopen("https://api.github.com/repos/burnman-project/burnman/pulls").read()
    data = simplejson.loads(r)
    print "found {0} pull requests...".format(len(data))
    for pr in data:
        by = pr['user']['login']
        title = pr['title']
        print "PR/{0}: '{2}' by {1} ".format(pr['number'], by, title)
        print "  use: python test.py test {0}:{1}".format(pr['head']['repo']['full_name'],pr['head']['ref'])
        #print pr['id']
    #for pr in data:
    #    print pr['id']

if whattodo =="test":
    userrepo, ref = arg1.split(":")
    ret = subprocess.check_call("cd {0} && git fetch https://github.com/{1} {2}".format(repodir, userrepo, ref), shell=True)
    ret = subprocess.check_call("cd {0} && git checkout FETCH_HEAD".format(repodir), shell=True)
    
    test(repodir, h, arg1)
    
    ret = subprocess.check_call("cd {0} && git checkout master -q".format(repodir), shell=True)

if whattodo == "run" and arg1=="all":
    print repodir

    ret = subprocess.check_call("cd {0} && git checkout master -q".format(repodir), shell=True)
    ret = subprocess.check_call("cd {0} && git pull origin -q".format(repodir), shell=True)

    answer = subprocess.check_output("cd {0};git log --format=oneline -n 10 --reverse".format(repodir),
                                     shell=True,stderr=subprocess.STDOUT)
    lines = answer.split("\n")
    for l in lines:
        sha1 = l.split(" ")[0]
        if len(sha1)!=40:
            continue
        if not h.have(sha1):
            
            ret = subprocess.check_call("cd {0};git checkout {1} -q".format(repodir, sha1),
                                        shell=True)

            test(repodir, h)
        
        else:
            pass

    ret = subprocess.check_call("cd {0} && git checkout master -q".format(repodir), shell=True)

if whattodo !="":
    h.render()






    


    
