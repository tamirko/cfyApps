#!/bin/bash

clear

all_secret_keys=`cfy secret li | grep -vEi "\-\-|Secrets| updated_at|^$" | grep "\|" | awk -F"|" '{ print $2 }' | sed -e 's/ //g'`
all_secret_keys=($all_secret_keys)


all_secret_file=~/mngr_secrets
rm -rf $all_secret_file
touch $all_secret_file

for curr_secret_key in "${all_secret_keys[@]}"; do
  curr_secret_value=`cfy secret get ${curr_secret_key} | grep "value:" | awk -F"value:" '{ print $2 }' | awk '{$1=$1};1'`
  #echo "${curr_secret_key}:${curr_secret_value}"
  echo "${curr_secret_key}:${curr_secret_value}" >> $all_secret_file
done

echo "The secrets file is ${all_secret_file}"
echo "and its content (key:value) is:"
cat $all_secret_file
