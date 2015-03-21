#!/bin/bash

clear

export virtualEnvName=myenv
export mainMngrBlueprintFile=sl_main_mngr.yaml
export mainMngrBlueprintPath=/root/cloudify-manager-blueprints/softlayer/$mainMngrBlueprintFile
export mainMngrJson=sl_main_mngr.json
export mainMngrJsonPath=/root/cloudify-manager-blueprints/softlayer/$mainMngrJson
export mainMngrBlueprintName=cfyMngr

export envMngrBlueprintFile=sl_env_mngr.yaml
export envMngrBlueprintPath=/root/cloudify-manager-blueprints/softlayer/$envMngrBlueprintFile
export envOrigMngrJson=sl_env_mngr.json
export envOrigMngrJsonPath=/root/cloudify-manager-blueprints/softlayer/$envOrigMngrJson
export envMngrBlueprintName=cfyManagerEnv

export placeHolder=None

source ${virtualEnvName}/bin/activate
echo AAA cfy init -r
cfy init -r
#cp $mainMngrBlueprintFile $mainMngrBlueprintPath
echo AAA cfy bootstrap --install-plugins -p $mainMngrBlueprintPath -i $mainMngrJsonPath
date1=$(date +"%s")
cfy bootstrap --install-plugins -p $mainMngrBlueprintPath -i $mainMngrJsonPath
date2=$(date +"%s")
diff=$(($date2-$date1))
echo "TIMEINFO bootstrap took $(($diff / 60)) minutes and $(($diff % 60)) seconds."
#cp $envMngrBlueprintFile $envMngrBlueprintPath
echo AAA cfy blueprints upload -p $envMngrBlueprintPath -b $envMngrBlueprintName  
cfy blueprints upload -p $envMngrBlueprintPath -b $envMngrBlueprintName  

mainMngrIP=`cfy --v |& grep "Manager" | cut -d= -f2 | sed 's/.$//'`
echo AAA mainMngrIP is $mainMngrIP

declare -a managers=("AB1stTest" "AB2ndTest" "Production")
declare -a ipAddresses=("${placeHolder}" "${placeHolder}" "${placeHolder}")

echo Iterating on the ${#managers[*]} envs : ${managers[*]}

for managerEnv in "${managers[@]}"
do
  currDeployment=${managerEnv}Env
  currDeploymentLower=`echo $currDeployment | tr [A-Z] [a-z]`
  managerEnvJson=${managerEnv}.json
  sed "s/ENV/${currDeploymentLower}/" ${envOrigMngrJsonPath}  > ${managerEnvJson}
  grep -i domain ${managerEnvJson} | sed 's/[ ",]//g'
  echo AAA cfy deployments create -d $currDeployment -i ${managerEnvJson} -b $envMngrBlueprintName
  cfy deployments create -d $currDeployment -i ${managerEnvJson} -b $envMngrBlueprintName
  sleep 70s
  envDate1=$(date +"%s")
  echo AAA cfy executions start -d $currDeployment --timeout 4500 -w install
  cfy executions start -d $currDeployment --timeout 4500 -w install
  envDate2=$(date +"%s")
  diff=$(($envDate2-$envDate1))
  echo "TIMEINFO ${currDeploymentLower} installation took $(($diff / 60)) minutes and $(($diff % 60)) seconds."
  echo "---------------------------------------"
done

livemanagers=0
while [ $livemanagers -lt ${#managers[*]} ];
do
  echo Waiting for the ${#managers[*]} managers : ${managers[*]}
  echo Live managers \: ${livemanagers}
  for index in ${!managers[*]}
  do
    currEnvName=${managers[$index]}Env
    currEnvMngrIP=${ipAddresses[$index]}
    if [ "${currEnvMngrIP}" == "${placeHolder}" ]; then      
      echo Waiting for $currEnvName ...	  
      echo AAA cfy deployments outputs -d $currEnvName | grep Value |  awk -F": " '{print $NF}' | sed 's/.$//'
      cfy deployments outputs -d $currEnvName
      origCurrIp=`cfy deployments outputs -d $currEnvName | grep Value |  awk -F": " '{print $NF}'`      
      raw2CurrIp=`cfy deployments outputs -d $currEnvName | grep Value |  awk -F": " '{print $NF}' | sed 's/.$//'`
      if [ "${origCurrIp}" == "${raw2CurrIp} " ]; then
        #echo "AAA need to remove last char - space "
        currIp=$raw2CurrIp
      else
        #echo "AAA NO need to remove last char"
        currIp=$origCurrIp	  
      fi
      currErrorLevel=$?
      if [ $currErrorLevel -ne 0 ]; then
        echo "XXX Error in 'cfy deployments outputs -d ${currEnvName} ...'"
      fi
      if [ "${currIp}" != "${placeHolder}" ]; then
        if [ "${currIp}" == "" ]; then
          echo "XXX currIp is empty ..."
        else
          echo Storing $currEnvName ip address \(${currIp}\)
          ipAddresses[$index]="${currIp}"
          let livemanagers=$livemanagers+1
        fi		 
      fi
    else
      echo ${currEnvName} ip address is already set \(${currEnvMngrIP}\)
    fi
    echo "- - - - - - - - - - - - - - - - - - - -"
  done
  sleep 10s
done

echo Environments  \: ${#managers[*]}
echo Live managers \: ${livemanagers}

echo "Installing Jenkins ... "
export bp=jenkinsBp
export dep=jenkinsDep
cfy blueprints upload -p cfyApps/ci/sl_ci.yaml -b $bp
currJson=cfyApps/ci/sl_ci.json
testEnvs="${managers[0]} ${managers[1]}"
testManagers="${ipAddresses[0]} ${ipAddresses[1]}"
sed -i -e "s/REPLACE_WITH_SPACE_SEPARTED_ENVRIONMENTS/$testEnvs/g" $currJson  
sed -i -e "s/REPLACE_WITH_SPACE_SEPARTED_IP_ADDRESSES/$testManagers/g" $currJson
prodEnv="${managers[2]}"
prodIP="${ipAddresses[2]}"
sed -i -e "s/REPLACE_WITH_PROD_ENVRIONMENT/$prodEnv/g" $currJson  
sed -i -e "s/REPLACE_WITH_PROD_IP_ADDRESS/$prodIP/g" $currJson
cfy deployments create -d $dep -i $currJson -b $bp
sleep 70s
bpDate1=$(date +"%s")  
cfy executions start -d $dep --timeout 4500 -w install
bpDate2=$(date +"%s")
diff=$(($bpDate2-$bpDate1))
echo "TIMEINFO installation of the Jenkins blueprint on ${currEnv} took $(($diff / 60)) minutes and $(($diff % 60)) seconds."
# The following can be used to kill all the vms
echo "#!/bin/bash"> cleanFlow.sh
echo "mkdir -p /.cloudify/bootstrap/manager/data">> cleanFlow.sh
echo "cfy init -r">> cleanFlow.sh

for currManagerIP in "${ipAddresses[@]}"
do
 echo "cfy use -t ${currManagerIP}" >> cleanFlow.sh
# Uninstall all apps
 echo "cfy deployments list | grep -i \"drupal\" | awk -F\| '{print \$2}' | sed 's/ //g' | xargs -I file cfy executions list -d file \| grep install \| grep -v uninstall \| grep started |  awk -F\| '{print \$2}' | sed 's/ //g' |  xargs -I file cfy executions cancel -e file -f" >> cleanFlow.sh
 echo "cfy deployments list | grep -i \"drupal\" | awk -F\| '{print \$2}' | sed 's/ //g' | xargs -I file cfy executions start -d file -f -w uninstall" >> cleanFlow.sh
# Delete all deployments
 echo "cfy deployments list | grep -i \"drupal\" | awk -F\| '{print \$2}' | sed 's/ //g' | xargs -I file cfy deployments delete -f -d file">> cleanFlow.sh
# Delete all blueprints
 echo "cfy blueprints list | grep -i \"drupal\" | awk -F\| '{print \$2}' | sed 's/ //g' | xargs -I file cfy blueprints delete -b file">> cleanFlow.sh
 echo "cfy teardown -f --ignore-deployments">> cleanFlow.sh
done  

echo "cfy use -t $mainMngrIP">> cleanFlow.sh
# Uninstall all apps
echo "cfy deployments list | grep -iE \"Env|jenk\" | awk -F\| '{print \$2}' | sed 's/ //g' | xargs -I file cfy executions list -d file | grep install | grep -v uninstall | grep started |  awk -F\| '{print \$2}' | sed 's/ //g' |  xargs -I file cfy executions cancel -e file -f">> cleanFlow.sh
echo "cfy deployments list | grep -iE \"Env|jenk\" | awk -F\| '{print \$2}' | sed 's/ //g' | xargs -I file cfy executions start -d file -f -w uninstall">> cleanFlow.sh
# Delete all deployments
echo "cfy deployments list | grep -iE \"Env|jenk\" | awk -F\| '{print \$2}' | sed 's/ //g' | xargs -I file cfy deployments delete -f -d file">> cleanFlow.sh
# Delete all blueprints
echo "cfy blueprints list | grep -iE \"Env|jenk\" | awk -F\| '{print \$2}' | sed 's/ //g' | xargs -I file cfy blueprints delete -b file">> cleanFlow.sh
echo "cfy teardown -f --ignore-deployments">> cleanFlow.sh
echo "echo end of \$0">> cleanFlow.sh
 
totalDate=$(date +"%s")
diff=$(($totalDate-$date1))
echo "TIMEINFO The creation of the whole env took $(($diff / 60)) minutes and $(($diff % 60)) seconds."
exit 

#cfy executions start -d myDeployment -p '{"variable_name":"site_name", "variable_value":"My_New_Site_Name"}' -w drush_setvar
