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

<html>
<head>
<title>MySQL Database Admnistration Tool</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>
<frameset cols="250,*" frameborder="NO" border="0" framespacing="0"> 
  <frame name="leftFrame" src="mysqladmin.jsp">
  <frame name="mainFrame" src="mysqlstruct.jsp?action=create">
</frameset>
<noframes>
<body bgcolor="#FFFFFF" text="#000000">
</body>
</noframes> 
</html>
