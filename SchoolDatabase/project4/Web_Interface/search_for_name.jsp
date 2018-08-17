<%@ page import="java.sql.*" %>

<link rel="stylesheet" href="styles.css">


 
<html><body>

<div class="center_div">

<h1>Student/Faculty Search By Name</h1>
<br>
<form action="name_search.jsp" method="post">
Please Enter the name of the Student or Faculty Member to be found:
<input type="text" name="search_name">
<select name="search_term" >
	<option value="faculty">Faculty</option>
	<option value="student">Student</option>

</select>
<input type="Submit" name="search_term" value="Search" >

</div>
</body></html>
