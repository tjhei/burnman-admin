#!/bin/bash

echo "`date`: `pwd`/run.sh"

lockdir=`pwd`/.lockdir
mkdir $lockdir >/dev/null 2>&1
if [ $? -ne 0 ];
then
  echo "Lock is active. Exiting."
  exit 42
fi

docker_image="tjhei/burnman"

# this is because I am running docker inside a VM:
#/local/docker-tests/boot2docker-v1.4.1-linux-amd64 start


dockercmd_indirect()
{
cmd=$1
mount="-v `pwd`:/main"
all="docker run --rm=true $mount $docker_image /bin/bash -c \"$cmd\""
echo "cmd: '$all'"
/local/docker-tests/boot2docker-v1.4.1-linux-amd64 ssh "$all"
}

# if you run directly rename this to dockercmd:
dockercmd()
{
cmd=$1
mount="-v `pwd`:/main"
all="run --rm=true $mount -h docker-`hostname` $docker_image /bin/bash -c \"$cmd\""
echo "docker $all"
eval docker $all
}


#test:
#dockercmd "cd /main; python runner.py"
#dockercmd "cd /main;python runner.py do-current"

dockercmd "cd /main; python runner.py run-all"

echo "now pull requests"
dockercmd "cd /main; python runner.py do-pullrequests"

echo "rendering:"
dockercmd "cd /main;python runner.py render"

echo "copying data"

rsync -az results.html logs/ timo.ces:public_html/burnman-logs/

echo "exiting."
rmdir $lockdir >/dev/null 2>&1
