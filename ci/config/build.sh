#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

envName=$1
echo "${currHostName}:${currFilename} Jenkins build ${envName}..."

if [ "${currentTask}" == "dummy" ]; then
  if [[ "${envName}" =~ "1stTest" ]]; then
    currentTheme="simplecorp"
  else
    currentTheme="selecta"
  fi
  msgID=`date|md5sum|cut -c -10`
  newDir=/tmp/tamir/${envName}${msgID}  
else
  currentTheme=${currentTask}
  newDir=/tmp/tamir/${envName}$currentTask
fi
newDir=/tmp/tamir/${envName}

echo "${currHostName}:${currFilename} Jenkins creating ${newDir}"
mkdir -p ${newDir}
cd ${newDir}

echo "${currHostName}:${currFilename} Jenkins currentTheme is ${currentTheme}"

managerIP=$2
echo dollar 2 is $2
echo dollar 2 is -$2-
echo manager IP is $managerIP
echo manager IP is -${managerIP}-


source /myenv/bin/activate
cfy --v
cfy init -r
cfy use -t ${managerIP}
cfy deployments list

#echo "${currHostName}:${currFilename} Jenkins orig app.json is:"
jenkinsLib=/var/lib/jenkins
export appJsonName=app.json
export origJppJsonPath=`find $jenkinsLib -name "${appJsonName}"`

#cat $origJppJsonPath

midDomainName=`echo $envName | tr [A-Z] [a-z]`
newAppJson=${jenkinsLib}/app${midDomainName}.json
cp -f $origJppJsonPath $newAppJson

sed -i -e "s/REPLACE_WITH_MID_DOMAIN_NAME/$midDomainName/g" $newAppJson

#echo "${currHostName}:${currFilename} Jenkins newAppJson is:"
#cat $newAppJson

# ===================================
function blueprintExist {	
	doesSuchBlueprintExist=`cfy blueprints list | grep -c "$1"`
	return $doesSuchBlueprintExist		
}

function deploymentExist {	
	doesSuchDeploymentExist=`cfy deployments list | grep -c "$1"`
	return $doesSuchDeploymentExist		
}

function executionsExist {	
	cfy executions list -d $1 > dummy
	retVal=$?
	rm dummy
	if [ $retVal -ne 0 ]; then		
		# Executions do not exist
		return 0
	fi	
	# Executions exist	
	return 1
}

function copyCurrent2Previous {	
	pushd $2
	cp -rp $1/* .
	popd
}

export prevFolderPath=`pwd`/prev
mkdir -p $prevFolderPath

export gitMainfolder=cfyApps
export blueprintFolderName=drupalAndMemcached
export blueprintYamlName=sl_drupalAndMemcached_blueprint.yaml
export blueprintName=drupalAndMemcached
export deploymentName=drupal${envName}

rm -rf $gitMainfolder
git clone https://github.com/tamirko/cfyApps.git
pushd $gitMainfolder
newBlueprintsExists=`diff -rq $blueprintFolderName $prevFolderPath | grep -vc gitignore`
if [ $newBlueprintsExists -gt 0 ]; then
  echo "Found differences - Building again"
  executionsExist $deploymentName
  execsExists=$?
   
  if [ $execsExists -gt 0 ]; then
    echo "Cancelling started executions if exist ... "
    echo "cfy executions list -d $deploymentName \| grep started \| awk -F\\\| '{print $2}' \| sed 's/ //g' \| xargs -I file cfy executions cancel -e file -f"
    cfy executions list -d $deploymentName | grep started | awk -F\| '{print $2}' | sed 's/ //g' |  xargs -I file cfy executions cancel -e file -f

    echo cfy executions start -d $deploymentName -w uninstall -f
    cfy executions start -d $deploymentName -w uninstall -f
  fi
  
  deploymentExist $deploymentName
  depExists=$?
  if [ $depExists -gt 0 ]; then 
    echo cfy deployments delete -d $deploymentName
    cfy deployments delete -d $deploymentName
  fi
  
  blueprintExist $blueprintName
  bpExists=$?
  if [ $bpExists -gt 0 ]; then
    echo cfy blueprints delete -b $blueprintName 
    cfy blueprints delete -b $blueprintName 
  fi
  
  echo cfy blueprints upload -p ${blueprintFolderName}/${blueprintYamlName} -b $blueprintName
  cfy blueprints upload -p ${blueprintFolderName}/${blueprintYamlName} -b $blueprintName
  if [ $? -eq 0 ]; then
    echo cfy deployments create -d $deploymentName -i $newAppJson -b $blueprintName
    cfy deployments create -d $deploymentName -i $newAppJson -b $blueprintName
	if [ $? -eq 0 ]; then
	  sleep 70s
	  echo cfy executions start -d $deploymentName -w install
	  cfy executions start -d $deploymentName -w install
	  if [ $? -eq 0 ]; then
	    currFolder=`pwd`
	    copyCurrent2Previous ${currFolder}/${blueprintFolderName} $prevFolderPath
	    sleep 70s
	    echo cfy deployments outputs -d $deploymentName
	    cfy deployments outputs -d $deploymentName
		if [ $? -eq 0 ]; then
		  cfy executions start -d $deploymentName -p "{\"variable_name\":\"site_name\", \"variable_value\":\"${midDomainName}\"}" -w drush_setvar
		  if [ $? -eq 0 ]; then
		    cfy executions start -d $deploymentName  -w drush_install -p "{\"project_name\":\"${currentTheme}\"}"
			if [ $? -eq 0 ]; then
			  cfy executions start -d $deploymentName -w drush_setvar -p "{\"variable_name\":\"theme_default\", \"variable_value\":\"${currentTheme}\"}"
			  if [ $? -eq 0 ]; then
			    echo "All is well"
			  else
			    echo "cfy executions set default theme ${currentTheme} failed"
			  fi
			else
			  echo "cfy executions download of ${currentTheme} failed"
			fi
          else
		    echo "cfy executions set site_name ${midDomainName} failed"
          fi          
		else
		  echo "cfy deployments outputs failed"
		fi        
	  else
	    echo "cfy executions installation failed"
	  fi
	else
	  echo "cfy deployments create failed"
	fi
  else
    echo "cfy blueprints upload failed"
  fi    
  # set site name - env name ...
  # set theme
else
  echo "Jenkins No differences exist - Aborting build - successfully"  
fi


deactivate
echo "${currHostName}:${currFilename} End of Jenkins build $1"
