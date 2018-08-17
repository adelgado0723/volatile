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
<h1>STUDENTS Table</h1>
 
<table>
<%
Class.forName("org.postgresql.Driver").newInstance();
connection = DriverManager.getConnection(connectionURL);
statement = connection.createStatement();
rs = statement.executeQuery("SELECT * FROM students");
%>
<tr>
<th><strong>student_id</strong></th>
<th><strong>name</strong></th>
<th><strong>date_of_birth</strong></th>
<th><strong>address</strong></th>
<th><strong>email</strong></th>
<th><strong>level</strong></th>

</tr>
<%
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
%>
 
</table>

</div>
</body></html>
