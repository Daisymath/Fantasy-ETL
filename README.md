# Fantasy ETL
 ETL files for scraping fantasy football data

# ETL Process

Data for this project comes from multiple sources:

1)  ESPN (current ADP, rankings, projections)
2)  https://www.pro-football-reference.com/ (season stats)
3)  https://fantasyfootballcalculator.com (historical ADP)

## Extract 
Season long stats for players was downloaded directly from 2).  This site includes a player ID which was used to connect each separate data source.

Historical ADP was scraped from 3) a single time.  This scraping used Beautiful Soup inside Python.

Finally, current ADP, rankings, and projections are dynamically scraped from ESPN.

## Transform

The 2023 ADP was joined to the file with historical ADPs and the rankings and projections files were updated.  This involved some light cleanup of column names.

This process had some manual adjustments needed:

1) Some players names are different between websites.  For example, Marvin Jones Jr. from one source was Marvin Jones in another.
2) The rookies needed their player ids manually searched for and entered into the playerID master file.  This is because they did not have season stats from 2) which produced this ID.

## Load

The last steps in this process were to load data into Google Drive and then connect to Tableau Public. 

This was done using the Google API inside Python.  First, old files were deleted from Google Drive and then the newly scraped files were uploaded in their place.

Lastly, Tableau Public was connected to these csv files and then connected via the PlayerID inside Tableau.

Please feel free to ask me any questions you have and thank you for reading!
