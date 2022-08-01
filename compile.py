import yaml
import sys
import getopt
import shutil
import re
import urllib.request
import zipfile
import os
import pathlib
import subprocess
from contextlib import contextmanager
from PlumedToHTML import test_plumed, get_html

if not (sys.version_info > (3, 0)):
   raise RuntimeError("We are using too many python 3 constructs, so this is only working with python 3")

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def process_egg(path,eggdb=None):
    if not eggdb:
        eggdb=sys.stdout

    with cd(path):
        stram = open("lesson.yml", "r")
        config=yaml.load(stram,Loader=yaml.BaseLoader)
        # check fields
        for field in ("url","instructors","title"):
            if not field in config:
               raise RuntimeError(field+" not found")
        print(path,config)

        #if re.match("^.*\.zip$",config["url"]):
        if os.path.exists("download"):
           shutil.rmtree("download")
        os.mkdir("download")
        # try to download
        try:
         urllib.request.urlretrieve(config["url"], 'file.zip')
        except urllib.error.URLError:
         return
        # try to open the zip file
        try:
          zf = zipfile.ZipFile("file.zip", "r")
        except zipfile.BadZipFile:
          return
        zf_namelist = zf.namelist()
        root=list(set([ x.split("/")[0] for x in zf_namelist]))
        # there is a main root directory
        if(len(root)==1 and len(zf_namelist)!=1): root="download/" + root[0]
        # there is not (or special case of one single file)
        else:        root="download/"
        zf.extractall(path="download")
        if os.path.exists("data"):
           shutil.rmtree("data")
        shutil.move(root,"data")

        # Check for the existence of a README file
        if not os.path.exists("data/README.md") : 
           raise RuntimeError("No README.md file found in lesson")
 
        # Get the lesson id from the path
        lesson_id = path[5:7] + "." + path[8:11]
        print("- id: '" + egg_id + "'",file=eggdb)
        print("  title: " + config["title"],file=eggdb)
        print("  path: " + path, file=eggdb)
        print("  instructors: " + config["instructors"],file=eggdb)
      

if __name__ == "__main__":
    nreplicas, replica, argv = 1, 0, sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"hn:r:",["nreplicas=","replica="])
    except:
       print('compile.py -n <nreplicas> -r <replica number>')

    for opt, arg in opts:
       if opt in ['-h'] :
          print('compile.py -n <nreplicas> -r <replica number>')
          sys.exit()
       elif opt in ["-n", "--nreplicas"]:
          nreplicas = int(arg)
       elif opt in ["-r", "--replica"]:
          replica = int(arg)
    print("RUNNING", nreplicas, "REPLICAS. THIS IS REPLICA", replica )
    # write plumed version to file
    stable_version=subprocess.check_output('plumed info --version', shell=True).decode('utf-8').strip()
    f=open("_data/plumed.yml","w")
    f.write("stable: v%s" % str(stable_version))
    f.close()
    with open("_data/lessons" + str(replica) + ".yml","w") as eggdb:
        print("# file containing lesson database.",file=eggdb)

        # list of paths - not ordered
        pathlist=list(pathlib.Path('.').glob('lessons/*/*/lesson.yml'))
        # Reduce the number of lesson by reading in the eggs to use from a file -- used for testing
        if os.path.exists("selected_lessons.dat") :
           pathlist = []
           with open("selected_lessons.dat", "r") as file:
              for readline in file : pathlist.append( pathlib.Path( './' + readline.strip() ) )
        # cycle on ordered list
        k=0
        for path in sorted(pathlist, reverse=True, key=lambda m: str(m)):

            if k%nreplicas==replica : process_lesson(re.sub("lesson.yml$","",str(path)),eggdb)
            k = k + 1
