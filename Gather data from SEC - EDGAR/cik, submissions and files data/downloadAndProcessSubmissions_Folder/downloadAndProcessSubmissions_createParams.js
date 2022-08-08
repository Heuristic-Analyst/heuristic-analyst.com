const fs = require('fs');

function createParamsSubmissions(tickers, titles, ciks, cik_data_file_path, params_file_path) {
    var base_host = "https://data.sec.gov";
    var base_path = "/submissions/";
    var user_agent = {"User-Agent": "UniversityResearch Timur t.oezsoy@t-online.de"};
    var original_file_prefix = "original_submissions_data_";
    var params = JSON.parse(fs.readFileSync(params_file_path, "utf8"));

    var cik_data = fs.readFileSync(cik_data_file_path, "utf8");
    cik_data = cik_data.split('\n').map(x => x.split('","').map(element => element.replaceAll('"',"")));
    
    var cikIndex = cik_data[0].indexOf("cik_str");
    var tickerIndex = cik_data[0].indexOf("ticker");
    var titleIndex = cik_data[0].indexOf("title");

    for (let i = 0; i < tickers.length; i++) {
        for (let j = 1; j < cik_data.length; j++) {
            if (cik_data[j][tickerIndex] == tickers[i]) {
                ciks.unshift(cik_data[j][cikIndex]);
                break;
            }
        }
    };
    for (let i = 0; i < titles.length; i++) {
        for (let j = 1; j < cik_data.length; j++) {
            if (cik_data[j][titleIndex] == titles[i]) {
                ciks.unshift(cik_data[j][cikIndex]);
                break;
            }
        }
    };

    params.special_params.ciks = ciks;

    for (let i = 0; i < ciks.length; i++) {
        params.url_attributes.host.push(base_host);
        params.url_attributes.path.push(base_path+"CIK"+ciks[i]+".json");
        params.url_attributes.headers.push(user_agent);
        params.saving_attributes.master_folder_path.push(params.saving_attributes.master_folder_path[0]);
        params.saving_attributes.folder_name_of_file.push(ciks[i]+"/");
        params.saving_attributes.file_name.push(original_file_prefix+ciks[i]+".json");
    }
    return params;
}

function createParamsAdditionalSubmissions(original_submissions_params, params_file_path) {
    var base_host = "https://data.sec.gov";
    var base_path = "/submissions/";
    var user_agent = {"User-Agent": "CompanyName YourName YourEmail"};
    var original_file_prefix = "original_additional_submissions_data_";
    var params = JSON.parse(fs.readFileSync(params_file_path, "utf8"));
    var original_submission;
    var additional_submissions_files;
    //iterate through every submission file
    for (let i = 0; i < original_submissions_params.special_params.ciks.length; i++) {
        //get downloaded submission file i
        original_submission = JSON.parse(fs.readFileSync(original_submissions_params.saving_attributes.master_folder_path[i]+original_submissions_params.saving_attributes.folder_name_of_file[i]+original_submissions_params.saving_attributes.file_name[i], "utf8"));
        //get additional filings file names and their corresponding dates
        additional_submissions_files = original_submission.filings.files.map(x => {
            return [new Date(x.filingTo), x.name];
        });
        //sort dates (will sort filings)
        additional_submissions_files.sort((a, b) => {
            return b[0] - a[0];
        });
        for (let j = 0; j < additional_submissions_files.length; j++) {
            params.url_attributes.host.push(base_host);
            params.url_attributes.path.push(base_path+additional_submissions_files[j][1]);
            params.url_attributes.headers.push(user_agent);
            params.saving_attributes.master_folder_path.push(params.saving_attributes.master_folder_path[0]);
            params.saving_attributes.folder_name_of_file.push(original_submissions_params.special_params.ciks[i]+"/");
            params.saving_attributes.file_name.push(original_file_prefix+additional_submissions_files[j][1]);
            params.special_params.ciks.push(original_submissions_params.special_params.ciks[i]);
        }
    }
    return params;
}

module.exports = {
    createParamsSubmissions,
    createParamsAdditionalSubmissions
}