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
<h1>COURSES Table</h1>
 
<table>
<%
Class.forName("org.postgresql.Driver").newInstance();
connection = DriverManager.getConnection(connectionURL);
statement = connection.createStatement();
rs = statement.executeQuery("SELECT * FROM courses");
%>
<tr>
<th><strong>course_id</strong></th>
<th><strong>description</strong></th>
<th><strong>level</strong></th>
<th><strong>instructor</strong></th>
<th><strong>semester</strong></th>

</tr>
<%
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

%>
 
</table>

</div>
</body></html>
