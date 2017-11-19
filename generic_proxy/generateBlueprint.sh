#!/bin/bash

clear

source setBlueprintValues.sh

# Do NOT change these, unless you
# really know what you are doing !!!
export ORIG_PRIMARY_NAME=PRIMARY_NAME
export ORIG_PRIMARY_TYPE=PRIMARY_TYPE
export ORIG_PRIMARY_DEVICE_ELEMENT1_NAME=PRIMARY_DEVICE_ELEMENT1_NAME
export ORIG_PRIMARY_DEVICE_ELEMENT2_NAME=PRIMARY_DEVICE_ELEMENT2_NAME

export ORIG_SECONDARY_NAME=SECONDARY_NAME
export ORIG_SECONDARY_TYPE=SECONDARY_TYPE
export ORIG_SECONDARY_DEVICE_ELEMENT1_NAME=SECONDARY_DEVICE_ELEMENT1_NAME
export ORIG_SECONDARY_DEVICE_ELEMENT2_NAME=SECONDARY_DEVICE_ELEMENT2_NAME


mkdir -p blueprints

export date1=`date +%d_%m_%Y_%H_%M_%S`
current_bp_ver=${folderPrefix}${date1}
current_bp_folder=blueprints/${current_bp_ver}
mkdir -p ${current_bp_folder}
mkdir -p ${current_bp_folder}/inputs

echo Replacing $ORIG_PRIMARY_TYPE with $PRIMARY_TYPE ...
cp -f templates/${ORIG_PRIMARY_TYPE}_blueprint.yaml ${current_bp_folder}/${PRIMARY_TYPE}_blueprint.yaml
cp -f inputs/${ORIG_PRIMARY_TYPE}_inputs_def.yaml ${current_bp_folder}/inputs/${PRIMARY_TYPE}_inputs_def.yaml

echo Replacing $ORIG_SECONDARY_TYPE with $SECONDARY_TYPE ...
cp -f templates/${ORIG_SECONDARY_TYPE}_blueprint.yaml ${current_bp_folder}/${SECONDARY_TYPE}_blueprint.yaml
cp -f inputs/${ORIG_SECONDARY_TYPE}_inputs_def.yaml ${current_bp_folder}/inputs/${SECONDARY_TYPE}_inputs_def.yaml
cp -f inputs/${ORIG_SECONDARY_TYPE}_inputs.yaml ${current_bp_folder}/inputs/${SECONDARY_TYPE}_inputs.yaml

cp -rp types ${current_bp_folder}/types
cp -rp plugins ${current_bp_folder}/plugins

sed -i -e "s+${ORIG_PRIMARY_TYPE}+${PRIMARY_TYPE}+g" ${current_bp_folder}/types/types.yaml

sed -i -e "s+${ORIG_PRIMARY_NAME}+${PRIMARY_NAME}+g" ${current_bp_folder}/${PRIMARY_TYPE}_blueprint.yaml
sed -i -e "s+${ORIG_PRIMARY_TYPE}+${PRIMARY_TYPE}+g" ${current_bp_folder}/${PRIMARY_TYPE}_blueprint.yaml
sed -i -e "s+${ORIG_PRIMARY_DEVICE_ELEMENT1_NAME}+${PRIMARY_DEVICE_ELEMENT1_NAME}+g" ${current_bp_folder}/${PRIMARY_TYPE}_blueprint.yaml
sed -i -e "s+${ORIG_PRIMARY_DEVICE_ELEMENT2_NAME}+${PRIMARY_DEVICE_ELEMENT2_NAME}+g" ${current_bp_folder}/${PRIMARY_TYPE}_blueprint.yaml

sed -i -e "s+${ORIG_PRIMARY_NAME}+${PRIMARY_NAME}+g" ${current_bp_folder}/inputs/${PRIMARY_TYPE}_inputs_def.yaml
sed -i -e "s+${ORIG_PRIMARY_TYPE}+${PRIMARY_TYPE}+g" ${current_bp_folder}/inputs/${PRIMARY_TYPE}_inputs_def.yaml

sed -i -e "s+${ORIG_PRIMARY_NAME}+${PRIMARY_NAME}+g" ${current_bp_folder}/${SECONDARY_TYPE}_blueprint.yaml
sed -i -e "s+${ORIG_PRIMARY_TYPE}+${PRIMARY_TYPE}+g" ${current_bp_folder}/${SECONDARY_TYPE}_blueprint.yaml
sed -i -e "s+${ORIG_SECONDARY_NAME}+${SECONDARY_NAME}+g" ${current_bp_folder}/${SECONDARY_TYPE}_blueprint.yaml
sed -i -e "s+${ORIG_PRIMARY_DEVICE_ELEMENT1_NAME}+${PRIMARY_DEVICE_ELEMENT1_NAME}+g" ${current_bp_folder}/${SECONDARY_TYPE}_blueprint.yaml
sed -i -e "s+${ORIG_PRIMARY_DEVICE_ELEMENT2_NAME}+${PRIMARY_DEVICE_ELEMENT2_NAME}+g" ${current_bp_folder}/${SECONDARY_TYPE}_blueprint.yaml
sed -i -e "s+${ORIG_SECONDARY_NAME}+${SECONDARY_NAME}+g" ${current_bp_folder}/${SECONDARY_TYPE}_blueprint.yaml
sed -i -e "s+${ORIG_SECONDARY_TYPE}+${SECONDARY_TYPE}+g" ${current_bp_folder}/${SECONDARY_TYPE}_blueprint.yaml
sed -i -e "s+${ORIG_SECONDARY_DEVICE_ELEMENT1_NAME}+${SECONDARY_DEVICE_ELEMENT1_NAME}+g" ${current_bp_folder}/${SECONDARY_TYPE}_blueprint.yaml
sed -i -e "s+${ORIG_SECONDARY_DEVICE_ELEMENT2_NAME}+${SECONDARY_DEVICE_ELEMENT2_NAME}+g" ${current_bp_folder}/${SECONDARY_TYPE}_blueprint.yaml

sed -i -e "s+${ORIG_PRIMARY_NAME}+${PRIMARY_NAME}+g" ${current_bp_folder}/inputs/${SECONDARY_TYPE}_inputs_def.yaml
sed -i -e "s+${ORIG_PRIMARY_TYPE}+${PRIMARY_TYPE}+g" ${current_bp_folder}/inputs/${SECONDARY_TYPE}_inputs_def.yaml

sed -i -e "s+${ORIG_SECONDARY_NAME}+${SECONDARY_NAME}+g" ${current_bp_folder}/inputs/${SECONDARY_TYPE}_inputs_def.yaml
sed -i -e "s+${ORIG_SECONDARY_TYPE}+${SECONDARY_TYPE}+g" ${current_bp_folder}/inputs/${SECONDARY_TYPE}_inputs_def.yaml

sed -i -e "s+${ORIG_PRIMARY_NAME}+${PRIMARY_NAME}+g" ${current_bp_folder}/inputs/${SECONDARY_TYPE}_inputs.yaml
sed -i -e "s+${ORIG_PRIMARY_TYPE}+${PRIMARY_TYPE}+g" ${current_bp_folder}/inputs/${SECONDARY_TYPE}_inputs.yaml

sed -i -e "s+${ORIG_SECONDARY_NAME}+${SECONDARY_NAME}+g" ${current_bp_folder}/inputs/${SECONDARY_TYPE}_inputs.yaml
sed -i -e "s+${ORIG_SECONDARY_TYPE}+${SECONDARY_TYPE}+g" ${current_bp_folder}/inputs/${SECONDARY_TYPE}_inputs.yaml

clear
bp_full_path=`pwd`/${current_bp_folder}
echo "======================================================================================"
echo "Your blueprint is in ${bp_full_path}"
echo "Run the following (primary blueprint):"
echo "--------------------------------------------------------------------------------------"
echo "cd ${bp_full_path}"
echo "export ${PRIMARY_TYPE}_BP=${PRIMARY_TYPE}_blueprint"
echo "cfy blueprints upload -b \$${PRIMARY_TYPE}_BP ${bp_full_path}/${PRIMARY_TYPE}_blueprint.yaml"
echo "export ${PRIMARY_NAME}_DEP=${PRIMARY_NAME}"
echo "cfy deployments create -b \$${PRIMARY_TYPE}_BP \$${PRIMARY_NAME}_DEP --skip-plugins-validation"
echo "cfy exe start install -d \$${PRIMARY_NAME}_DEP"
echo "cfy deployments outputs \$${PRIMARY_NAME}_DEP"
echo "cfy node-instances -v list -d \$${PRIMARY_NAME}_DEP"
echo ""
echo "======================================================================================"
echo "Then run the following (secondary blueprint):"
echo "--------------------------------------------------------------------------------------"
echo "export ${SECONDARY_TYPE}_BP=${SECONDARY_TYPE}_blueprint"
echo "export external_blueprint_name=\${${PRIMARY_TYPE}_BP}"
echo "export external_deployment_name=\${${PRIMARY_NAME}_DEP}"
echo "cfy blueprints upload -b \$${SECONDARY_TYPE}_BP ${bp_full_path}/${SECONDARY_TYPE}_blueprint.yaml"
echo "for device_version in {1..3}"
echo "do"
echo "export ${SECONDARY_TYPE}_DEP=${SECONDARY_TYPE}_\${device_version}"
echo "export device_type=${SECONDARY_TYPE}"
echo "cfy deployments create -b \$${SECONDARY_TYPE}_BP \$${SECONDARY_TYPE}_DEP --skip-plugins-validation -i external_deployment_name=\${external_deployment_name} -i external_blueprint_name=\${external_blueprint_name} -i device_type=\"\${device_type}\"&&cfy executions start install -d \$${SECONDARY_TYPE}_DEP&&cfy deployments outputs \$${SECONDARY_TYPE}_DEP &"
echo "done"
echo "======================================================================================"
echo "To remove the SECONDARY stuff, run ... : "
echo "--------------------------------------------------------------------------------------"
echo "for device_version in {1..3}"
echo "do"
echo "export ${SECONDARY_TYPE}_DEP=${SECONDARY_TYPE}_\${device_version}"
echo "cfy executions start uninstall -d \$${SECONDARY_TYPE}_DEP && cfy deployments delete \$${SECONDARY_TYPE}_DEP -f &"
echo "done"
echo "export depCounter=\`cfy deployments list | grep "\${${SECONDARY_TYPE}_BP}" | grep -viE \"\-\-|created_by|^$|Listing|Deployments:\" | wc -l\`"
echo "while [ \$depCounter -ne 0 ]"
echo "do"
echo "echo \"Waiting for deployments to be deleted...\""
echo "sleep 5s"
echo "export depCounter=\`cfy deployments list | grep "\${${SECONDARY_TYPE}_BP}" | grep -viE \"\-\-|created_by|^$|Listing|Deployments:\" | wc -l\`"
echo "done"
echo "cfy blueprints delete \$${SECONDARY_TYPE}_BP"
echo ""
echo "--------------------------------------------------------------------------------------"
echo "To remove the PRIMARY stuff, run ... : "
echo "--------------------------------------------------------------------------------------"
echo "cfy executions start uninstall -d \$${PRIMARY_NAME}_DEP && cfy deployments delete \$${PRIMARY_NAME}_DEP -f&&cfy blueprints delete \$${PRIMARY_TYPE}_BP"
#read -n 1

#rm -rf ${current_bp_folder}

exit

if [ "$#" -lt 3 ]; then
    echo "======================================================================================"
    echo "Usage: $0 111 222 333"
    echo "E.g: "
    echo "   The following will create a new blueprint named ...."
    echo "   which is based onand whose display name is"
    echo "======================================================================================"
    exit 1
else
    echo "Do something ...."
fi

#sed -i -e "s+\(.*\)\($newCloudName\)\(.*\)\($basedOnCloudDisplayName\)\(.*\)+\1\2\3$newCloudDisplayName\5+g" xxx


echo " "
echo "End of $0"
echo "--------------------------------------------------------------------------------------"
exit
