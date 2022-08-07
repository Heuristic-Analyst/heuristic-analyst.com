const fs = require('fs');

function makeCikDataCsv10Digits(full_file_path, encoding="utf8") {
    console.log(full_file_path);
    var cik_data = fs.readFileSync(full_file_path, encoding);
    cik_data = cik_data.split('\n').map(x => x.split('","').map(element => element.replaceAll('"',"")));
    var cikIndex = cik_data[0].indexOf("cik_str");
    for (let i = 1; i < cik_data.length; i++) {
        cik_data[i][cikIndex] = "0".repeat(10-String(cik_data[i][cikIndex]).length)+String(cik_data[i][cikIndex]);
    }
    cik_data = cik_data.map(row => {
        return row.map(x => '"'+x+'"');
    });
    fs.writeFileSync(full_file_path, cik_data.join("\n"));
}

async function JsonFileToCsvFileType1(folder_path_of_file, file_name, save_new_file_name, encoding="utf8") {
    // Type:
    // {
    //     1:{
    //         "name":"hello world",
    //         ...
    //     },
    //     2:{
    //         "name":"world hello",
    //         ...
    //     }
    // }
    var jsonData = JSON.parse(fs.readFileSync(folder_path_of_file+"/"+file_name, encoding));
    var arr = [];
    var keys = Object.keys(jsonData);
    var keys2 = Object.keys(jsonData[keys[0]]);
    arr.push(keys2.map(x => '"'+x+'"'));
    for (let i = 0; i < keys.length; i++) {
        arr.push(Object.values(jsonData[keys[i]]).map(x => '"'+x+'"'));
    };
    fs.writeFileSync(folder_path_of_file+"/"+save_new_file_name, arr.join("\n"));
    console.log(new Date(), "LOG:", "Coverted saved file: json -", file_name,"- to csv -", save_new_file_name);
};

const JsonToCsvType2 = function(json_data) {
    // Type:
    // {
    //     1:{
    //         "name":["hello world"],
    //         "abc": [...]
    //          ...
    //     },
    //     2:{
    //         "name":["world hello"],
    //         "abc": [...]
    //          ...
    //     }
    // }
    var arr = [];
    var keys = Object.keys(json_data);
    var keys2 = Object.keys(json_data[keys[0]]);
    arr.push(keys2.map(x => '"'+x+'"'));
    for (let i = 0; i < Object.keys(json_data).length; i++) {
        for (let j = 0; j < json_data[keys[i]][keys2[0]].length; j++) {
            arr.push([]);
            for (let k = 0; k < keys2.length; k++) {
                arr[arr.length-1].push('"'+json_data[keys[i]][keys2[k]][j]+'"');
            }
        }
    };
    return arr.join("\n");
};


function createSubmissionsCsvAndDescription(folder_path, folder_name, orig_subm_data_file_name, cik_number, encoding="utf8"){
    var orig_sub_data = JSON.parse(fs.readFileSync(folder_path+folder_name+"/"+orig_subm_data_file_name, encoding));
    // save description about company
    var descriptionData = {
        "cik": orig_sub_data.cik,
        "name": orig_sub_data.name,
        "sic": orig_sub_data.sic,
        "sicDescription": orig_sub_data.sicDescription,
        "tickers": orig_sub_data.tickers,
        "exchanges": orig_sub_data.exchanges,
        "addresses": orig_sub_data.addresses
    };
    fs.writeFileSync(folder_path+folder_name+"/"+"description_"+descriptionData.cik+".json", JSON.stringify(descriptionData))
    console.log(new Date(), "LOG:", "Extracted description file from submissions data -", "description_"+cik_number+".json");
    // save all filings in "filings"
    var filingsOrder = orig_sub_data.filings.files.map((x) => {
      return [new Date(x.filingFrom), "additional_submissions_data_"+x.name];
    });
    // sort dates - newest first
    filingsOrder.sort((a, b) => {
      return b[0] - a[0];
    });
    var fullJsonData = {
        "0": orig_sub_data.filings.recent
    };
    if (filingsOrder.length > 0) {
        for (let i = 0; i < filingsOrder.length; i++) {
            fullJsonData[String(i+1)] = JSON.parse(fs.readFileSync(folder_path+folder_name+"/"+filingsOrder[i][1], encoding));
        }
    }
    fs.writeFileSync(folder_path+folder_name+"/"+"processed_submissions_data_"+descriptionData.cik+".csv", JsonToCsvType2(fullJsonData));
    console.log(new Date(), "LOG:", "Extracted full submissions data -", "processed_submissions_data_"+cik_number+".csv");

}

function sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}

module.exports = {
    createSubmissionsCsvAndDescription,
    JsonFileToCsvFileType1,
    JsonToCsvType2,
    makeCikDataCsv10Digits,
    sleep
}