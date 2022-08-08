const downloadAndSaveData = require("../downloadAndSaveData_Folder/downloadAndSaveData");
const downloadAndProcessSubmissions_createParams = require("./downloadAndProcessSubmissions_createParams");
const fs = require('fs');

async function main(tickers, titles, ciks, cik_data, params_json, milliseconds_till_next_request) {
    //download data - first all main submissions, then additional ones (older ones)
    var params_submissions = downloadAndProcessSubmissions_createParams.createParamsSubmissions(tickers, titles, ciks, cik_data, params_json);
    await downloadAndSaveData.downloadAndSaveData(params_submissions, milliseconds_till_next_request);
    var params_additional_submissions = downloadAndProcessSubmissions_createParams.createParamsAdditionalSubmissions(params_submissions, params_json);
    await downloadAndSaveData.downloadAndSaveData(params_additional_submissions, milliseconds_till_next_request);
    var iterator = 0;
    for (let i = 0; i < params_submissions.special_params.ciks.length; i++) {
        main_submission = JSON.parse(fs.readFileSync(params_submissions.saving_attributes.master_folder_path[i]+params_submissions.saving_attributes.folder_name_of_file[i]+params_submissions.saving_attributes.file_name[i], "utf8"));
        // extract description about company from main submissions file
        var description_data = {
            "cik": params_submissions.special_params.ciks[i],
            "name": main_submission.name,
            "sic": main_submission.sic,
            "sicDescription": main_submission.sicDescription,
            "tickers": main_submission.tickers,
            "exchanges": main_submission.exchanges,
            "addresses": main_submission.addresses
        };
        fs.writeFileSync(params_submissions.saving_attributes.master_folder_path[i]+params_submissions.saving_attributes.folder_name_of_file[i]+"description_"+params_submissions.special_params.ciks[i]+".json", JSON.stringify(description_data));
        //create one csv out of the downloaded submissions files
        var full_json_data = {
            "0": main_submission.filings.recent
        };
        var j = 1;
        while (true) {
            if (params_submissions.special_params.ciks[i] == params_additional_submissions.special_params.ciks[iterator]) {
                full_json_data[j] = JSON.parse(fs.readFileSync(params_additional_submissions.saving_attributes.master_folder_path[iterator]+params_additional_submissions.saving_attributes.folder_name_of_file[iterator]+params_additional_submissions.saving_attributes.file_name[iterator], "utf8"));
                iterator++;
                j++;
            } else {
                break;
            }
        };
        var arr = [];
        var keys = Object.keys(full_json_data);
        var keys2 = Object.keys(full_json_data[keys[0]]);
        arr.push(keys2.map(x => '"'+x+'"'));
        for (let i = 0; i < Object.keys(full_json_data).length; i++) {
            for (let j = 0; j < full_json_data[keys[i]][keys2[0]].length; j++) {
                arr.push([]);
                for (let k = 0; k < keys2.length; k++) {
                    arr[arr.length-1].push('"'+full_json_data[keys[i]][keys2[k]][j]+'"');
                }
            }
        };
        fs.writeFileSync(params_submissions.saving_attributes.master_folder_path[i]+params_submissions.saving_attributes.folder_name_of_file[i]+"processed_submissions_data_"+params_submissions.special_params.ciks[i]+".csv", arr.join("\n"));
    }
}

var tickers = ["F", "AAPL", "TSLA"];
var titles = [];
var ciks = [];
var cik_data = "../cik_data/processed_cik_data.csv";
var params_json = "./downloadAndProcessSubmissions_Params.json";
var milliseconds_till_next_request = 100;
main(tickers, titles, ciks, cik_data, params_json, milliseconds_till_next_request);
