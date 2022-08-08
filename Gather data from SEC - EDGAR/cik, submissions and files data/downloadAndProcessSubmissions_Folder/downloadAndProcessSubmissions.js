const downloadAndSaveData = require("../downloadAndSaveData_Folder/downloadAndSaveData");
const downloadAndProcessSubmissions_createParams = require("./downloadAndProcessSubmissions_createParams");
const fs = require('fs');

async function main(tickers, titles, ciks, cik_data, params_json, milliseconds_till_next_request) {
    var unix_time_request_started = String(new Date().valueOf());
    //download data - first all main submissions, then additional ones (older ones)
    var params_submissions = downloadAndProcessSubmissions_createParams.createParamsSubmissions(tickers, titles, ciks, cik_data, params_json);
    await downloadAndSaveData.downloadAndSaveData(params_submissions, milliseconds_till_next_request);
    var params_additional_submissions = downloadAndProcessSubmissions_createParams.createParamsAdditionalSubmissions(params_submissions, params_json);
    await downloadAndSaveData.downloadAndSaveData(params_additional_submissions, milliseconds_till_next_request);
    var iterator = 0;
    for (let i = 0; i < params_submissions.special_params.ciks.length; i++) {
        main_submission = JSON.parse(fs.readFileSync(params_submissions.saving_attributes.master_folder_path[i]+params_submissions.saving_attributes.folder_name_of_file[i]+params_submissions.saving_attributes.file_name[i], "utf8"));
        //delete original (now redundant) json file
        fs.unlinkSync(params_submissions.saving_attributes.master_folder_path[i]+params_submissions.saving_attributes.folder_name_of_file[i]+params_submissions.saving_attributes.file_name[i]);
        console.log(new Date(), "LOG:", "Deleted redundant json -", params_submissions.saving_attributes.file_name[i]);
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
        console.log(new Date(), "LOG:", "Extracted company description -", "description_"+params_submissions.special_params.ciks[i]+".json");
        //create one csv out of the downloaded submissions files
        var full_json_data = {
            "0": main_submission.filings.recent
        };
        var j = 1;
        while (true) {
            if (params_submissions.special_params.ciks[i] == params_additional_submissions.special_params.ciks[iterator]) {
                full_json_data[j] = JSON.parse(fs.readFileSync(params_additional_submissions.saving_attributes.master_folder_path[iterator]+params_additional_submissions.saving_attributes.folder_name_of_file[iterator]+params_additional_submissions.saving_attributes.file_name[iterator], "utf8"));
                //delete original (now redundant) json file
                fs.unlinkSync(params_additional_submissions.saving_attributes.master_folder_path[iterator]+params_additional_submissions.saving_attributes.folder_name_of_file[iterator]+params_additional_submissions.saving_attributes.file_name[iterator]);
                console.log(new Date(), "LOG:", "Deleted redundant json -", params_additional_submissions.saving_attributes.file_name[iterator]);
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
        console.log(new Date(), "LOG:", "Extracted all submissions of company -", "processed_submissions_data_"+params_submissions.special_params.ciks[i]+".csv");
    };
    //save timepstamps of when we got submission of which cik
    var submission_timestamp_csv;
    if (fs.existsSync("./processed_submissions.csv")) {
        submission_timestamp_csv = fs.readFileSync("./processed_submissions.csv", "utf8");   
        submission_timestamp_csv = submission_timestamp_csv.split('\n').map(x => x.split('","').map(element => element.replaceAll('"',"")));         
        var cikIndex = submission_timestamp_csv[0].indexOf("cik");
        var found_cik;
        for (let i = 0; i < params_submissions.special_params.ciks.length; i++) {
            found_cik = false;
            for (let j = 0; j < submission_timestamp_csv.length; j++) {
                if (params_submissions.special_params.ciks[i] == submission_timestamp_csv[j][cikIndex]) {
                    submission_timestamp_csv.splice(j,1);
                    submission_timestamp_csv.splice( 1, 0, [unix_time_request_started, params_submissions.special_params.ciks[i]]);
                    found_cik = true;
                    break;
                }         
            }
            if (found_cik == false) {
                submission_timestamp_csv.splice( 1, 0, [unix_time_request_started, params_submissions.special_params.ciks[i]]);
            }
        }
    } else {
        submission_timestamp_csv = params_submissions.special_params.ciks;
        submission_timestamp_csv = submission_timestamp_csv.map(x => [unix_time_request_started, x]);
        submission_timestamp_csv.unshift(['timestamp_unix_submissions_got', 'cik']);   
    }
    submission_timestamp_csv = submission_timestamp_csv.map(row => {
        return row.map(x => ['"'+x+'"'])
    });
    fs.writeFileSync("./processed_submissions.csv", submission_timestamp_csv.join("\n")); 
};




var tickers = ["SNAP"];
var titles = [];
var ciks = [];
var cik_data = "../cik_data/processed_cik_data.csv";
var params_json = "./downloadAndProcessSubmissions_Params.json";
var milliseconds_till_next_request = 100;
main(tickers, titles, ciks, cik_data, params_json, milliseconds_till_next_request);
