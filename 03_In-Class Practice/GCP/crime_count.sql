  /*Summarization each year crime count*/
SELECT
  year,
  COUNT(*) AS total_crimes
FROM
  `bigquery-public-data.austin_crime.crime`
GROUP BY
  year
ORDER BY
  year ASC;
  
/*Clustering crime count by location and district*/ 
SELECT
  DISTINCT location,
  district,
  COUNT(*) AS count
FROM
  `bigquery-public-data.austin_crime.crime`
GROUP BY
  location,
  district
ORDER BY
  location, district;

/*filter using where clause*/
SELECT
  location,
  COUNT(*) AS theft_count
FROM
  `bigquery-public-data.austin_crime.crime`
WHERE
  primary_type = 'Theft'
GROUP BY
  location
ORDER BY
  theft_count DESC
LIMIT 10;

 /*Partition by*/ /*This query returns the most recent crime record (based on the timestamp) for each crime description (such as "burglary," "assault," etc.), along with the count of crimes that occurred at that specific timestamp. The crime count is aggregated for each description and timestamp combination.*/
WITH
  RankedCrimes AS (
  SELECT
    description,
    timestamp,
    COUNT(unique_key) AS crime_count,
    ROW_NUMBER() OVER (PARTITION BY description ORDER BY timestamp DESC) AS rank
  FROM
    `bigquery-public-data.austin_crime.crime`
  GROUP BY
    description,
    timestamp )
SELECT
  description,
  timestamp,
  crime_count
FROM
  RankedCrimes
WHERE
  rank = 1
ORDER BY
  description;