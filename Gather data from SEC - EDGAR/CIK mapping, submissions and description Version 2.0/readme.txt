In these files I wrote some code to gather:
 - Official CIK mapping of public companies (found here: https://www.sec.gov/files/company_tickers.json)
 - Submissions and description of company (e.g. Apple: https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json)

It can download submission files by ticker, title and cik number

The information is gathered and transformed into CSVs and JSONs and saved in subfolders (foldername is CIK number, because some companies could have "/" or other symbols in their name, and not every company has a ticker/is a public company).

It just download submissions and descriptions data of companies that are listed in the CIK mapping csv I create, so if you want to add other companies, just add them to the csv!

HOW TO RUN THE PROGRAM:
 - make sure the libraries "axios", "fs" and "perf_hooks", and the framework NodeJS are available/installed
 - open app.js and edit these parameters to yours:
    var user_agent = "Company YourName YourEmail";
    var folder_save_here = "./Example Output/";
    var ticker = ["AAPL", "F"];
    var title = ["Tesla, Inc."];
    var ciks = ["0001067983"];
    var download_new_cik_data = true;
    var download_new_submissions_data = true;
 - run app.js by typing "node app.js" in your command prompt
