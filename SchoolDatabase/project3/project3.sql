CREATE FUNCTION calculateGradeProbs() 
RETURNS void  AS $$


	DECLARE
		
		assigned  INTEGER;
		numGrades INTEGER;
		numStudents INTEGER;
		numSchools INTEGER;
		schCode	   INTEGER;
		tmpGrade   INTEGER;
		numGradesLeft INTEGER;
		letterGrade text;
		stuCount   NUMERIC;
		aGrades	   NUMERIC;
		aMinusGrades NUMERIC;
		bPlusGrades  NUMERIC;
		bGrades	   NUMERIC;
		cGrades	   NUMERIC;
		dGrades	   NUMERIC;
		r	   NUMERIC;
	BEGIN

		SELECT INTO numSchools MAX(school_code)
		FROM school_probabilities;

		-- raise notice 'Value: %', numSchools;
		
		CREATE TABLE dist( 
						school_id bigint references school_probabilities(school_code),
						aG numeric, 
						aMinusG numeric,
						bPlusG numeric,
						bG numeric,
						cG numeric,
						dG numeric
							);

		-- Populating table with values.	

		For i IN 1..numSchools Loop

			r := 0;	

			-- Get count of students at each school
			select INTO stuCount COUNT(simulated_recs.school)
			from simulated_recs, school_probabilities
			where simulated_recs.school = school_probabilities.school AND school_code = i
			group by simulated_recs.school, school_probabilities.school_code
			;


			-- Calculating Probabilities and saving the remainder.			

			Select INTO aGrades Cast(probs[1] AS NUMERIC) from school_probabilities where school_code = i;
			aGrades := aGrades * stuCount;
			r := aGrades - floor(aGrades);
			aGrades := Floor(aGrades);

			Select INTO aMinusGrades Cast(probs[2] AS NUMERIC) from school_probabilities where school_code = i;
			aMinusGrades := aMinusGrades * stuCount;
			r := r +  (aMinusGrades - floor(aMinusGrades));
			aMinusGrades := Floor(aMinusGrades) ;


			Select INTO bPlusGrades Cast(probs[3] AS NUMERIC) from school_probabilities where school_code = i;
			bPlusGrades := bPlusGrades * stuCount;
			r := r + (bPlusGrades - floor(bPlusGrades));
			bPlusGrades := Floor(bPlusGrades);


			Select INTO bGrades Cast(probs[4] AS NUMERIC) from school_probabilities where school_code = i;
			bGrades := bGrades * stuCount;
			r := r + (bGrades - floor(bGrades));
			bGrades := Floor(bGrades);
					

			Select INTO cGrades Cast(probs[5] AS NUMERIC) from school_probabilities where school_code = i;
			cGrades := cGrades * stuCount;
			r := r + (cGrades - floor(cGrades));
			cGrades := Floor(cGrades);


			Select INTO dGrades Cast(probs[6] AS NUMERIC) from school_probabilities where school_code = i;
			dGrades := dGrades * stuCount;
			r := r + (dGrades - floor(dGrades));
			dGrades := Floor(dGrades);
			

			r := ROUND(r);

			-- Making the remaining grades C's

			cGrades := cGrades + r;
			

			-- Inserting calculated values into the dist table.	
			INSERT INTO dist
			(school_id, aG, aMinusG, bPlusG, bG, cG, dG)
			VALUES
			(
				i, aGrades, aMinusGrades, bPlusGrades, bGrades, cGrades, dGrades
				
			);

			

		End Loop;

		/*
			The grades are randomly assigned by iterating through each student 
			and producing a random number in the range of 1 - 6. This number 
			represents the potential grade to be distributed. If that school 
			still has some of those grades left to give out, it does. Then it
			decrements the number of those grades available by one and updates 
			the dist table. On the other hand, if a grade is 
			assigned, but that school has no more of that grade left to 
			allocate, then it increments then it traverses and checks the other
			possible grades in a circular fashion.


		*/	
		SELECT INTO numStudents MAX(record_id)
		FROM simulated_recs;
		
		SELECT INTO numGrades MAX(id)
		FROM grade_values;

		For i IN 1..numStudents Loop

			-- Randomly select grade for the school
			
			-- Obtaining the code of the school that this student attends
			select INTO schCode school_probabilities.school_code
			from simulated_recs, school_probabilities
			where simulated_recs.school = school_probabilities.school AND record_id = i;
			
			assigned := 0;
			
			tmpGrade := ROUND(RANDOM() * (numGrades-1)) + 1;

			-- Assigning an available grade
			WHILE (	assigned = 0) Loop
				
				-- Random Grader Assigned A
				IF tmpGrade = 1 THEN
					Select into numGradesLeft aG
					from dist
					where school_id = schCode;
			
					IF numGradesLeft > 0 THEN
						
						Select INTO letterGrade grade from grade_values where id = tmpGrade;
						UPDATE simulated_recs
						SET grade = letterGrade
						WHERE record_id = i;

						numGradesLeft := numGradesLeft - 1;
					
						UPDATE dist 
						SET aG = numGradesLeft
						WHERE school_id = schCode;
						assigned := 1;
					ELSE
					
						tmpGrade := tmpGrade + 1;


					END IF;
				
				-- Random Grader Assigned A-
				ELSIF tmpGrade = 2 THEN
					Select into numGradesLeft aMinusG
					from dist
					where school_id = schCode;
			
					IF numGradesLeft > 0 THEN
					
							
						Select INTO letterGrade grade from grade_values where id = tmpGrade;
						UPDATE simulated_recs
						SET grade = letterGrade
						WHERE record_id = i;

						numGradesLeft := numGradesLeft - 1;
					
						UPDATE dist 
						SET aMinusG = numGradesLeft
						WHERE school_id = schCode;
						assigned := 1;
					ELSE
					
						tmpGrade := tmpGrade + 1;


					END IF;
			

				-- Random Grader Assigned B+
				ELSIF tmpGrade = 3 THEN
					Select into numGradesLeft bPlusG
					from dist
					where school_id = schCode;
					IF numGradesLeft > 0 THEN
									
						Select INTO letterGrade grade from grade_values where id = tmpGrade;
						UPDATE simulated_recs
						SET grade = letterGrade
						WHERE record_id = i;

						numGradesLeft := numGradesLeft - 1;
					
						UPDATE dist 
						SET bPlusG = numGradesLeft
						WHERE school_id = schCode;
						assigned := 1;
					ELSE
					
						tmpGrade := tmpGrade + 1;


					END IF;
			


				-- Random Grader Assigned B
				ELSIF tmpGrade = 4 THEN
					Select into numGradesLeft bG
					from dist
					where school_id = schCode;
			
					IF numGradesLeft > 0 THEN
					
						
						Select INTO letterGrade grade from grade_values where id = tmpGrade;
						UPDATE simulated_recs
						SET grade = letterGrade
						WHERE record_id = i;


						numGradesLeft := numGradesLeft - 1;
					
						UPDATE dist 
						SET bG = numGradesLeft
						WHERE school_id = schCode;
						assigned := 1;
					
					ELSE
					
						tmpGrade := tmpGrade + 1;

					END IF;
				

				-- Random Grader Assigned C
				ELSIF tmpGrade = 5 THEN
					Select into numGradesLeft cG
					from dist
					where school_id = schCode;

					IF numGradesLeft > 0 THEN
												
						Select INTO letterGrade grade from grade_values where id = tmpGrade;
						UPDATE simulated_recs
						SET grade = letterGrade
						WHERE record_id = i;
						numGradesLeft := numGradesLeft - 1;
					
						UPDATE dist 
						SET cG = numGradesLeft
						WHERE school_id = schCode;
						assigned := 1;
					ELSE
					
						tmpGrade := tmpGrade + 1;


					END IF;
			
				-- Random Grader Assigned a D
				ELSIF tmpGrade = 6 THEN
					Select into numGradesLeft dG
					from dist
					where school_id = schCode;
					IF numGradesLeft > 0 THEN
											
						Select INTO letterGrade grade from grade_values where id = tmpGrade;
						UPDATE simulated_recs
						SET grade = letterGrade
						WHERE record_id = i;

						numGradesLeft := numGradesLeft - 1;
					
						UPDATE dist 
						SET dG = numGradesLeft
						WHERE school_id = schCode;
						assigned := 1;

					ELSE
						tmpGrade := 1;
					END IF;
				END IF;
			END LOOP;

		END LOOP;
		Drop table dist cascade;
	
	END;


