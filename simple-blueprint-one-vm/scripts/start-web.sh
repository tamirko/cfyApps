#! /bin/bash

ctx logger info "b4 set e `whoami`"
set -e

currStat=$?
ctx logger info "b4 mkdir2 stat of prev $currStat"
export myWeb=~/myweb
mkdir -p ${myWeb}
currStat=$?
ctx logger info "b4 cd stat of prev $currStat"
cd ${myWeb}
currStat=$?
ctx logger info "b4 cd python stat of prev $currStat"
COMMAND="python -m SimpleHTTPServer 8000"
currStat=$?
ctx logger info "b4 cd nohup stat of prev $currStat"
nohup ${COMMAND} > /dev/null 2>&1 &
currStat=$?
ctx logger info "b4 was here stat of prev $currStat"
echo ">>>>> Cloudify was here..." >> ~/cloudify.txt
currStat=$?
ctx logger info "End of $0 stat of prev $currStat"