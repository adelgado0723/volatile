<%@ page import="java.sql.*" %>

<link rel="stylesheet" href="styles.css">
 
<html><body>

<div class="center_div">

<h1>Course Search By Description</h1>
<br>
<form action="delete.jsp" method="post">
Select table to be operated on...

<br>
<select name="relation" >

	<option value="faculties">FACULTIES</option>
	<option value="students">STUDENTS</option>
	<option value="courses">COURSES</option>
	<option value="enroll">ENROLL</option>
</select>

<br>
Select delete options...

<br>
<select name="delete_option" >

	<option value="dRecord">Delete Record</option>
	<option value="dAttribute">Delete Attribute</option>
	<option value="dTable">Delete Table</option>
</select>

<br>

<input type="Submit"  value="ENTER" >




</div>
</body></html>
