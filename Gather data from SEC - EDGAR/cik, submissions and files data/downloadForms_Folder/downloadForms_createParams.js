const fs = require('fs');

function createParams(forms_params, cik_data_file_path, submissions_timestamps_file_path, submission_files_folder, params_file_path) {
    var params = JSON.parse(fs.readFileSync(params_file_path, "utf8"));
    var base_host = "https://www.sec.gov";
    var base_path = "/Archives/edgar/data/";
    var user_agent = {"User-Agent": "CompanyName YourName YourEmail"};


    var cik_data = fs.readFileSync(cik_data_file_path, "utf8");
    cik_data = cik_data.split('\n').map(x => x.split('","').map(element => element.replaceAll('"',"")));
    
    var cikIndex = cik_data[0].indexOf("cik_str");
    var tickerIndex = cik_data[0].indexOf("ticker");
    var titleIndex = cik_data[0].indexOf("title");

    for (let i = 0; i < forms_params.length; i++) {
        forms_params[i]["valid"] = false;
        if (forms_params[i].type == "ticker") {
            for (let j = 1; j < cik_data.length; j++) {
                if (cik_data[j][tickerIndex] == forms_params[i].id) {
                    forms_params[i].type = "cik";
                    forms_params[i].id = cik_data[j][cikIndex];
                    forms_params[i]["valid"] = true;
                    break;
                }
            }
        } else if (forms_params[i].type == "title") {
            for (let j = 1; j < cik_data.length; j++) {
                if (cik_data[j][titleIndex] == forms_params[i].id) {
                    forms_params[i].type = "cik";
                    forms_params[i].id = cik_data[j][cikIndex];
                    forms_params[i]["valid"] = true;
                    break;
                }
            }
        } else if (forms_params[i].type == "cik") {
            forms_params[i]["valid"] = true;
        }
    }
    
    var submissions_timestamps = fs.readFileSync(submissions_timestamps_file_path, "utf8");
    submissions_timestamps = submissions_timestamps.split('\n').map(x => x.split('","').map(element => element.replaceAll('"',"")));
    var cikIndexSubTimeStmp = submissions_timestamps[0].indexOf("cik");
    for (let i = 0; i < forms_params.length; i++) {
        if (forms_params[i].valid == true) {
            forms_params[i].valid = false;
            for (let j = 1; j < submissions_timestamps.length; j++) {
                if (submissions_timestamps[j][cikIndexSubTimeStmp] == forms_params[i].id) {
                    forms_params[i].valid = true;
                    break;
                }
            }
        };
        if (forms_params[i].valid == false) {
            console.log(new Date(), "LOG:", "Can not download files for CIK number", forms_params[i].id, "- no submissions data found");
        }
    }
    var submission_data;
    for (let i = 0; i < forms_params.length; i++) {
        if (forms_params[i].valid == true) {
            for (let j = 0; j < forms_params[i].form.length; j++) {
                submission_data = fs.readFileSync(submission_files_folder+forms_params[i].id+"/"+"processed_submissions_data_"+forms_params[i].id+".csv", "utf8");
                submission_data = submission_data.split('\n').map(x => x.split('","').map(element => element.replaceAll('"',"")));
                var formIndex = submission_data[0].indexOf("form");
                var filingDateIndex = submission_data[0].indexOf("filingDate");
                var accessionNumberIndex = submission_data[0].indexOf("accessionNumber");        
                if ("filing_date" in forms_params[i]) {
                    for (let k = 1; k < submission_data.length; k++) {
                        if (submission_data[k][filingDateIndex] == forms_params[i].filing_date[j] && submission_data[k][formIndex] == forms_params[i].form[j]) {
                            if (!fs.existsSync(params.saving_attributes.master_folder_path[0]+forms_params[i].id+"/"+forms_params[i].form[j]+"/"+submission_data[k][accessionNumberIndex]+".txt")) {
                                params.url_attributes.host.push(base_host);
                                params.url_attributes.path.push(base_path+forms_params[i].id+"/"+submission_data[k][accessionNumberIndex].replaceAll("-","")+"/"+submission_data[k][accessionNumberIndex]+".txt");
                                params.url_attributes.headers.push(user_agent);
                                params.saving_attributes.master_folder_path.push(params.saving_attributes.master_folder_path[0]);
                                params.saving_attributes.folder_name_of_file.push(forms_params[i].id+"/"+forms_params[i].form[j]+"/");
                                params.saving_attributes.file_name.push(submission_data[k][accessionNumberIndex]+".txt");
                            }   
                        }
                    }
                } else if ("filings_date_range" in forms_params[i]) {
                    forms_params[i].filings_date_range[j].filing_date_including_from = new Date(forms_params[i].filings_date_range[j].filing_date_including_from);
                    forms_params[i].filings_date_range[j].filing_date_including_to = new Date(forms_params[i].filings_date_range[j].filing_date_including_to);
                    for (let k = 1; k < submission_data.length; k++) {
                        if (forms_params[i].filings_date_range[j].filing_date_including_from <= new Date(submission_data[k][filingDateIndex]) && forms_params[i].filings_date_range[j].filing_date_including_to >= new Date(submission_data[k][filingDateIndex])) {
                            if (submission_data[k][formIndex] == forms_params[i].form[j]) {
                                if (!fs.existsSync(params.saving_attributes.master_folder_path[0]+forms_params[i].id+"/"+forms_params[i].form[j]+"/"+submission_data[k][accessionNumberIndex]+".txt")) {
                                    params.url_attributes.host.push(base_host);
                                    params.url_attributes.path.push(base_path+forms_params[i].id+"/"+submission_data[k][accessionNumberIndex].replaceAll("-","")+"/"+submission_data[k][accessionNumberIndex]+".txt");
                                    params.url_attributes.headers.push(user_agent);
                                    params.saving_attributes.master_folder_path.push(params.saving_attributes.master_folder_path[0]);
                                    params.saving_attributes.folder_name_of_file.push(forms_params[i].id+"/"+forms_params[i].form[j]+"/");
                                    params.saving_attributes.file_name.push(submission_data[k][accessionNumberIndex]+".txt");
                                }
                            }
                        }
                    }
                } else {
                    for (let k = 1; k < submission_data.length; k++) {
                        if (submission_data[k][formIndex] == forms_params[i].form[j]) {
                            if (!fs.existsSync(params.saving_attributes.master_folder_path[0]+forms_params[i].id+"/"+forms_params[i].form[j]+"/"+submission_data[k][accessionNumberIndex]+".txt")) {
                                params.url_attributes.host.push(base_host);
                                params.url_attributes.path.push(base_path+forms_params[i].id+"/"+submission_data[k][accessionNumberIndex].replaceAll("-","")+"/"+submission_data[k][accessionNumberIndex]+".txt");
                                params.url_attributes.headers.push(user_agent);
                                params.saving_attributes.master_folder_path.push(params.saving_attributes.master_folder_path[0]);
                                params.saving_attributes.folder_name_of_file.push(forms_params[i].id+"/"+forms_params[i].form[j]+"/");
                                params.saving_attributes.file_name.push(submission_data[k][accessionNumberIndex]+".txt");
                            }
                        }
                    }
                }
            }
        }
    }
    return params;
}

module.exports = {
    createParams
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
createParams(forms_to_get,cik_data, submissions_timestamps_file_path, submission_files_folder, params_json);