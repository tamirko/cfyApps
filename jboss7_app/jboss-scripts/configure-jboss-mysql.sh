#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

DIR=/tmp
cd $DIR/

jboss_root_folder=$(ctx source instance runtime_properties jboss_root_folder)

ctx logger info "${currHostName}:${currFilename} Downloading Jboss from ${jboss_downloadPath} ..."


datasource_demo_war_url=$(ctx source node properties datasource_demo_war_url)
warFile=$(ctx source node properties warFileName)


ctx logger info "${currHostName}:${currFilename} Downloading demo war file from ${datasource_demo_war_url} to `pwd`..."
wget -O $warFile ${datasource_demo_war_url}
currStatus=$?
ctx logger info "${currHostName}:${currFilename} wget -O $warFile ${datasource_demo_war_url} -currStatus=${currStatus}"

export applicationWarFolder=${jboss_root_folder}/standalone/deployments/
mv -f ${warFile} ${applicationWarFolder}
currStatus=$?
ctx logger info "${currHostName}:${currFilename} mv -f ${warFile} ${applicationWarFolder} -currStatus=${currStatus}"


mysql_connector_url=$(ctx source node properties mysql_connector_url)

export jdbcDriverName=$(ctx source node properties jdbcDriverName)
ctx logger info "${currHostName}:${currFilename} Downloading mysql connector jar file from ${mysql_connector_url} to `pwd`..."
wget -O $jdbcDriverName ${mysql_connector_url}
currStatus=$?
ctx logger info "${currHostName}:${currFilename} wget -O $jdbcDriverName ${mysql_connector_url} -currStatus=${currStatus}"

mv -f ${jdbcDriverName} ${applicationWarFolder}
currStatus=$?
ctx logger info "${currHostName}:${currFilename} mv -f ${jdbcDriverName} ${applicationWarFolder} -currStatus=${currStatus}"


chmod +x ${jboss_root_folder}/bin/*.sh
currStatus=$?
ctx logger info "${currHostName}:${currFilename} chmod +x ${jboss_root_folder}/bin/*.sh -currStatus=${currStatus}"

export destStandaloneXmlFile=${jboss_root_folder}/standalone/configuration/standalone.xml
rm -rf $destStandaloneXmlFile
ctx download-resource "jboss-scripts/standalone.xml" "@{\"target_path\": \"$destStandaloneXmlFile\"}"

export jbossPort=$(ctx source node properties jbossPort)
export portStr="port=\"${jbossPort}\""
sed -i -e "s/port=\"8080\"/$portStr/g" $destStandaloneXmlFile

export allZeroes="0.0.0.0"
sed -i -e "s/\(.*inet-address.*\)\(127\.0\.0\.1\)\(.*\)/\1${allZeroes}\3/g" $destStandaloneXmlFile

sed -i -e "s/\(.*extension.*\)\(\.osgi\)//g" $destStandaloneXmlFile


databaseName=$(ctx target node properties dbName)
ctx logger info "${currHostName}:${currFilename} :databaseName ${databaseName}"

dbUsername=$(ctx target node properties dbUserName)
ctx logger info "${currHostName}:${currFilename} :dbUsername ${dbUsername}"

dbPassword=$(ctx target node properties dbUserPassword)
ctx logger info "${currHostName}:${currFilename} :dbPassword ${dbPassword}"

dbPort=$(ctx target node properties dbPort)
ctx logger info "${currHostName}:${currFilename} :dbPort ${dbPort}"

dbHost=$(ctx target instance host_ip)
ctx logger info "${currHostName}:${currFilename} :dbHost ${dbHost}"

export driverConnectorString="<datasource jndi-name=\"java:jboss/exported/MySqlDS\" pool-name=\"MySqlDS\" enabled=\"true\"><connection-url>jdbc:mysql://${dbHost}:${dbPort}/${databaseName}</connection-url><driver>${jdbcDriverName}</driver><security><user-name>${dbUsername}</user-name><password>${dbPassword}</password></security></datasource>"
ctx logger info "${currHostName}:${currFilename} data source connection string is ${driverConnectorString} ..."
sed -i -e "s+\(.*\)\(</datasource>\)\(.*\)+                \2\n                $driverConnectorString+g" $destStandaloneXmlFile
