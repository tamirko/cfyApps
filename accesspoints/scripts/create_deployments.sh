#!/bin/bash

pushd ~/
source env331/bin/activate
popd
cfy use -t 185.43.218.204

for i in {81..130}
do
   python create_and_install_deployment.py fire${i} & 
done

deactivate 