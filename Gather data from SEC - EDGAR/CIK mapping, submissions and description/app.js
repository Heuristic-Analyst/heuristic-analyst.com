const downloadCikData = require("./downloadCikData");
const downloadSubmissionsData = require("./downloadSubmissionsData");
const { performance } = require('perf_hooks');

//##############################
//Where to save the data (will create subfolders for each ticker)
let dataFolder = "";
//Filename and path of CIK mapping
let cikDataFilename = "CikData.csv";
let cikDataFilepath = dataFolder+cikDataFilename;
//SEC/EDGAR wants some info about the person who uses their API
let userAgentString = "CompanyName YourName Email";
//Ticker list of the submissions and descriptions we want to get
let getDataOfTicker = ["F", "AAPL", "TSLA"]; //Ford, Apple and Tesla
//##############################

//In this function we will run the scripts to gather the CIK mapping and then the ticker-submissions/descriptions
//We also measure the time - query is faster then 100ms then sleep untill 100ms are reached
async function main(download_cik_data=false, download_submissions_and_description_data=false, get_data_of_ticker = [], cik_filepath, user_agent_string) {
    let startTime;
    let endTime;
    if (download_cik_data == true) {
        startTime = performance.now();
        await downloadCikData.downloadCikDataFct(cik_create_filename=cikDataFilename, cik_data_folder=dataFolder, user_agent_string=userAgentString);
        endTime = performance.now();
        if (endTime - startTime<100) {
            await delay(100-(endTime - startTime));
        }
        console.log(String(endTime - startTime)+"ms");
    }
    if (download_submissions_and_description_data == true) {
        for (let i = 0; i < get_data_of_ticker.length; i++) {
            startTime = performance.now();
            await downloadSubmissionsData.downloadSubmissionsAndDescriptionDataFct(company_ticker=get_data_of_ticker[i], cik_filepath=cik_filepath, submissions_data_folder=dataFolder, user_agent_string=userAgentString);        
            endTime = performance.now();
            if (endTime - startTime<100) {
                await delay(100-(endTime - startTime));
            }
            console.log(String(endTime - startTime)+"ms");
        }
    }
}

main(download_cik_data=true, download_submissions_and_description_data=true, get_data_of_ticker = getDataOfTicker, cik_filepath=cikDataFilepath, user_agent_string = userAgentString);
