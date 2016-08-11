# jboss-mysql-blueprint
A JBoss-MySQL admin sample blueprint for OpenStack and Hybrid (OpenStack and vSphere)

This blueprint enables ypu to deploy, configure, monitor, heal and scale a Drupal 7 on OpenStack and on Hybrid Cloud (OpenStack and vSphere). <br>
Once installed, Cloudify enables you to perform Day-2 operations on your live environments. <br>
E.G :  Apply patches, invoke security updates etc. <br>


# Prerequisites

- An Ubuntu 14.04 image id from your OpenStack account and from your vSphere account <br>
- An flavor image id of your choice from your OpenStack account <br>

# Tested Version

This blueprint has been test with Cloudify version 3.4.0 and with JBoss 7.

# Usage

All you need to do is to set/specify (as an input to the blueprint) the OpenStack image id for Ubuntu 14.04 and the OpenStack flavor Id. <br>
If you use the Hybrid version, you need to set/specify (as an input to the blueprint) the vsphere_template_name for Ubuntu 14.04.


### Step 1: Installation

`cfy install upload -b <choose_blueprint_id> -p <blueprint_filename>` <br>

If you have or want to use an inputs file : <br>
`cfy install upload -b <choose_blueprint_id> -p <blueprint_filename> -i <your_inputs_file>` <br>

This process will create all the cloud resources needed for the application and the application itself ...: <br>

- VMs
- Floating IP's
- Security Groups

and everything else that is needed and declared in the blueprint.<br>

### Step 2: Verify installation

Once the workflow execution is complete, we can view the application endpoint by running: <br>

`cfy deployments outputs -d <deployment_id>`

Hit that URL to see the application running.

### Step 3: Access the application

Browse to http://jboss_floating_ip:jbossPort/mysqladmin/ and start working with the MySQL admin application.


### Step 4: Uninstall

Now lets run the `uninstall` workflow. This will uninstall the application,
as well as delete all related resources. <br>

`cfy uninstall -d <deployment_id>`

