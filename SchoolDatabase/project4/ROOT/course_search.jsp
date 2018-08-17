<%@ page import="java.sql.*" %>

<link rel="stylesheet" href="styles.css">

<%
String connectionURL =
"jdbc:postgresql://class-db.cs.fiu.edu:5432/spr18_adelg001?user=spr18_adelg001&password=2059273";

Connection connection = null;
Statement statement = null;
ResultSet rs = null;
%>
 
<html><body>

<div class="center_div">

<h1>Search Results:</h1>
<br>
<% 

	String des  = request.getParameter("description");
	if(des == null )
	{
		out.println("ERROR taking input search term!<br>");
		response.sendRedirect("get_course_description.jsp");

	}
	else
	{


%>

 
<table>
<tr>
<th><strong>course_id</strong></th>
<th><strong>description</strong></th>
<th><strong>level</strong></th>
<th><strong>instructor</strong></th>
<th><strong>semester</strong></th>

</tr>

<%
Class.forName("org.postgresql.Driver").newInstance();
connection = DriverManager.getConnection(connectionURL);
statement = connection.createStatement();
rs = statement.executeQuery("SELECT * FROM courses WHERE description = \'"+ des+ "\' ;");


while (rs.next()) {

%>
<tr>
<td><%out.println(rs.getString("course_id"));%></td>
<td><%out.println(rs.getString("description") );%></td>
<td><%out.println(rs.getString("level"));%></td>
<td><%out.println(rs.getString("instructor"));%></td>
<td><%out.println(rs.getString("semester"));%></td>
</tr>


<%

}

rs.close();

}

%>

</table>

<form action="home.jsp" method="post">
<br>
<br>
<input type="Submit" value="Home" >

</div>
</body></html>

