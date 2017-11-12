#!/bin/bash

clear

source setBlueprintValues.sh

mkdir -p blueprints

export date1=`date +%d_%m_%Y_%H_%M_%S`
current_bp_ver=bp_${date1}
current_bp_folder=blueprints/${current_bp_ver}
mkdir -p ${current_bp_folder}
mkdir -p ${current_bp_folder}/inputs

echo Replacing $ORIG_PRIMARY_NAME with $PRIMARY_NAME ...
cp -f templates/${ORIG_PRIMARY_NAME}_blueprint.yaml ${current_bp_folder}/${PRIMARY_NAME}_blueprint.yaml
cp -f inputs/${ORIG_PRIMARY_NAME}_inputs_def.yaml ${current_bp_folder}/inputs/${PRIMARY_NAME}_inputs_def.yaml

echo Replacing $ORIG_SECONDARY_NAME with $SECONDARY_NAME ...
cp -f templates/${ORIG_SECONDARY_NAME}_blueprint.yaml ${current_bp_folder}/${SECONDARY_NAME}_blueprint.yaml
cp -f inputs/${ORIG_SECONDARY_NAME}_inputs_def.yaml ${current_bp_folder}/inputs/${SECONDARY_NAME}_inputs_def.yaml
cp -f inputs/${ORIG_SECONDARY_NAME}_inputs.yaml ${current_bp_folder}/inputs/${SECONDARY_NAME}_inputs.yaml

cp -rp types ${current_bp_folder}/types
cp -rp plugins ${current_bp_folder}/plugins

sed -i -e "s+${ORIG_PRIMARY_NAME}+${PRIMARY_NAME}+g" ${current_bp_folder}/${PRIMARY_NAME}_blueprint.yaml
sed -i -e "s+${ORIG_PRIMARY_NAME}+${PRIMARY_NAME}+g" ${current_bp_folder}/inputs/${PRIMARY_NAME}_inputs_def.yaml

sed -i -e "s+${ORIG_PRIMARY_NAME}+${PRIMARY_NAME}+g" ${current_bp_folder}/${SECONDARY_NAME}_blueprint.yaml
sed -i -e "s+${ORIG_SECONDARY_NAME}+${SECONDARY_NAME}+g" ${current_bp_folder}/${SECONDARY_NAME}_blueprint.yaml

sed -i -e "s+${ORIG_PRIMARY_NAME}+${PRIMARY_NAME}+g" ${current_bp_folder}/inputs/${SECONDARY_NAME}_inputs_def.yaml
sed -i -e "s+${ORIG_SECONDARY_NAME}+${SECONDARY_NAME}+g" ${current_bp_folder}/inputs/${SECONDARY_NAME}_inputs_def.yaml

sed -i -e "s+${ORIG_PRIMARY_NAME}+${PRIMARY_NAME}+g" ${current_bp_folder}/inputs/${SECONDARY_NAME}_inputs.yaml
sed -i -e "s+${ORIG_SECONDARY_NAME}+${SECONDARY_NAME}+g" ${current_bp_folder}/inputs/${SECONDARY_NAME}_inputs.yaml


bp_full_path=`pwd`/${current_bp_folder}
echo "======================================================================================"
echo "Your blueprint is in ${bp_full_path}"
echo "Run the following:"
echo "--------------------------------------------------------------------------------------"
echo "cd ${bp_full_path}"
echo "export ${PRIMARY_NAME}_BP=${PRIMARY_NAME}_blueprint"
echo "cfy blueprints upload -b \$${PRIMARY_NAME}_BP ${bp_full_path}/${PRIMARY_NAME}_blueprint.yaml"
echo "export ${PRIMARY_NAME}_DEP=GLOBAL_${PRIMARY_NAME}"
echo "cfy dep cr -b \$${PRIMARY_NAME}_BP \$${PRIMARY_NAME}_DEP --skip-plugins-validation"
echo "cfy exe start install -d \$${PRIMARY_NAME}_DEP"
echo "cfy deployments outputs \$${PRIMARY_NAME}_DEP"
echo "cfy node-instances -v list -d \$${PRIMARY_NAME}_DEP"
echo "--------------------------------------------------------------------------------------"
echo "======================================================================================"
echo ...
read -n 3

rm -rf ${current_bp_folder}

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
