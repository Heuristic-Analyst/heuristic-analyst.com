const downloadAndSaveData = require("../downloadAndSaveData_Folder/downloadAndSaveData");
const downloadForms_createParams = require("./downloadForms_createParams");
const fs = require('fs');

async function main(forms_to_get,cik_data, submissions_timestamps_file_path, submission_files_folder, params_json, milliseconds_till_next_request) {
    //download data
    var params = downloadForms_createParams.createParams(forms_to_get,cik_data, submissions_timestamps_file_path, submission_files_folder, params_json);
    await downloadAndSaveData.downloadAndSaveData(params, milliseconds_till_next_request);
}


var forms_to_get = [
    {
        "type":"ticker",
        "id":"AAPL",
        "form":["10-Q", "8-K"],
        "filing_date":["2022-07-29", "2010-03-12"],
    },
    {
        "type":"title",
        "id":"Tesla, Inc.",
        "form":["10-Q"],
        "filings_date_range":[{
            "filing_date_including_from":"2021-07-30",
            "filing_date_including_to":"2022-07-30"
        }]
    },
    {
        "type":"ticker",
        "id":"SNAP",
        "form":["10-K"]
    },
];

var cik_data = "../cik_data/processed_cik_data.csv";
var submissions_timestamps_file_path = "../downloadAndProcessSubmissions_Folder/processed_submissions.csv";
var submission_files_folder = "../"
var params_json = "./downloadForms_Params.json";
main(forms_to_get,cik_data, submissions_timestamps_file_path, submission_files_folder, params_json);