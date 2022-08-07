const fs = require('fs');

function returnSubmissionsParams(ticker_arr, title_arr, cik_arr, save_folder_path, cik_data_file_path, encoding="utf8") {
    var cik_data = fs.readFileSync(cik_data_file_path, encoding);
    cik_data = cik_data.split('\n').map(x => x.split('","').map(element => element.replaceAll('"',"")));
    var cik_numbers_list = [];
    var host = "data.sec.gov";
    var path = "/submissions/";
    var submissionsDataObject = {
        "download_url":[],
        "folder_path":[],
        "folder_name":[],
        "file_name":[],
        "cik_number":[]
    };
    var cikIndex = cik_data[0].indexOf("cik_str");
    var tickerIndex = cik_data[0].indexOf("ticker");
    var titleIndex = cik_data[0].indexOf("title");

    for (let i = 0; i < ticker_arr.length; i++) {
        for (let j = 1; j < cik_data.length; j++) {
            if (cik_data[j][tickerIndex] == ticker_arr[i]) {
                cik_numbers_list.push(cik_data[j][cikIndex]);
            }
        }
    };
    for (let i = 0; i < title_arr.length; i++) {
        for (let j = 1; j < cik_data.length; j++) {
            if (cik_data[j][titleIndex] == title_arr[i]) {
                cik_numbers_list.push(cik_data[j][cikIndex]);
            }
        }
    };
    for (let i = 0; i < cik_arr.length; i++) {
        cik_numbers_list.push(cik_arr[i]);
    };

    for (let i = 0; i < cik_numbers_list.length; i++) {
        submissionsDataObject.download_url.push({
            "host":host,
            "path":path+"CIK"+cik_numbers_list[i]+".json",
        });
        submissionsDataObject.folder_path.push(save_folder_path);
        submissionsDataObject.folder_name.push(cik_numbers_list[i]);
        submissionsDataObject.file_name.push("original_submissions_data_"+cik_numbers_list[i]+".json");
        submissionsDataObject.cik_number.push(cik_numbers_list[i]);
    };
    return submissionsDataObject;
}

function returnAdditionalSubmissionsParams(folder_path_name, folder_name_of_file, submission_file_name, save_file_prefix, encoding="utf8") {
    var jsonData = JSON.parse(fs.readFileSync(folder_path_name+folder_name_of_file+"/"+submission_file_name, encoding));
    var additionalSubmissions = jsonData.filings.files;
    var host = "data.sec.gov";
    var path = "/submissions/";
    var submissionsDataObject = {
        "download_url":[],
        "folder_path":[],
        "folder_name":[],
        "file_name":[]
    };
    for (let i = 0; i < additionalSubmissions.length; i++) {
        submissionsDataObject.download_url.push({
            "host":host,
            "path":path+additionalSubmissions[i].name,
        });
        submissionsDataObject.folder_path.push(folder_path_name);
        submissionsDataObject.folder_name.push(folder_name_of_file);
        submissionsDataObject.file_name.push(save_file_prefix+additionalSubmissions[i].name); //"additional_submissions_data_"
    };
    return submissionsDataObject;
}

// params for https request
function returnUrlOptionsParams(user_agent) {
    var options = {
        "host":"",
        "path":"",
        "header": { "User-Agent": user_agent}
    };
    return options;
}
// params of cik_data
function returnCikDataParams(save_folder_path) {
    var cik_data = {
        "download_url":[
            {
                "host": "www.sec.gov",
                "path": "/files/company_tickers.json"
            }
        ],
        "folder_path":[save_folder_path],
        "folder_name":["cik_data"],
        "original_file_name":["original_cik_data.json"],
        "processed_file_name":["processed_cik_data.csv"]
    };
    return cik_data;
}

module.exports = {
    returnSubmissionsParams,
    returnAdditionalSubmissionsParams,
    returnUrlOptionsParams,
    returnCikDataParams
}