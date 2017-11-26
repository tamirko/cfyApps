#!/bin/bash

clear

all_secret_file=~/mngr_secrets

echo "Reading the content of the secrets file (${all_secret_file})."
echo "For importing the secrets to the CFY manager,"
echo "run the following commands (copy and paste them):"
echo "-------------------------------------------------------------------"
for curr_secret_line in `cat ${all_secret_file}`; do
  curr_secret_key=`echo $curr_secret_line | awk -F":" '{ print $1 }'`
  curr_secret_value=`echo $curr_secret_line | awk -F":" '{ print $2 }'`
  echo "cfy secret create -s \"${curr_secret_value}\" $curr_secret_key"
done
echo " "