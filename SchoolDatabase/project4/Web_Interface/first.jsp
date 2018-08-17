<%@ page import="java.sql.*" %>
This program test connectivity of PostgreSQL from JSP<br>
Contents of students table (created by  create table students (student_id integer, name text,...) <br>
id  name<br>
-----------<br>
 
<%
String connectionURL =
"jdbc:postgresql://class-db.cs.fiu.edu:5432/spr18_adelg001?user=spr18_adelg001&password=2059273";

Connection connection = null;
Statement statement = null;
ResultSet rs = null;
%>
 
<html><body>
 
<%
Class.forName("org.postgresql.Driver").newInstance();
connection = DriverManager.getConnection(connectionURL);
statement = connection.createStatement();
rs = statement.executeQuery("SELECT * FROM students");
 
while (rs.next()) {
out.println(rs.getString("student_id")+"<br>");
out.println(rs.getString("name")+"<br>");
}
 
rs.close();
%>
 
</body></html>
