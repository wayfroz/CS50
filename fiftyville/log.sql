-- Keep a log of any SQL queries you execute as you solve the mystery.

--see what crimes have been reported
SELECT * FROM crime_scene_reports WHERE month = 7 AND day= 28 AND street = "Humphrey Street";

--check interviews of three witnesses
SELECT * FROM interviews WHERE month = 7 AND day = 28;
--Checking liscence palte
SELECT * FROM bakery_security_logs WHERE month = 7 AND day = 28 AND license_plate = "0NTHK55" OR license_plate = "322W7JE";
--checkig atm withdrawings
SELECT * FROM atm_transactions WHERE atm_location = "Leggett Street" AND transaction_type = "withdraw" AND day = 28 AND month = 7;
--acctount_numbers
--28500762 28296815 76054385 49610011 16153065 25506511 81061156 26013199
--JOIN with bank_accounts to search for PERSON_ID who made a withdrawl on that day
SELECT * FROM bank_accounts
JOIN atm_transactions
ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.atm_location = "Leggett Street"
AND atm_transactions.transaction_type = "withdraw"
AND atm_transactions.day = 28
AND atm_transactions.month = 7;
--try to connect with PEOPLE table
SELECT name, passport_number FROM PEOPLE
INNER JOIN bank_accounts ON people.id = bank_accounts.person_id
INNER JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.atm_location = "Leggett Street"
AND atm_transactions.transaction_type = "withdraw"
AND atm_transactions.day = 28
AND atm_transactions.month = 7;
--check passengers who flew connecting it with passports #
SELECT people.name, passengers.passport_number, flight_id FROM passengers
JOIN people ON people.passport_number = passengers.passport_number
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.atm_location = "Leggett Street"
AND atm_transactions.transaction_type = "withdraw"
AND atm_transactions.day = 28
AND atm_transactions.month = 7
ORDER BY name ASC;
--checking flights using a person's passport_number
SELECT city, people.name, flights.day, flights.month FROM airports
JOIN flights ON flights.destination_airport_id = airports.id
JOIN passengers ON passengers.flight_id = flights.destination_airport_id
JOIN people ON people.passport_number = passengers.passport_number
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.atm_location = "Leggett Street"
AND atm_transactions.transaction_type = "withdraw"
AND atm_transactions.day = 28
AND atm_transactions.month = 7;

--checking names (8 names)
SELECT people.name, people.passport_number, people.phone_number FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.atm_location = "Leggett Street"
AND atm_transactions.transaction_type = "withdraw"
AND atm_transactions.day = 28
AND atm_transactions.month = 7
ORDER BY name ASC;

--check where and WHO flew on July 29
SELECT flights.month, flights.day, people.name, airports.city from airports
JOIN flights ON flights.destination_airport_id = airports.id
JOIN passengers ON passengers.flight_id = flights.id
JOIN people ON people.passport_number = passengers.passport_number
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.atm_location = "Leggett Street"
AND atm_transactions.transaction_type = "withdraw"
AND atm_transactions.day = 28
AND atm_transactions.month = 7
AND flights.day = 29
AND flights.month = 7
ORDER BY name ASC;

--check the time when the thief (Diana) left the bakery
SELECT * FROM phone_calls
WHERE month = 7
AND day = 28
AND caller = "(367) 555-5533"
AND duration <= 60;
-- who's the accomplice
SELECT * FROM people
WHERE phone_number = "(609) 555-5876";
--passport "3391710505"
SELECT month, day FROM flights
WHERE id IN
(SELECT * FROM passengers
WHERE passport_number = "3391710505");

SELECT * FROM people
WHERE license_plate = "32W7JE";

SELECT * FROM phone_calls
WHERE month = 7
AND day = 28
AND duration < 60;

--whom Philip called
SELECT * FROM phone_calls
WHERE day = 28
AND month = 7
AND receiver = "(389) 555-5198";


SELECT * FROM people
WHERE name = "Brooke" OR name = "Bruce" OR name = "Kenny" OR name = "Luca" OR name = "Taylor";