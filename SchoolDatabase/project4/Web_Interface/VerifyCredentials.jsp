<%@page contentType="text/html" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>




<html>
	<head>
		<link rel="stylesheet" href="styles.css">
	</head>
	<body>

		<%
		String username = request.getParameter("username");
		String password = request.getParameter("password");

		if(username.equals("adelg001")&&password.equals("cop4710"))
		{
			session.setAttribute("username", username);
			response.sendRedirect("home.jsp");

		}
		else
		{
			out.println("ERROR: Incorrect username and/or password!");

		}

		%>


	</body>
</html>

