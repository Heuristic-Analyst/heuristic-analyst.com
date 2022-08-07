const createParamsForDownloadData = require("./createParamsForDownloadData");
const downloadData = require("./downloadData");
const useful_functions = require("./useful_functions");
const { performance } = require('perf_hooks');


var user_agent = "Company YourName YourEmail";
var folder_save_here = "./Example Output/";
var ticker = ["AAPL", "F"];
var title = ["Tesla, Inc."];
var ciks = ["0001067983"];
var download_new_cik_data = true;
var download_new_submissions_data = true;

async function main(download_new_cik_data, download_new_submissions_data, user_agent, folder_save_here, ticker, title, ciks) {
    var options = createParamsForDownloadData.returnUrlOptionsParams(user_agent);
    var cik_data = createParamsForDownloadData.returnCikDataParams(folder_save_here);
    var submissions_params = [ticker, title, ciks, folder_save_here, folder_save_here+cik_data.folder_name[0]+"/"+cik_data.processed_file_name[0]];
    
    let startTime;
    let endTime;
    if (download_new_cik_data == true) {
        // Cik data download: set download url (host and path) and download saving params for each iteration for each downloading file
        for (let i = 0; i < cik_data.download_url.length; i++) {
            options.host = cik_data.download_url[i].host;
            options.path = cik_data.download_url[i].path;
            startTime = performance.now();
            await downloadData.downloadData(options, cik_data.folder_path[i], cik_data.folder_name[i], cik_data.original_file_name[i]);
            // Json to Csv
            await useful_functions.JsonFileToCsvFileType1(cik_data.folder_path[i]+cik_data.folder_name[i], cik_data.original_file_name[i], cik_data.processed_file_name[i]);
            // add additional zeros to the beggining of the Cik numbers - cik needs to be 10 digits
            useful_functions.makeCikDataCsv10Digits(cik_data.folder_path[i]+cik_data.folder_name[i]+"/"+cik_data.processed_file_name[i]);
            endTime = performance.now();
            // delay script - 10 requests per second - 1 request per 100 milliseconds
            if (endTime - startTime<100) {
                await useful_functions.sleep(100-(endTime - startTime));
            }
        }
    }
    if (download_new_submissions_data == true) {
        var submissions_data = createParamsForDownloadData.returnSubmissionsParams(submissions_params[0], submissions_params[1], submissions_params[2], submissions_params[3], submissions_params[4]);
        // Submissions data download: 
        // loop through every ticker and title -> length of download_url
        for (let i = 0; i < submissions_data.download_url.length; i++) {
            //set download url (host and path)
            options.host = submissions_data.download_url[i].host;
            options.path = submissions_data.download_url[i].path;
            startTime = performance.now();
            // download each submissions data
            await downloadData.downloadData(options, submissions_data.folder_path[i], submissions_data.folder_name[i], submissions_data.file_name[i]);
            // create params with maybe additional submissions data from long ago
            var additional_submission_data = createParamsForDownloadData.returnAdditionalSubmissionsParams(submissions_data.folder_path[i], 
                submissions_data.folder_name[i],
                submissions_data.file_name[i], 
                "additional_submissions_data_");
            endTime = performance.now();
            // delay script - 10 requests per second - 1 request per 100 milliseconds
            if (endTime - startTime<100) {
                await useful_functions.sleep(100-(endTime - startTime));
            }
            // loop through additional submissions data (like before, length of download_url is length of tickers+titles)
            for (let i = 0; i < additional_submission_data.download_url.length; i++) {
                //set download url (host and path)
                options.host = additional_submission_data.download_url[i].host;
                options.path = additional_submission_data.download_url[i].path;
                startTime = performance.now();
                // download each additional submissions data
                await downloadData.downloadData(options, additional_submission_data.folder_path[i], additional_submission_data.folder_name[i], additional_submission_data.file_name[i]);
                // delay script - 10 requests per second - 1 request per 100 milliseconds
                if (endTime - startTime<100) {
                    await useful_functions.sleep(100-(endTime - startTime));
                }
            }
            // create one chronological csv with all submissions data
            useful_functions.createSubmissionsCsvAndDescription(submissions_data.folder_path[i], submissions_data.folder_name[i], submissions_data.file_name[i], submissions_data.cik_number[i]);
        }
    }
}

main(download_new_cik_data, download_new_submissions_data, user_agent, folder_save_here, ticker, title, ciks);