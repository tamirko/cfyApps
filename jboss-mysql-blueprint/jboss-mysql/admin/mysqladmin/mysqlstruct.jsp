<%
///////////////////////////////////////////////////////////////////////////////
// MySQLADMIN - Administer MySQL DB using a web browser
// Copyright (C) 2004  Riccardo Pompeo (Italy)
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
//
%>

<%	
	javax.naming.InitialContext initCtx = new javax.naming.InitialContext();
	javax.sql.DataSource ds = (javax.sql.DataSource) initCtx.lookup("java:jboss/exported/MySqlDS");
	java.sql.Connection db=ds.getConnection();
%>


<html>
<head>
<title>Database administration</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>

<body bgcolor="#FFFFFF" text="#000000">
<SCRIPT>top.frames["leftFrame"].location.href="mysqladmin.jsp"</SCRIPT>

	<% 
		String action=request.getParameter("action");
		String table=request.getParameter("table");
	%>
			
	<%
		if (table!=null && action.equals("struct")) 
		{ 	
				  java.sql.DatabaseMetaData dbmeta=db.getMetaData();
				  java.sql.ResultSet rset=dbmeta.getColumns(null,null,table,null); 
				  java.sql.ResultSet index=dbmeta.getIndexInfo(null,null,table,false,false); 
				  java.sql.ResultSet pkeys=dbmeta.getPrimaryKeys(null,null,table);
				  java.sql.ResultSet forkeys=dbmeta.getExportedKeys(null,null,table);
				  java.sql.ResultSet dbtypes=dbmeta.getTypeInfo();
				  java.util.Hashtable pkHash=new java.util.Hashtable();
				  while(pkeys.next())
				  {
						String column=pkeys.getString("COLUMN_NAME");
						pkHash.put(column,column);
				  }

			%>
			
				<p><font size="+2"><b><%= table %></b></font></p>

				<table width="75%" border="1">
				  <tr bgcolor="#FFFF33"> 
					<td> 
					  <div align="center"><b>Column</b></div>
					</td>
					<td> 
					  <div align="center"><b>Type</b></div>
					</td>
					<td> 
					  <div align="center"><b>Size</b></div>
					</td>
					<td> 
					  <div align="center"><b>Digits</b></div>
					</td>
					<td> 
					  <div align="center"><b>Is nullable</b></div>
					</td>
					<td> 
					  <div align="center"><b>Primary key</b></div>
					</td>
					<td> 
					  <div align="center"><b>Command</b></div>
					</td>
				  </tr>
				  <% while(rset.next()) { %>
				  <tr> 
					<td><%= rset.getString("COLUMN_NAME") %></td>
					<td><%= rset.getString("TYPE_NAME") %></td>
					<td><%= rset.getString("COLUMN_SIZE") %></td>
					<td><%= rset.getString("DECIMAL_DIGITS") %></td>
					<td><%= rset.getString("IS_NULLABLE") %></td>
					<td><%= (pkHash.containsKey(rset.getString("COLUMN_NAME"))) ? "YES" : "NO" %></td>
					
    <td><a href="mysqlstruct.jsp?action=dropcolumn&table=<%= table %>&column=<%= rset.getString("COLUMN_NAME") %>">Drop</a></td>
				  </tr>
				  <% }  %>
				</table>	

				<p>&nbsp;</p>

				
<form name="addcol" method="post" action="mysqlstruct.jsp">
  <input type="hidden" name="action" value="addcolumn">
				  <input type="hidden" name="table" value="<%= table %>">
				  <table width="75%" border="1">
					  <tr bgcolor="#FFFF33"> 
						<td> 
						  <div align="center"><b>Name</b></div>
						</td>
						<td> 
						  <div align="center"><b>Type</b></div>
						</td>
						<td> 
						  <div align="center"><b>Size (M)</b></div>
						</td>
						<td> 
        				  <div align="center"><b>Digits (D)</b></div>
						</td>
						<td> 
						  <div align="center"><b>NOT NULL</b></div>
						</td>
						<td> 
						  <div align="center"><b>Default</b></div>
						</td>
					  </tr>
					  <tr> 
						<td><input type="text" name="name"></td>
						<td>							
							<select name="type">
							  <% 
							  	 dbtypes.beforeFirst();
							  	 while(dbtypes.next()) 
								 { 
								 	String type=dbtypes.getString("TYPE_NAME");
								 	String par=dbtypes.getString("CREATE_PARAMS");							 
							  %>
							  
							  		<option value="<%= type %>"><%= type %><%= par %></option>
							  <% } %>
							</select>
						</td>
						<td><input type="text" name="size" value="10"></td>
						<td><input type="text" name="digits" value="0"></td>
						<td>
							<select name="notnull">
							  <option value="NULL">NO</option>
							  <option value="NOT NULL">YES</option>
							</select>
						</td>
						<td><input type="text" name="default"></td>
					  </tr>
					</table>
				  <p>
					<input type="submit" name="Submit" value="Add column">
				  </p>
				</form>

				<p>&nbsp;</p>
				
				<table width="40%" border="1">
				  <tr bgcolor="#FFFF33"> 
					<td><div align="center"><b>Index name</b></div></td>
					<td><div align="center"><b>Non unique</b></div></td>
					<td><div align="center"><b>Column</b></div></td>
					<td><div align="center"><b>Command</b></div></td>
				  </tr>
				  <% while(index.next()) { %>
				  <tr> 
					<td><%= index.getString("INDEX_NAME") %></td>
					<td><%= index.getString("NON_UNIQUE") %></td>
					<td><%= index.getString("COLUMN_NAME") %></td>
					
    <td><a href="mysqlstruct.jsp?action=dropindex&table=<%= table %>&index=<%= index.getString("INDEX_NAME") %>">Drop</a></td>
				  </tr>
				  <% }  %>
				</table>
				
				
<p><a href="mysqlstruct.jsp?action=createindex&table=<%= table %>">Create 
  index...</a></p>
				<p>&nbsp;</p>

				<table width="50%" border="1">
				  <tr bgcolor="#FFFF33"> 
					<td><div align="center"><b>PK key name</b></div></td>
					<td><div align="center"><b>PK table name</b></div></td>
					<td><div align="center"><b>PK column</b></div></td>
					<td><div align="center"><b>FK key name</b></div></td>
					<td><div align="center"><b>FK table name</b></div></td>
					<td><div align="center"><b>FK column</b></div></td>
				  </tr>
				  <% while(index.next()) { %>
				  <tr> 
					<td><%= index.getString("PK_NAME") %></td>
					<td><%= index.getString("PKTABLE_NAME") %></td>
					<td><%= index.getString("PKCOLUMN_NAME") %></td>
					<td><%= index.getString("FK_NAME") %></td>
					<td><%= index.getString("FKTABLE_NAME") %></td>
					<td><%= index.getString("FKCOLUMN_NAME") %></td>
				  </tr>
				  <% }  %>
				</table>

				
<p><a href="mysqlstruct.jsp?action=createconstraint&table=<%= table %>">Create 
  constraint...</a></p>
	
		<% } else if (action.equals("showall")) { 

				java.sql.ResultSet typerset=db.getMetaData().getTypeInfo();
				java.util.Hashtable sqltypes=new java.util.Hashtable();
				while(typerset.next())
				{
					String literal=typerset.getString("LITERAL_PREFIX");
					sqltypes.put(typerset.getString("TYPE_NAME").toLowerCase(),(literal==null)? "" : literal);
				}

				java.sql.DatabaseMetaData dbmeta=db.getMetaData();
				java.sql.ResultSet tlist=dbmeta.getTables(null,null,null,null); 
				while(tlist.next())
				{
					java.sql.ResultSet rset=db.createStatement().executeQuery("SHOW CREATE TABLE " + tlist.getString("TABLE_NAME"));
					rset.next();
					%>
					
						<p>DROP TABLE <%= tlist.getString("TABLE_NAME") %></p>
						<p><%= rset.getString("create table") %></p>
					
					<%

					rset=db.createStatement().executeQuery("SELECT * FROM " + tlist.getString("TABLE_NAME"));
				    java.sql.ResultSetMetaData meta=rset.getMetaData();
				    int columnCount=meta.getColumnCount();
				    while(rset.next()) 
					{
						StringBuffer stmt=new StringBuffer().append("INSERT INTO ").append(tlist.getString("TABLE_NAME")).append(" (");			  
					    StringBuffer values=new StringBuffer().append(") VALUES (");
						for(int cnt=1; cnt <= columnCount; cnt++) 
						{
							if(cnt!=1)
							{
								stmt.append(",");
								values.append(",");
							}
							 
							stmt.append(meta.getColumnName(cnt));
							Object obj=rset.getObject(cnt);
							String type=meta.getColumnTypeName(cnt).toLowerCase();
							if(rset.wasNull())
							{
								values.append("NULL");
							}
							else
							{
								String value=obj.toString();							
								values.append(sqltypes.get(type)).append(value).append(sqltypes.get(type));
							}
						}
						
						stmt.append(values.toString()).append(")");
						%>
						
						<p><%= stmt.toString() %></p>
						
						<%					
					}
					%>
					<p>COMMIT</p>
					<%
				}
		%>

		<% } else if (action.equals("createassociation")) { 

				java.sql.DatabaseMetaData dbmeta=db.getMetaData();
				java.sql.ResultSet tlist=dbmeta.getTables(null,null,null,null); 
				java.sql.ResultSet dbtypes=dbmeta.getTypeInfo();

		%>
				
<form name="formconstr" method="post" action="mysqlstruct.jsp">
  <input type="hidden" name="action" value="createassociation1">
				   <p>Table name: 
					<input type="text" name="table">
				   </p>
				   <p>A table:
						<select name="Atable">
							<% while(tlist.next()) { %>
							  <option value="<%= tlist.getString("TABLE_NAME") %>"><%= tlist.getString("TABLE_NAME") %></option>
							<% }  %>
						</select>
				  </p>
				   <p>B table:
						<select name="Btable">
							  <option value="" selected>-</option>
							<% tlist.beforeFirst(); %>
							<% while(tlist.next()) { %>
							  <option value="<%= tlist.getString("TABLE_NAME") %>"><%= tlist.getString("TABLE_NAME") %></option>
							<% }  %>
						</select>
				  </p>
				  
				  <p>&nbsp; </p>
				  <table width="75%" border="1">
					  <tr bgcolor="#FFFF33"> 
						<td> 
						  <div align="center"><b>Name</b></div>
						</td>
						<td> 
						  <div align="center"><b>Type</b></div>
						</td>
						<td> 
						  <div align="center"><b>Size (M)</b></div>
						</td>
						<td> 
        				  <div align="center"><b>Digits (D)</b></div>
						</td>
						<td> 
						  <div align="center"><b>NOT NULL</b></div>
						</td>
						<td> 
						  <div align="center"><b>Default</b></div>
						</td>
						<td> 
						  <div align="center"><b>Primary key</b></div>
						</td>
					  </tr>
					  
					  <% for(int cnt=1; cnt <= 10; cnt++) { String colnum="col" + String.valueOf(cnt); %>
						  <tr> 
							<td><input type="text" name="<%= colnum %>_name"></td>
							<td>							
								<select name="<%= colnum %>_type">
								  <% 
									 dbtypes.beforeFirst();
									 while(dbtypes.next()) 
									 { 
										String type=dbtypes.getString("TYPE_NAME");
										String par=dbtypes.getString("CREATE_PARAMS");							 
								  %>
								  
										<option value="<%= type %>"><%= type %><%= par %></option>
								  <% } %>
								</select>
							</td>
							<td><input type="text" name="<%= colnum %>_size" value="10"></td>
							<td><input type="text" name="<%= colnum %>_digits" value="0"></td>
							<td>
								<select name="<%= colnum %>_notnull">
									<% if(cnt == 1) { %>
										  <option value="NOT NULL">YES</option>
										  <option value="NULL">NO</option>
									<% } else { %>
										  <option value="NULL">NO</option>
										  <option value="NOT NULL">YES</option>
									<% } %>
								</select>
							</td>
							<td><input type="text" name="<%= colnum %>_default"></td>
							<td>
								<select name="<%= colnum %>_primkey">
									<% if(cnt == 1) { %>
										  <option value="PRIMARY KEY">YES</option>
										  <option value="">NO</option>
									<% } else { %>
										  <option value="">NO</option>
										  <option value="PRIMARY KEY">YES</option>
									<% } %>
								</select>
							</td>
						  </tr>
						<% } %>
					</table>
				  
				  <p>
					<input type="submit" name="Submit" value="Create association">
				  </p>
				</form>

		<% } else if (action.equals("createassociation1")) {
	
				java.sql.ResultSet typerset=db.getMetaData().getTypeInfo();
				java.util.Hashtable literal=new java.util.Hashtable();
				java.util.Hashtable params=new java.util.Hashtable();
				while(typerset.next())
				{
					String value=typerset.getString("LITERAL_PREFIX");
					literal.put(typerset.getString("TYPE_NAME"),(literal==null)? "" : value);
					value=typerset.getString("CREATE_PARAMS");
					params.put(typerset.getString("TYPE_NAME"),(literal==null)? "" : value);
				}

				java.sql.DatabaseMetaData dbmeta=db.getMetaData();
				String Atable=request.getParameter("Atable");
				String Btable=request.getParameter("Btable");
				if(Btable!=null && Btable.equals(""))
					Btable=null;

				if(table==null || table.equals("") || Atable==null || (Btable!=null && Atable.equals(Btable)))
				{
					response.sendRedirect("mysqlstruct.jsp?action=createassociation");
					return;
				}

				java.sql.ResultSet Acolumns=dbmeta.getColumns(null,null,Atable,null); 				  
		        java.sql.ResultSet Apkeys=dbmeta.getPrimaryKeys(null,null,Atable);
				java.sql.ResultSet Bcolumns=null; 				  
		        java.sql.ResultSet Bpkeys=null;
				if(Btable!=null)
				{
					Bcolumns=dbmeta.getColumns(null,null,Btable,null); 				  
					Bpkeys=dbmeta.getPrimaryKeys(null,null,Btable);
				}
				
				StringBuffer stmt=new StringBuffer().append("CREATE TABLE ").append(table).append(" (");
				StringBuffer pkdecl=new StringBuffer().append(",PRIMARY KEY (");
				boolean pkexist=false;

				while(Apkeys.next())
				{
					String name=Apkeys.getString("COLUMN_NAME");
				
					Acolumns.beforeFirst();
					while(Acolumns.next())
					{
						if(Acolumns.getString("COLUMN_NAME").equals(name))
						{
							String type=Acolumns.getString("TYPE_NAME").toUpperCase();
							String size=Acolumns.getString("COLUMN_SIZE");
							String digits=Acolumns.getString("DECIMAL_DIGITS");

							if(pkexist)
								stmt.append(",");

							stmt.append(name).append(" ").append(type);
	
							String par=(String)params.get(type); 
							if(par!=null && (par.startsWith("(M)") || par.startsWith("[(M)]") ))						
								stmt.append("(").append(size).append(")");
							else if(par!=null && (par.startsWith("(M,D)") || par.startsWith("[(M,D)]") || par.startsWith("[(M,[D])]") ))						
								stmt.append("(").append(size).append(",").append(digits).append(")");

							stmt.append(" ").append("NOT NULL");
	
							if(!pkexist)
								pkdecl.append(name);
							else
								pkdecl.append(",").append(name);
						
							pkexist=true;
						}
					}
				}

				if(!pkexist)
				{
					response.sendRedirect("mysqlstruct.jsp?action=createassociation");
					return;
				}
				
				if(Btable!=null)
				{
					pkexist=false;
					while(Bpkeys.next())
					{
						String name=Bpkeys.getString("COLUMN_NAME");
					
						Bcolumns.beforeFirst();
						while(Bcolumns.next())
						{
							if(Bcolumns.getString("COLUMN_NAME").equals(name))
							{
								String type=Bcolumns.getString("TYPE_NAME").toUpperCase();
								String size=Bcolumns.getString("COLUMN_SIZE");
								String digits=Bcolumns.getString("DECIMAL_DIGITS");
	
								stmt.append(",").append(name).append(" ").append(type);
		
								String par=(String)params.get(type); 
								if(par!=null && (par.startsWith("(M)") || par.startsWith("[(M)]") ))						
									stmt.append("(").append(size).append(")");
								else if(par!=null && (par.startsWith("(M,D)") || par.startsWith("[(M,D)]") || par.startsWith("[(M,[D])]") ))						
									stmt.append("(").append(size).append(",").append(digits).append(")");

								stmt.append(" ").append("NOT NULL");
		
								if(!pkexist)
									pkexist=true;
	
								pkdecl.append(",").append(name);
							}
						}
					}
	
					if(!pkexist)
					{
						response.sendRedirect("mysqlstruct.jsp?action=createassociation");
						return;
					}
				}

				for(int cnt=1; cnt<=10; cnt++)
				{
					String colnum="col" + String.valueOf(cnt);
					String name=request.getParameter(colnum + "_name");
					String type=request.getParameter(colnum + "_type");
					String size=request.getParameter(colnum + "_size");
					String digits=request.getParameter(colnum + "_digits");
					String notnull=request.getParameter(colnum + "_notnull");
					String defval=request.getParameter(colnum + "_default");
					String primkey=request.getParameter(colnum + "_primkey");
					
					if(name!=null && !name.equals(""))
					{
						stmt.append(",").append(name).append(" ").append(type);

						String par=(String)params.get(type); 
						if(par!=null && (par.startsWith("(M)") || par.startsWith("[(M)]") ))						
							stmt.append("(").append(size).append(")");
						else if(par!=null && (par.startsWith("(M,D)") || par.startsWith("[(M,D)]") || par.startsWith("[(M,[D])]") ))						
							stmt.append("(").append(size).append(",").append(digits).append(")");

						if(notnull.equals("NOT NULL"))
							stmt.append(" ").append(notnull);

						if(defval!=null && !defval.equals(""))
								stmt.append(" DEFAULT ").append(literal.get(type)).append(defval).append(literal.get(type));

						if(primkey!=null && primkey.equals("PRIMARY KEY"))
						{
							if(!pkexist)
							{
								pkexist=true;
								pkdecl.append(name);
							}
							else
								pkdecl.append(",").append(name);
						}
					}
					else
						break;
				}	

				stmt.append(pkdecl.toString()).append(")").append(")");
			    try
				{
					db.createStatement().executeUpdate(stmt.toString());
				}
				catch(Exception exc)
				{ %>
					<p>SQL statement : <%= stmt.toString() %></p>
					<p>Exception : <%= exc.getMessage() %></p>
				  <%
					return;
				}
			%>
			
			<%		
				response.sendRedirect("mysqlstruct.jsp?action=struct&table="+table);
			%>
	
			
		<% } else if (action.equals("createconstraint")) { 
		
				  java.sql.DatabaseMetaData dbmeta=db.getMetaData();
				  java.sql.ResultSet rset=dbmeta.getColumns(null,null,table,null); 				  
				  java.sql.ResultSet tlist=dbmeta.getTables(null,null,null,null); 
		%>
				<p><font size="+2"><b><%= table %></b></font></p>
				
<form name="formconstr" method="post" action="mysqlstruct.jsp">
  <input type="hidden" name="action" value="createconstraint1">
				  <input type="hidden" name="table" value="<%= table %>">
				  <p>Constraint name: <input type="text" name="constraint"></p>
					<table width="50%" border="1">
					  <tr bgcolor="#FFFF33"> 
						<td> 
						  <div align="center"><b>Column</b></div>
						</td>
						<td> 
						  <div align="center"><b>Type</b></div>
						</td>
						<td> 
						  <div align="center"><b>Index</b></div>
						</td>
					  </tr>
					  <% while(rset.next()) { %>
					  <tr> 
						<td><%= rset.getString("COLUMN_NAME") %></td>
						<td><%= rset.getString("TYPE_NAME") %></td>
						<td>
        					<input type="checkbox" name="<%= table + "_" + rset.getString("COLUMN_NAME") %>" value="true">
      					</td>
					  </tr>
					  <% }  %>
					</table>					
				  <p>&nbsp;</p>
				   <p>FK table:
						<select name="fktable">
							<% while(tlist.next()) { %>
							  <option value="<%= tlist.getString("TABLE_NAME") %>"><%= tlist.getString("TABLE_NAME") %></option>
							<% }  %>
						</select>
					</p>
				  <p>
					<input type="submit" name="Submit" value="Create constraint">
				  </p>
				</form>

		<% } else if (action.equals("createconstraint1")) { 
		
				  String constraint=request.getParameter("constraint");
				  String fktable=request.getParameter("fktable");
				  java.sql.DatabaseMetaData dbmeta=db.getMetaData();
				  java.sql.ResultSet rset=dbmeta.getColumns(null,null,table,null); 				  
				  java.sql.ResultSet fkrset=dbmeta.getColumns(null,null,fktable,null); 				  
		%>
		
				<p><font size="+2"><b><%= table %></b></font></p>
				
<form name="formconstr1" method="post" action="mysqlstruct.jsp">
  <input type="hidden" name="action" value="createconstraint2">
				  <input type="hidden" name="table" value="<%= table %>">
				  <input type="hidden" name="fktable" value="<%= fktable %>">
				  <input type="hidden" name="constraint" value="<%= constraint %>">

					<p>Constraint: <b><%= constraint %></b></p>
				  
					<table width="50%" border="1">
					  <tr bgcolor="#FFFF33"> 
						<td> 
						  <div align="center"><b>Column</b></div>
						</td>
						<td> 
						  <div align="center"><b>Type</b></div>
						</td>
					  </tr>
					  <% while(rset.next()) { 
					  
					  	 String colname=table + "_" + rset.getString("COLUMN_NAME");
						 String value=request.getParameter(colname);
						 if(value!=null && value.equals("true")) {
					  %>
							  <tr> 
								<td><%= rset.getString("COLUMN_NAME") %></td>
								<td><%= rset.getString("TYPE_NAME") %></td>
								<input type="hidden" name="<%= colname %>" value="true">
							  </tr>
					  <% }}  %>
					</table>					
				  
					<p>FK table: <b><%= fktable %></b></p>
				  
					<table width="50%" border="1">
					  <tr bgcolor="#FFFF33"> 
						<td> 
						  <div align="center"><b>Column</b></div>
						</td>
						<td> 
						  <div align="center"><b>Type</b></div>
						</td>
						<td> 
						  <div align="center"><b>Index</b></div>
						</td>
					  </tr>
					  <% while(fkrset.next()) { %>
					  <tr> 
						<td><%= fkrset.getString("COLUMN_NAME") %></td>
						<td><%= fkrset.getString("TYPE_NAME") %></td>
						<td>
        					<input type="checkbox" name="<%= fktable + "_" + fkrset.getString("COLUMN_NAME") %>" value="true">
      					</td>
					  </tr>
					  <% }  %>
					</table>					
				  <p>&nbsp;</p>
				  <p>
					<input type="submit" name="Submit" value="Create constraint">
				  </p>
				</form>

		<% } else if (action.equals("createconstraint2")) {
		
				String constraint=request.getParameter("constraint");
				String fktable=request.getParameter("fktable");
				java.sql.DatabaseMetaData dbmeta=db.getMetaData();
				java.sql.ResultSet rset=dbmeta.getColumns(null,null,table,null); 				  
				java.sql.ResultSet fkrset=dbmeta.getColumns(null,null,fktable,null); 				  

				StringBuffer stmt=new StringBuffer().append("ALTER TABLE ").append(table);
				stmt.append(" ADD CONSTRAINT ").append(constraint);
				stmt.append(" FOREIGN KEY ").append(constraint + "_fk").append(" (");
				
				boolean isfirst=true;
			    while(rset.next()) 
				{
					String column=rset.getString("COLUMN_NAME");
					String parameter=table + "_" + column;
					String value=request.getParameter(parameter);
					
					if(value!=null && value.equals("true"))
					{
						if(isfirst)
							isfirst=false;
						else
							stmt.append(",");
							
						stmt.append(column);
					}
				}		
		
				stmt.append(") REFERENCES ").append(fktable).append(" (");

				isfirst=true;
			    while(fkrset.next()) 
				{ 
					String column=fkrset.getString("COLUMN_NAME");
					String parameter=fktable + "_" + column;
					String value=request.getParameter(parameter);
					
					if(value!=null && value.equals("true"))
					{
						if(isfirst)
							isfirst=false;
						else
							stmt.append(",");
							
						stmt.append(column);
					}
				}		
		
				stmt.append(") ON DELETE CASCADE");

				try
				{
					db.createStatement().executeUpdate(stmt.toString());
				}
				catch(Exception exc)
				{ %>
					<p>SQL statement : <%= stmt.toString() %></p>
					<p>Exception : <%= exc.getMessage() %></p>
<%
					return;
				}
					
				response.sendRedirect("mysqlstruct.jsp?action=struct&table="+table);
		%>

		<% } else if (action.equals("createindex")) { 
		
				  java.sql.DatabaseMetaData dbmeta=db.getMetaData();
				  java.sql.ResultSet rset=dbmeta.getColumns(null,null,table,null); 
		%>
		
				<p><font size="+2"><b><%= table %></b></font></p>
				
<form name="form2" method="post" action="mysqlstruct.jsp">
  <input type="hidden" name="action" value="createindex1">
				  <input type="hidden" name="table" value="<%= table %>">
				  <p>Index name: <input type="text" name="indexname"></p>
				   <p>Index type:
						<select name="type">
						  <option value="INDEX">INDEX</option>
						  <option value="UNIQUE">UNIQUE</option>
						  <option value="PRIMARY KEY">PRIMARY KEY</option>
						</select>
					</p>
					<table width="50%" border="1">
					  <tr bgcolor="#FFFF33"> 
						<td> 
						  <div align="center"><b>Column</b></div>
						</td>
						<td> 
						  <div align="center"><b>Type</b></div>
						</td>
						<td> 
						  <div align="center"><b>Index</b></div>
						</td>
					  </tr>
					  <% while(rset.next()) { %>
					  <tr> 
						<td><%= rset.getString("COLUMN_NAME") %></td>
						<td><%= rset.getString("TYPE_NAME") %></td>
						<td>
        					<input type="checkbox" name="<%= rset.getString("COLUMN_NAME") %>" value="true">
      					</td>
					  </tr>
					  <% }  %>
					</table>					
				  <p>&nbsp;</p>
				  <p>
					<input type="submit" name="Submit" value="Create index">
				  </p>
				</form>

		<% } else if (action.equals("createindex1")) {
		
				java.sql.DatabaseMetaData dbmeta=db.getMetaData();
				java.sql.ResultSet rset=dbmeta.getColumns(null,null,table,null); 
				String indexname=request.getParameter("indexname");
				String type=request.getParameter("type");
				StringBuffer stmt=new StringBuffer().append("ALTER TABLE ").append(table);
				
				if(type!=null && type.equals("PRIMARY KEY"))
					stmt.append(" ADD PRIMARY KEY (");
				else if(type!=null && type.equals("UNIQUE"))	
					stmt.append(" ADD UNIQUE ").append(indexname).append(" (");
				else
					stmt.append(" ADD INDEX ").append(indexname).append(" (");				
				
				boolean isfirst=true;
			    while(rset.next()) 
				{ 
					String column=rset.getString("COLUMN_NAME");
					String value=request.getParameter(column);
					
					if(value!=null && value.equals("true"))
					{
						if(isfirst)
							isfirst=false;
						else
							stmt.append(",");
							
						stmt.append(column);
					}
				}		
		
				stmt.append(")");

				try
				{
					db.createStatement().executeUpdate(stmt.toString());
				}
				catch(Exception exc)
				{ %>
					<p>SQL statement : <%= stmt.toString() %></p>
					<p>Exception : <%= exc.getMessage() %></p>
<%
					return;
				}
					
				response.sendRedirect("mysqlstruct.jsp?action=struct&table="+table);
		%>
		
		<% } else if (action.equals("create")) { 
				
				java.sql.DatabaseMetaData dbmeta=db.getMetaData();
				java.sql.ResultSet dbtypes=dbmeta.getTypeInfo();
		%>
				
				
<form name="create" method="post" action="mysqlstruct.jsp">
  <input type="hidden" name="action" value="create1">
					
				  <p>Table name: 
					<input type="text" name="table">
				  </p>
				  <p>&nbsp; </p>
				  <table width="75%" border="1">
					  <tr bgcolor="#FFFF33"> 
						<td> 
						  <div align="center"><b>Name</b></div>
						</td>
						<td> 
						  <div align="center"><b>Type</b></div>
						</td>
						<td> 
						  <div align="center"><b>Size (M)</b></div>
						</td>
						<td> 
        				  <div align="center"><b>Digits (D)</b></div>
						</td>
						<td> 
						  <div align="center"><b>NOT NULL</b></div>
						</td>
						<td> 
						  <div align="center"><b>Default</b></div>
						</td>
						<td> 
						  <div align="center"><b>Primary key</b></div>
						</td>
					  </tr>
					  
					  <% for(int cnt=1; cnt <= 20; cnt++) { String colnum="col" + String.valueOf(cnt); %>
						  <tr> 
							<td><input type="text" name="<%= colnum %>_name"></td>
							<td>							
								<select name="<%= colnum %>_type">
								  <% 
									 dbtypes.beforeFirst();
									 while(dbtypes.next()) 
									 { 
										String type=dbtypes.getString("TYPE_NAME");
										String par=dbtypes.getString("CREATE_PARAMS");							 
								  %>
								  
										<option value="<%= type %>"><%= type %><%= par %></option>
								  <% } %>
								</select>
							</td>
							<td><input type="text" name="<%= colnum %>_size" value="10"></td>
							<td><input type="text" name="<%= colnum %>_digits" value="0"></td>
							<td>
								<select name="<%= colnum %>_notnull">
									<% if(cnt == 1) { %>
										  <option value="NOT NULL">YES</option>
										  <option value="NULL">NO</option>
									<% } else { %>
										  <option value="NULL">NO</option>
										  <option value="NOT NULL">YES</option>
									<% } %>
								</select>
							</td>
							<td><input type="text" name="<%= colnum %>_default"></td>
							<td>
								<select name="<%= colnum %>_primkey">
									<% if(cnt == 1) { %>
										  <option value="PRIMARY KEY">YES</option>
										  <option value="">NO</option>
									<% } else { %>
										  <option value="">NO</option>
										  <option value="PRIMARY KEY">YES</option>
									<% } %>
								</select>
							</td>
						  </tr>
						<% } %>
					</table>
				
				  
				  <p>&nbsp;</p>
				  <p>
					<input type="submit" name="Submit" value="Create table">
				  </p>
				</form>
										 	
		
		<% } else if (action.equals("create1")) {
	
				java.sql.ResultSet typerset=db.getMetaData().getTypeInfo();
				java.util.Hashtable literal=new java.util.Hashtable();
				java.util.Hashtable params=new java.util.Hashtable();
				while(typerset.next())
				{
					String value=typerset.getString("LITERAL_PREFIX");
					literal.put(typerset.getString("TYPE_NAME"),(literal==null)? "" : value);
					value=typerset.getString("CREATE_PARAMS");
					params.put(typerset.getString("TYPE_NAME"),(literal==null)? "" : value);
				}

				if(table==null || table.equals(""))
				{
					response.sendRedirect("mysqlstruct.jsp?action=create");
					return;
				}

				StringBuffer stmt=new StringBuffer().append("CREATE TABLE ").append(table).append(" (");
				StringBuffer pkdecl=new StringBuffer().append(",PRIMARY KEY (");
				boolean pkexist=false;
				
				for(int cnt=1; cnt<=20; cnt++)
				{
					String colnum="col" + String.valueOf(cnt);
					String name=request.getParameter(colnum + "_name");
					String type=request.getParameter(colnum + "_type");
					String size=request.getParameter(colnum + "_size");
					String digits=request.getParameter(colnum + "_digits");
					String notnull=request.getParameter(colnum + "_notnull");
					String defval=request.getParameter(colnum + "_default");
					String primkey=request.getParameter(colnum + "_primkey");
					
					if(name!=null && !name.equals(""))
					{
						if(cnt>1)
							stmt.append(",");

						stmt.append(name).append(" ").append(type);

						String par=(String)params.get(type); 
						if(par!=null && (par.startsWith("(M)") || par.startsWith("[(M)]") ))						
							stmt.append("(").append(size).append(")");
						else if(par!=null && (par.startsWith("(M,D)") || par.startsWith("[(M,D)]") || par.startsWith("[(M,[D])]") ))						
							stmt.append("(").append(size).append(",").append(digits).append(")");

						if(notnull.equals("NOT NULL"))
							stmt.append(" ").append(notnull);

						if(defval!=null && !defval.equals(""))
								stmt.append(" DEFAULT ").append(literal.get(type)).append(defval).append(literal.get(type));

						if(primkey!=null && primkey.equals("PRIMARY KEY"))
						{
							if(!pkexist)
							{
								pkexist=true;
								pkdecl.append(name);
							}
							else
								pkdecl.append(",").append(name);
						}
					}
					else if((name==null || name.equals("")) && cnt==1)
					{
						response.sendRedirect("mysqlstruct.jsp?action=create");
						return;
					}
					else
						break;
				}	

				if(pkexist)
					stmt.append(pkdecl.toString()).append(")");

				stmt.append(")");

				try
				{
					db.createStatement().executeUpdate(stmt.toString());
				}
				catch(Exception exc)
				{ %>
					<p>SQL statement : <%= stmt.toString() %></p>
					<p>Exception : <%= exc.getMessage() %></p>
<%
					return;
				}
					
				response.sendRedirect("mysqlstruct.jsp?action=struct&table="+table);
			%>
		<% } else if (action.equals("addcolumn")) {
	
				java.sql.ResultSet typerset=db.getMetaData().getTypeInfo();
				java.util.Hashtable literal=new java.util.Hashtable();
				java.util.Hashtable params=new java.util.Hashtable();
				while(typerset.next())
				{
					String value=typerset.getString("LITERAL_PREFIX");
					literal.put(typerset.getString("TYPE_NAME"),(literal==null)? "" : value);
					value=typerset.getString("CREATE_PARAMS");
					params.put(typerset.getString("TYPE_NAME"),(literal==null)? "" : value);
				}

				StringBuffer stmt=new StringBuffer().append("ALTER TABLE ").append(table).append(" ADD COLUMN ");
				String name=request.getParameter("name");
				String type=request.getParameter("type");
				String size=request.getParameter("size");
				String digits=request.getParameter("digits");
				String notnull=request.getParameter("notnull");
				String defval=request.getParameter("default");
					
				if(name==null || name.equals(""))
				{
					response.sendRedirect("mysqlstruct.jsp?action=struct&table="+table);
					return;
				}
				
				stmt.append(name).append(" ").append(type);

				String par=(String)params.get(type); 
				if(par!=null && (par.startsWith("(M)") || par.startsWith("[(M)]") ))						
					stmt.append("(").append(size).append(")");
				else if(par!=null && (par.startsWith("(M,D)") || par.startsWith("[(M,D)]") || par.startsWith("[(M,[D])]") ))						
					stmt.append("(").append(size).append(",").append(digits).append(")");

				if(notnull.equals("NOT NULL"))
					stmt.append(" ").append(notnull);

				if(defval!=null && !defval.equals(""))
						stmt.append(" DEFAULT ").append(literal.get(type)).append(defval).append(literal.get(type));
								
				try
				{
					db.createStatement().executeUpdate(stmt.toString());
				}
				catch(Exception exc)
				{ %>
					<p>SQL statement : <%= stmt.toString() %></p>
					<p>Exception : <%= exc.getMessage() %></p>
<%
					return;
				}
					
				response.sendRedirect("mysqlstruct.jsp?action=struct&table="+table);
			%>

		<% } else if (action.equals("drop")) { %>

			Confirm deletion of table <b><%= table %></b> 
			
<form name="form1" method="post" action="mysqlstruct.jsp">
  <input type="hidden" name="action" value="drop1">
				<input type="hidden" name="table" value="<%= table %>">
				<input type="submit" name="Submit" value="YES">
			</form>

		<% } else if (action.equals("drop1")) {
	
				StringBuffer stmt=new StringBuffer().append("DROP TABLE ").append(table);

				try
				{
					db.createStatement().executeUpdate(stmt.toString());
				}
				catch(Exception exc)
				{ %>
					<p>SQL statement : <%= stmt.toString() %></p>
					<p>Exception : <%= exc.getMessage() %></p>
				  <%
					return;
				}
					
			%>

			<p>Table <%= table %> deleted</p>

		<% } else if (action.equals("dropindex")) { %>

			Confirm deletion of index <b><%= request.getParameter("index") %></b> from table <b><%= table %></b> 
			
<form name="form1" method="post" action="mysqlstruct.jsp">
  <input type="hidden" name="action" value="dropindex1">
				<input type="hidden" name="table" value="<%= table %>">
				<input type="hidden" name="index" value="<%= request.getParameter("index") %>">
				<input type="submit" name="Submit" value="YES">
			</form>

		<% } else if (action.equals("dropindex1")) {
	
				StringBuffer stmt=new StringBuffer().append("ALTER TABLE ").append(table);
				String index=request.getParameter("index");
				
				if(index.equals("PRIMARY"))
					stmt.append(" DROP PRIMARY KEY ");
			    else
					stmt.append(" DROP INDEX ").append(index);

				try
				{
					db.createStatement().executeUpdate(stmt.toString());
				}
				catch(Exception exc)
				{ %>
					<p>SQL statement : <%= stmt.toString() %></p>
					<p>Exception : <%= exc.getMessage() %></p>
				  <%
					return;
				}
					
				response.sendRedirect("mysqlstruct.jsp?action=struct&table="+table);
			%>

		<% } else if (action.equals("dropcolumn")) { %>

			Confirm deletion of column <b><%= request.getParameter("column") %></b> from table <b><%= table %></b> 
			
<form name="form1" method="post" action="mysqlstruct.jsp">
  <input type="hidden" name="action" value="dropcolumn1">
				<input type="hidden" name="table" value="<%= table %>">
				<input type="hidden" name="column" value="<%= request.getParameter("column") %>">
				<input type="submit" name="Submit" value="YES">
			</form>

		<% } else if (action.equals("dropcolumn1")) {
	
				StringBuffer stmt=new StringBuffer().append("ALTER TABLE ").append(table);
				stmt.append(" DROP COLUMN ").append(request.getParameter("column"));

				try
				{
					db.createStatement().executeUpdate(stmt.toString());
				}
				catch(Exception exc)
				{ %>
					<p>SQL statement : <%= stmt.toString() %></p>
					<p>Exception : <%= exc.getMessage() %></p>
				  <%
					return;
				}
					
				response.sendRedirect("mysqlstruct.jsp?action=struct&table="+table);
			%>
		<% } %>

</body>
</html>

<%
	db.close();
%>
