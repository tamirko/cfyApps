#!/bin/bash

clear

export virtualEnvName=myenv
export mainMngrBlueprintFile=softlayer_main_mngr.yaml
export mainMngrBlueprintPath=/root/cloudify-manager-blueprints/softlayer/$mainMngrBlueprintFile
export mainMngrJson=sl_main_mngr.json
export mainMngrBlueprintName=cfyMngr

export envMngrBlueprintFile=softlayer_env_mngr.yaml
export envMngrBlueprintPath=/root/cloudify-manager-blueprints/softlayer/$envMngrBlueprintFile
export envOrigMngrJson=sl_env_mngr.json
export envMngrBlueprintName=envMngr

export placeHolder=None

echo cfy init
echo source ${virtualEnvName}/bin/activate
cp $mainMngrBlueprintFile $mainMngrBlueprintPath
echo cfy bootstrap --install-plugins -p $mainMngrBlueprintPath -i $mainMngrJson

cp $envMngrBlueprintFile $envMngrBlueprintPath
echo cfy blueprints upload -p $envMngrBlueprintPath -b $envMngrBlueprintName  

declare -a managers=("Dev" "Tests" "QA" "Staging" "Production")
declare -a ipAddresses=("${placeHolder}" "${placeHolder}" "${placeHolder}" "${placeHolder}" "${placeHolder}")

echo Iterating on the ${#managers[*]} envs : ${managers[*]}

for managerEnv in "${managers[@]}"
do 
  currDeployment=${managerEnv}Env
  currDeploymentLower=`echo $currDeployment | tr [A-Z] [a-z]`
  managerEnvJson=${managerEnv}.json
  sed "s/ENV/${currDeploymentLower}/" ${envOrigMngrJson}  > ${managerEnvJson}
  grep -i domain ${managerEnvJson} | sed 's/[ ",]//g'
  echo cfy deployments create -d $currDeployment -i ${managerEnvJson} -b $envMngrBlueprintName
  echo cfy executions start -d $currDeployment -w install
  echo "---------------------------------------"
done

livemanagers=0
while [ $livemanagers -lt ${#managers[*]} ];
do
 echo Waiting for the ${#managers[*]} managers : ${managers[*]}
 echo Live managers \: ${livemanagers}
 for index in ${!managers[*]}
 do
   currEnvName=${managers[$index]}
   currEnvMngrIP=${ipAddresses[$index]}
   if [ "${currEnvMngrIP}" == "${placeHolder}" ]; then
     echo Waiting for $currEnvName ...
     # cfy deployments outputs -d dr0503_dep | grep public |  cut -d: -f3 | sed 's/.$//g' |  sed 's/^.//g'
     # cfy deployments outputs -d dr0503_dep | grep public |  awk -F": " '{print $NF}' | sed 's/.$//'
   
     currIp=`grep public ${currEnvName}Ip |  awk -F": " '{print $NF}' | sed 's/.$//'`
	 currErrorLevel=$?
	 if [ $currErrorLevel -ne 0 ]; then
		echo "XXX Error in 'grep public ${currEnvName}Ip ...'"
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
  