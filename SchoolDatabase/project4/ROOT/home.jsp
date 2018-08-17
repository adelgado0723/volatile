<%@ page import="java.sql.*" %>

<link rel="stylesheet" href="styles.css">


 
<html><body>

<div class="center_div">
<h1>Welcome to the University Database.</h1>
 <br/>





<h2>Alter Database</h2>
<ul>
	<li>
		<h3><a href="http://ocelot.aul.fiu.edu:5153/error.jsp">Insert Data</a><h3>
		<p>
						
		</p>
	</li>
	<li>
		<h3><a href="http://ocelot.aul.fiu.edu:5153/error.jsp">Delete Data</a><h3>
		<p>
			Delete a table, or information within a table.
		</p>
	</li>
	<li>
		<h3><a href="http://ocelot.aul.fiu.edu:5153/error.jsp">Update Data</a><h3>
		<p>

		</p>
	</li>

 
</ul>
<br/>

<h2>Search Database</h2>
<ul>
	<li>
		<h3><a href="http://ocelot.aul.fiu.edu:5153/search_for_name.jsp">Search Student/Faculty Name</a><h3>
		<p>
			Search for a student or faculty member by name.			
		</p>
	</li>
	<li>
		<h3><a href="http://ocelot.aul.fiu.edu:5153/get_course_description.jsp">Search Courses By Description</a><h3>
		<p>
			Search for a course record using the description of the course.	
		</p>
	</li>
 
</ul>

<br/>

<h2>View Tables:</h2>

<ul>
	<li>
		<h3><a href="http://ocelot.aul.fiu.edu:5153/students.jsp">Students</a><h3>
		<p>
			The Students page contains the personal contact information of each 
			student as well as their unique student id. 
		</p>
	</li>
	<li>
		<h3><a href="http://ocelot.aul.fiu.edu:5153/faculties.jsp">Faculties</a><h3>
		<p>
			The Faculties page contains the personal contact information of each 
			faculty member as well as their unique faculty id. 

		</p>
	</li>
 	<li>
		<h3><a href="http://ocelot.aul.fiu.edu:5153/courses.jsp">Courses</a><h3>
		<p>
			The COURSES table contains each course's unique course id as well as
			a brief description of the course and information about the professor
			teaching the course as well as the semester in which the course
			was offered.
		</p>

	</li>
	<li>
		<h3><a href="http://ocelot.aul.fiu.edu:5153/enroll.jsp">Enroll</a><h3>
		<p>
			The Enroll Page contains the entire ENROLL table which
			keeps records containing a student id, a course id, and the grade that the
			student received in the course.
		</p>
	</li>
 

</ul>
</div>
</body></html>
