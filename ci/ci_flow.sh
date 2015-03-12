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
cfy bootstrap --install-plugins -p $mainMngrBlueprintPath -i $mainMngrJsonPath

#cp $envMngrBlueprintFile $envMngrBlueprintPath
echo AAA cfy blueprints upload -p $envMngrBlueprintPath -b $envMngrBlueprintName  
cfy blueprints upload -p $envMngrBlueprintPath -b $envMngrBlueprintName  

mainMngrIP=`cfy --v |& grep "Manager" | cut -d= -f2 | sed 's/.$//'`
echo AAA mainMngrIP is $mainMngrIP


declare -a managers=("Dev" "Tests" "QA" "Staging" "Production")
declare -a ipAddresses=("${placeHolder}" "${placeHolder}" "${placeHolder}" "${placeHolder}" "${placeHolder}")

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
  echo AAA cfy executions start -d $currDeployment --timeout 4500 -w install
  cfy executions start -d $currDeployment --timeout 4500 -w install
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
      cfy deployments outputs -d $currEnvName | grep Value |  awk -F": " '{print $NF}' | sed 's/.$//'	  
      currIp=`cfy deployments outputs -d $currEnvName | grep Value |  awk -F": " '{print $NF}' | sed 's/.$//'`      
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

echo Managers IP addresses are:
for index in ${!managers[*]}
do  
  echo ${managers[$index]} : ${ipAddresses[$index]}
done
  
echo Environments  \: ${#managers[*]}
echo Live managers \: ${livemanagers}
  
 
exit 


cfy deployments outputs -d dr0503_dep

Getting outputs for deployment: dr0503_dep [manager=119.81.178.105]
 - "endpoint":
     Description: My application endpoint
     Value: {u'public_ip': ${placeHolder}}
  