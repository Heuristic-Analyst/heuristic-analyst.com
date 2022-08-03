In these files I wrote some code to gather:
 - Official CIK mapping of public companies (found here: https://www.sec.gov/files/company_tickers.json)
 - Submissions and description of company (e.g. Apple: https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json)

The information is gathered and transformed into CSVs and JSONs and saved in subfolders (foldername is ticker).

To transform it for usage of also private companies you should change the following:
 - Foldername when saved from ticker to comp name
 - Search of CIK through comp name and not ticker
 - you should add the private companies by yourself to the CIK mapping list

HOW TO RUN THE PROGRAM:
 - open app.js and edit the parameters to yours (where to save stuff, User-Agent-Header, etc.)
 - run "node app.js"