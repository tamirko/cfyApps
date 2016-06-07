#!/bin/bash

pushd ~/
source env331/bin/activate
popd
cfy use -t 185.43.218.204

for i in {40..60}
do
   python delete_deployment.py fire${i} & 
done

deactivate 