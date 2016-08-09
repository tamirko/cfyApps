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

	<% 
		String action=request.getParameter("action");
		String table=request.getParameter("table");
		String orderby=request.getParameter("orderby");
		String record=request.getParameter("record");
		String offset=request.getParameter("offset");
		
		if (action==null) 
		{ 	
	%>
			<%
				  java.sql.DatabaseMetaData dbmeta=db.getMetaData();
				  java.sql.ResultSet rset=dbmeta.getTables(null,null,null,null); 
			%>
				
				  <table width="30%" border="1">
				  <tr>
					<td bgcolor="#FFFF00"><div align="center"><b>Name</b></div></td>
					<td bgcolor="#FFFF00"><div align="center"><b>Type</b></div></td>
					<td bgcolor="#FFFF00"><div align="center"><b>Command</b></div></td>
				  </tr>

				  <% while(rset.next()) { %>			  
					  <tr> 
							
    <td><a href="mysqladmin.jsp?action=query&table=<%= rset.getString("TABLE_NAME") %>" target="mainFrame"><%= rset.getString("TABLE_NAME") %></a></td>
							
    <td><a href="mysqlstruct.jsp?action=struct&table=<%= rset.getString("TABLE_NAME") %>" target="mainFrame"><%= rset.getString("TABLE_TYPE") %></a></td>
							
    <td> <a href="mysqlstruct.jsp?action=drop&table=<%= rset.getString("TABLE_NAME") %>" target="mainFrame">Drop</a> 
    </td>
					  </tr>
				  <% }  %>

				  </table>

				  
<p><a href="mysqlstruct.jsp?action=create" target="mainFrame">Create new table...</a></p>
				  
<p><a href="mysqlstruct.jsp?action=createassociation" target="mainFrame">Create 
  new association...</a></p>
				  
<p><a href="mysqlstruct.jsp?action=showall" target="mainFrame">Show all SQL CREATE...</a></p>

	<% 		
		}
		else if (table!=null && action.equals("query")) 
		{ 	
	%>
			<p><font size="+2"><b><%= table %></b></font></p>
			<table width="75%" border="1">
			<%
				  java.sql.PreparedStatement stmt;
				  StringBuffer query=new StringBuffer().append("SELECT * FROM ").append(table);
				  String urlOrderby="";
				  String urlOffset="";

				  if(orderby != null)
				  {
				  	 query.append(" ORDER BY ").append(orderby);
					 urlOrderby="&orderby="+orderby;
				  }	
					
				  if(offset != null)
				  {
				  	 query.append(" LIMIT ").append(offset).append(",10");
					 urlOffset="&offset="+offset;
				  }

				  stmt=db.prepareStatement(query.toString());					
				  java.sql.ResultSet rset=stmt.executeQuery();
				  java.sql.ResultSetMetaData meta=rset.getMetaData();
				  int columnCount=meta.getColumnCount();
				  java.sql.ResultSet dbmeta=db.getMetaData().getPrimaryKeys(null,null,table);
				  java.util.Hashtable list=new java.util.Hashtable();
				  while(dbmeta.next())
				  {
				  		list.put(dbmeta.getString("COLUMN_NAME"),new Integer(dbmeta.getShort("KEY_SEQ")));
				  } 

			%>
				  <tr bgcolor="#FFFF33">
					<td><div align="center">Command</div></td>
					<% for(int cnt=1; cnt <= columnCount; cnt++) { %>				  
						<td> 
						  
      <div align="center"><a href="mysqladmin.jsp?action=query&table=<%= table %>&orderby=<%= meta.getColumnName(cnt) %><%= urlOffset %>"> 
        <% if(list.containsKey(meta.getColumnName(cnt))) { %>
        <b><%= meta.getColumnName(cnt) %></b> 
        <% } else { %>
        <%= meta.getColumnName(cnt) %> 
        <% } %>
        </a></div>
						</td>
					<% } %>
				  </tr>

				  <% while(rset.next()) { %>			  
					  <tr> 						
						<% 
							StringBuffer url=new StringBuffer();
							for(java.util.Enumeration keysEnum=list.keys(); keysEnum.hasMoreElements() ;) 
							{
								String column=(String)keysEnum.nextElement();
								url.append(column).append("=").append(rset.getString(column)).append("&");
							}							
						%>
						
						<% if(!list.isEmpty()) { %>
					    	
							
    <td> <a href="mysqladmin.jsp?action=delete&<%= url %>table=<%= table %>">Delete</a> 
      <a href="mysqladmin.jsp?action=update&<%= url %>table=<%= table %>">Update</a> 
    </td>
						<% } %>

						<% for(int cnt=1; cnt <= columnCount; cnt++) { 
							String value=rset.getString(cnt);
							boolean isnull=rset.wasNull();
						%>				  
							<td><%= (isnull) ? "" : value %></td>
						<% } %>
						
					  </tr>
				  <% }  %>
			</table>		
			<p>&nbsp;</p>
			
<p><a href="mysqladmin.jsp?action=insert&table=<%= table %>">New record....</a></p>
			
			<% if(offset != null)
			   { 
			   		int offs=Integer.parseInt(offset); 
			   		if(offs-10 >= 0) {
			%>
					
<p><a href="mysqladmin.jsp?action=query&table=<%= table %>&offset=<%= String.valueOf(offs-10) %><%= urlOrderby %>">Prev 
  10</a></p>
					
			<%		} %>			
			
					
<p><a href="mysqladmin.jsp?action=query&table=<%= table %>&offset=<%= String.valueOf(offs+10) %><%= urlOrderby %>">Next 
  10</a></p>
			<% } else { %>			

				
<p><a href="mysqladmin.jsp?action=query&table=<%= table %>&offset=0<%= urlOrderby %>">Paged 
  view...</a></p>
			<% } %>			

	<% }
	   else if (action.equals("insert") && table!=null)
	   {
				  java.sql.DatabaseMetaData dbmeta=db.getMetaData();
				  java.sql.ResultSet rset=dbmeta.getColumns(null,null,table,null); 
			%>

			<p><font size="+2"><b><%= table %></b></font></p>
			
<form name="insert" method="post" action="mysqladmin.jsp">
  <table width="43%" border="1">
					<tr bgcolor="#FFFF33">						  
					  <td width="32%" height="29"> 
						<div align="center"><b>Column name</b></div>
					  </td>				 							  
					  <td width="27%" height="29"> 
						<div align="center"><b>Column type</b></div>
					  </td>				  							  
					  <td width="41%" height="29"> 
						<div align="center"><b>Content</b></div>
					  </td>
					</tr>
					<% while(rset.next()) { %>			  
						<tr bgcolor="#CCCCCC"> 					       				  
						  <td width="32%" height="24"> 
							<% if(rset.getString("IS_NULLABLE").equals("NO")) { %>
							<b><%= rset.getString("COLUMN_NAME") %></b> 
							<% } else { %>
							<%= rset.getString("COLUMN_NAME") %> 
							<% } %>
						  </td>					  
						  <td width="27%" height="29"> 
							<div align="center"><b><%= rset.getString("TYPE_NAME") %></b></div>
						  </td>				  
						  <td width="41%" height="24"> 
							<input type="text" name="<%= rset.getString("COLUMN_NAME") %>">
						  </td>
						</tr>
				<% }  %>
			  </table>			  
			  <p>
				<input type="hidden" name="action" value="insert1">
				<input type="hidden" name="table" value="<%= table %>">
			  </p>
			  <p> 
				<input type="submit" name="Submit" value="Store">
			  </p>
			</form>
	<% }
	   else if (action.equals("update") && table!=null)
	   {
		    java.sql.ResultSet rset=db.getMetaData().getColumns(null,null,table,null); 
		    java.sql.ResultSet pkeys=db.getMetaData().getPrimaryKeys(null,null,table);
			java.util.Hashtable colHash=new java.util.Hashtable();
			java.util.Hashtable pkHash=new java.util.Hashtable();
			StringBuffer query=new StringBuffer().append("SELECT * FROM ").append(table).append(" WHERE ");

		    java.sql.ResultSet typerset=db.getMetaData().getTypeInfo();
			java.util.Hashtable sqltypes=new java.util.Hashtable();
			while(typerset.next())
			{
				String literal=typerset.getString("LITERAL_PREFIX");
				sqltypes.put(typerset.getString("TYPE_NAME").toLowerCase(),(literal==null)? "'" : literal);
			}

			while(rset.next())
			{
				colHash.put(rset.getString("COLUMN_NAME"),rset.getString("TYPE_NAME"));
			}

			while(pkeys.next())
			{
				String col=pkeys.getString("COLUMN_NAME");
				pkHash.put(col,col);
				
				query.append(col).append("=");
				
				String type=(String)colHash.get(col);
				type = type.toLowerCase();
				query.append(sqltypes.get(type)).append(request.getParameter(col)).append(sqltypes.get(type));
					
			    if(!pkeys.isLast())
			   		query.append(" AND ");
			}

		    java.sql.PreparedStatement stmt;
			stmt=db.prepareStatement(query.toString());
		    java.sql.ResultSet data=stmt.executeQuery();
			data.next();
			rset.beforeFirst(); 
			
			%>

			<p><font size="+2"><b><%= table %></b></font></p>
			
<form name="update" method="post" action="mysqladmin.jsp">
  <table width="48%" border="1">
					<tr bgcolor="#FFFF33"> 				  
					  <td width="30%" height="29"> 
						<div align="center"><b>Column name</b></div>
					  </td>				  								  
					  <td width="29%" height="29"> 
						<div align="center"><b>Column type</b></div>
					  </td>				  								  
					  <td width="41%" height="29"> 
						<div align="center"><b>Content</b></div>
					  </td>
					</tr>
					<% while(rset.next()) { 
						String column=rset.getString("COLUMN_NAME");
					%>			  
					<tr bgcolor="#CCCCCC"> 					       				  
					  <td width="30%" height="24"> 
						<% if(rset.getString("IS_NULLABLE").equals("NO")) { %>
						<b><%= column %></b> 
						<% } else { %>
						<%= column %> 
						<% } %>
					  </td>					  									  
					  <td width="29%" height="24"><%= rset.getString("TYPE_NAME") %></td>					  
					  <td width="41%" height="24"> 
						<% 
						String value=data.getString(column);
						boolean isnull=data.wasNull();
						
						if(!pkHash.containsKey(column)) { 
						%>
							<input type="text" name="<%= column %>" value="<%= (isnull) ? "" : value %>">
						<% } else { %>
							<%= data.getString(column) %><input type="hidden" name="<%= column %>" value="<%= data.getString(column) %>">
						<% } %>
					  </td>
					</tr>
				<% }  %>
			  </table>			  
			  <p>
				<input type="hidden" name="action" value="update1">
				<input type="hidden" name="table" value="<%= table %>">
			  </p>
			  <p> 
				<input type="submit" name="Submit" value="Store">
			  </p>
			</form>
    <% 		
		}
		else if (table!=null && action.equals("insert1")) 
		{ 	
			java.sql.DatabaseMetaData dbmeta=db.getMetaData();
			java.sql.ResultSet rset=dbmeta.getColumns(null,null,table,null); 
		    java.sql.ResultSet typerset=db.getMetaData().getTypeInfo();
			java.util.Hashtable sqltypes=new java.util.Hashtable();
			while(typerset.next())
			{
				String literal=typerset.getString("LITERAL_PREFIX");
				sqltypes.put(typerset.getString("TYPE_NAME").toLowerCase(),(literal==null)? "'" : literal);
			}

			StringBuffer fields=new StringBuffer();
			StringBuffer values=new StringBuffer();
			while(rset.next()) 
			{			
				String type=rset.getString("TYPE_NAME").toLowerCase();
				String column=rset.getString("COLUMN_NAME");
				String value=request.getParameter(column);
				
				if(rset.getString("IS_NULLABLE").equals("NO") && (value==null || value.equals("")))
				{
					response.sendRedirect("mysqladmin.jsp?action=insert&table=" + table);
					return;		
				}				

				fields.append(column);				
				if(value!=null && !value.equals(""))
				{
					values.append(sqltypes.get(type)).append(value).append(sqltypes.get(type)); 					
				}
				else
					values.append("NULL"); 				
				
				if(!rset.isLast())
				{
					fields.append(",");
					values.append(",");
				}
			}
			
			String insert=new StringBuffer().append("INSERT INTO ").append(table).append(" (").append(fields.toString()).append(") VALUES (").append(values).append(")").toString();

			try
			{
				db.createStatement().executeUpdate(insert);
				if(!db.getAutoCommit())
					db.commit();
			}
			catch(Exception exc)
			{ %>
				<p>SQL statement : <%= insert.toString() %></p>
				<p>Exception : <%= exc.getMessage() %></p>
  <%
			 	return;
			}
				
			response.sendRedirect("mysqladmin.jsp?action=query&table=" + table);
		}
		else if (table!=null && action.equals("delete")) 
		{ 	
			java.sql.ResultSet columns=db.getMetaData().getColumns(null,null,table,null); 
		    java.sql.ResultSet typerset=db.getMetaData().getTypeInfo();
			java.util.Hashtable sqltypes=new java.util.Hashtable();
			while(typerset.next())
			{
				String literal=typerset.getString("LITERAL_PREFIX");
				sqltypes.put(typerset.getString("TYPE_NAME").toLowerCase(),(literal==null)? "'" : literal);
			}

			java.util.Hashtable colHash=new java.util.Hashtable();
			while(columns.next())
			{
				colHash.put(columns.getString("COLUMN_NAME"),columns.getString("TYPE_NAME"));
			}

		    java.sql.ResultSet pkeys=db.getMetaData().getPrimaryKeys(null,null,table);
			StringBuffer stmt=new StringBuffer().append("DELETE FROM ").append(table).append(" WHERE ");
			while(pkeys.next())
			{
			    String column=pkeys.getString("COLUMN_NAME");
				String value=request.getParameter(column);
				stmt.append(column).append("=");
				String type=(String)colHash.get(column);
				type = type.toLowerCase();
				stmt.append(sqltypes.get(type)).append(value).append(sqltypes.get(type)); 
					
			    if(!pkeys.isLast())
					stmt.append(" AND "); 
			}
						
			try
			{
				db.createStatement().executeUpdate(stmt.toString());
				if(!db.getAutoCommit())
					db.commit();
			}
			catch(Exception exc)
			{ %>
				<p>SQL statement : <%= stmt.toString() %></p>
				<p>Exception : <%= exc.getMessage() %></p>
  <%
			 	return;
			}
				
			response.sendRedirect("mysqladmin.jsp?action=query&table=" + table);
		}
		else if (table!=null && action.equals("update1")) 
		{ 	
			java.sql.ResultSet columns=db.getMetaData().getColumns(null,null,table,null); 
		    java.sql.ResultSet typerset=db.getMetaData().getTypeInfo();
			java.util.Hashtable sqltypes=new java.util.Hashtable();
			while(typerset.next())
			{
				String literal=typerset.getString("LITERAL_PREFIX");
				sqltypes.put(typerset.getString("TYPE_NAME").toLowerCase(),(literal==null)? "" : literal);
			}

			java.util.Hashtable colHash=new java.util.Hashtable();
			while(columns.next())
			{
				colHash.put(columns.getString("COLUMN_NAME"),columns.getString("TYPE_NAME"));
			}

		    java.sql.ResultSet pkeys=db.getMetaData().getPrimaryKeys(null,null,table);
			java.util.Hashtable pkHash=new java.util.Hashtable();
			StringBuffer where=new StringBuffer().append(" WHERE ");
			while(pkeys.next())
			{
				String column=pkeys.getString("COLUMN_NAME");
				pkHash.put(column,column);
				String value=request.getParameter(column);
				where.append(column).append("=");
				String type=(String)colHash.get(column);
				type= type.toLowerCase();
				where.append(sqltypes.get(type)).append(value).append(sqltypes.get(type)); 
					
			    if(!pkeys.isLast())
					where.append(" AND "); 
			}

			StringBuffer stmt=new StringBuffer().append("UPDATE ").append(table).append(" SET ");
			boolean isfirstcol=true;
			for(java.util.Enumeration keysEnum=colHash.keys(); keysEnum.hasMoreElements() ;) 
			{
				String column=(String)keysEnum.nextElement();
				if(!pkHash.containsKey(column))
				{
					if(isfirstcol)
						isfirstcol=false;
					else
						stmt.append(","); 

					String value=request.getParameter(column);
					stmt.append(column).append("=");
					String type=(String)colHash.get(column);
					type= type.toLowerCase();
					if(value!=null && !value.equals(""))
					{
						stmt.append(sqltypes.get(type)).append(value).append(sqltypes.get(type)); 
					}
					else
						stmt.append("NULL");							
				}
			}
			stmt.append(where);							
						
			try
			{
				db.createStatement().executeUpdate(stmt.toString());
				if(!db.getAutoCommit())
					db.commit();
			}
			catch(Exception exc)
			{ %>
				<p>SQL statement : <%= stmt.toString() %></p>
				<p>Exception : <%= exc.getMessage() %></p>
  <%
			 	return;
			}
				
			response.sendRedirect("mysqladmin.jsp?action=query&table=" + table);
	%>
  <% } %>


</body>
</html>

<%
	db.close();
%>
