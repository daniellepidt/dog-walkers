#-----------------------------------------------------------------------------------------------#
-- -1- --
-- עבור יום בשבוע וחלק ביום שעבורם יש לפחות 5 מוליכי כלבים שרשומים לטיול עם כלבים כעת -- 
-- החזירו את היום בשבוע, החלק ביום ומספר הכלבים הרשומים --
-- מיינו את הרשימה לפי יום בשבוע בסדר עולה --

SELECT day_in_the_week, part_of_day, COUNT(DISTINCT(dog_number)) AS num_of_dogs
From Walk
WHERE request_status = 'accepted'
GROUP BY day_in_the_week, part_of_day
HAVING COUNT(DISTINCT(dog_walker_email)) > 4
ORDER BY FIELD(day_in_the_week, "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday");

#-----------------------------------------------------------------------------------------------#
-- -2- --
-- עבור מוליך כלבים שנרשם כפרמיום בשנת 2021 והתכתב עם בעלי כלבים שברשותם לפחות כלב אחד שרשום לטיולים עם מוליך זה --
-- הציגו את האימייל, שם פרטי ומשפחה של מוליך הכלבים ומספר הודעות בין מוליך הכלבים לבין בעלי הכלבים שרשומים אליו כעת --
-- מיינו לפי מספר הודעות בסדר יורד -- 

SELECT user_email, first_name, last_name, COUNT(*) AS num_of_messages
FROM
	(SELECT MATCH_W_O.dog_walker_email, MATCH_W_O.dog_owner_email, message_id
	 FROM
		 (SELECT dog_walker_email ,dog_owner_email
		  FROM Walk AS WK JOIN Dog AS D ON WK.dog_number = D.dog_number
		  WHERE request_status = 'accepted'
		  GROUP BY dog_walker_email ,dog_owner_email
		 ) AS MATCH_W_O 
		JOIN Send_Receive_Message AS SRM
		ON ((MATCH_W_O.dog_owner_email = SRM.dog_owner_email) AND (MATCH_W_O.dog_walker_email = SRM.premium_dog_walker_email))
    ) AS W_O_M
    JOIN Dog_Walker AS W 
    ON W_O_M.dog_walker_email = W.dog_walker_email
    JOIN Users AS U 
    ON W.dog_walker_email = U.user_email
WHERE YEAR(registration_date_as_premium) = "2021"
GROUP BY user_email, first_name, last_name
ORDER BY num_of_messages DESC;

#-----------------------------------------------------------------------------------------------#
-- -3- --
-- עבור מוליך שרשומים אליו כעת רק כלבים מחוסנים וידודותיים --
-- החזירו את שמו ואימייל --
 
SELECT DISTINCT first_name, last_name, user_email
FROM Users AS U JOIN Walk AS WK1 ON U.user_email = WK1.dog_walker_email
WHERE WK1.request_status = 'accepted' 
	  AND
      WK1.dog_walker_email NOT IN (SELECT DISTINCT(WK2.dog_walker_email)
									FROM Walk AS WK2 JOIN Dog AS D ON WK2.dog_number = D.dog_number
									WHERE is_vaccinated IS FALSE OR is_friendly IS FALSE);
                                    
#-----------------------------------------------------------------------------------------------#     
-- -4- --
-- עבור כל כלב שרשום כעת לטיול אחד לפחות --
-- החזירו את מספר הכלב, שם הכלב, והאימייל של מוליך הכלבים שהכלב רשום אליו עם מספר הטיולים הגבוה ביותר (המוליך שמבצע עם אותו הכלב הכי הרבה טיולים -- 

SELECT WK1.dog_number, D.dog_name, WK1.dog_walker_email
FROM  Walk AS WK1 JOIN Dog As D ON WK1.dog_number = D.dog_number 
WHERE WK1.request_status = 'accepted'
GROUP BY WK1.dog_number, D.dog_name, WK1.dog_walker_email
HAVING COUNT(*) = 
	(SELECT MAX(num_of_walks)
	FROM
		(SELECT WK2.dog_number, WK2.dog_walker_email, COUNT(*) AS num_of_walks
		FROM Walk AS WK2
		WHERE WK2.request_status = 'accepted'
		GROUP BY WK2.dog_number, WK2.dog_walker_email) AS MAXI
	WHERE WK1.dog_number = MAXI.dog_number
	GROUP BY MAXI.dog_number);