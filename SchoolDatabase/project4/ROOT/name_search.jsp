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

	String role = request.getParameter("search_term");
	String sname  = request.getParameter("search_name");
	if(sname == null )
	{
		out.println("ERROR taking input search term!<br>Make sure all search fields are filled out.<br>");
		response.sendRedirect("search_for_name.jsp");


	}
	else
	{


%>

 
<table>

<tr>
<th><strong>id</strong></th>
<th><strong>name</strong></th>
<th><strong>date_of_birth</strong></th>
<th><strong>address</strong></th>
<th><strong>email</strong></th>
<th><strong>level</strong></th>

</tr>


<%
if(role.equals("student"))
{
Class.forName("org.postgresql.Driver").newInstance();
connection = DriverManager.getConnection(connectionURL);
statement = connection.createStatement();
rs = statement.executeQuery("SELECT * FROM students WHERE name = \'"+ sname+ "\' ;");


while (rs.next()) {

%>
<tr>
<td><%out.println(rs.getString("student_id"));%></td>
<td><%out.println(rs.getString("name") );%></td>
<td><%out.println(rs.getString("date_of_birth"));%></td>
<td><%out.println(rs.getString("address"));%></td>
<td><%out.println(rs.getString("email"));%></td>
<td><%out.println(rs.getString("level"));%></td>
</tr>
<%

}

rs.close();



}

else if(role.equals("faculty"))
{

Class.forName("org.postgresql.Driver").newInstance();
connection = DriverManager.getConnection(connectionURL);
statement = connection.createStatement();
rs = statement.executeQuery("SELECT * FROM faculties WHERE name = \'"+ sname + "\';");

while (rs.next()) {

%>
<tr>
<td><%out.println(rs.getString("faculty_id"));%></td>
<td><%out.println(rs.getString("name") );%></td>
<td><%out.println(rs.getString("date_of_birth"));%></td>
<td><%out.println(rs.getString("address"));%></td>
<td><%out.println(rs.getString("email"));%></td>
<td><%out.println(rs.getString("level"));%></td>
</tr>

<%

}

rs.close();
}
}


%>

	
 
</table>

<form action="home.jsp" method="post">

<br>
<br>

<input type="Submit" value="Home" >

</div>
</body></html>

