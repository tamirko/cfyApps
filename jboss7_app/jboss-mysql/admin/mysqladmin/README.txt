===========================================================================
MySQLADMIN - Administer MySQL DB using a web browser
Copyright (C) 2004  Riccardo Pompeo (Italy)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

===========================================================================

DESCRIPTION
===========
MySQLADMIN is an administration tool for MySQL. 

It requires a J2EE server (eg. Tomcat, Weblogic, ...) and MySQL JDBC driver.

Using MySQLADMIN you can:
- Browse table data
- Insert, update and delete data
- Browse table structure
- Create, drop, modify table

MySQLADMIN can be used to ennance your web site functionality enabling a DB administrator to have access to db data and structure using a simple web browser.

Security is not included. For example use your LDAP to restrict user access.    



PACKAGE CONTENT
===============

README.txt: This file

index.jsp: It is the main page. Display a frame calling mysqladmin.jsp and mysqlstruct.jsp pages

mysqladmin.jsp: It handles browsing of DB tables 

mysqlstruct.jsp: It handles administration of DB tables (create, drop, add columns, create index, ....)

 
SETUP
=====

Create a datasource with name 'mysqldb' linked to a MySQL connection pool.

For example add this lines to weblogic config.xml configuration file:

 <JDBCConnectionPool DriverName="com.mysql.jdbc.Driver" Name="MySQL Connection Pool" Password="" Properties=""
 Targets="myserver" URL="jdbc:mysql://localhost:3306/mysqldb?user=mysqluser&amp;password=mysqlpwd&amp;autoReconnect=true"/>
 <JDBCTxDataSource JNDIName="mysqldb" Name="MySQL ADMIN Data Source" PoolName="MySQL Connection Pool" Targets="myserver"/>

Deploy mysqladmin.war file

Open your web browser at http://localhost:7001/mysqladmin


TEST PLATFORM
=============

WindowsXP x86 
JRockit 8.1 SP2 1.4.1_05
Weblogig 8.1 SP2
MySQL JDBC Connector 2.0.14
MySQL Server 3.23.54


INFO
====
My web page: http://www.sixtyfourbit.org
My e-mail: riccardo.pompeo@sixtyfourbit.org



