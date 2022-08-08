const downloadAndSaveData = require("../downloadAndSaveData_Folder/downloadAndSaveData");
const downloadAndProcessCiks_createParams = require("./downloadAndProcessCiks_createParams");
const fs = require('fs');

async function main(params_json, milliseconds_till_next_request) {
    //download data
    var params = downloadAndProcessCiks_createParams.createParams(params_json);
    await downloadAndSaveData.downloadAndSaveData(params, milliseconds_till_next_request);
    try {
        //convert downloaded json to csv
        var jsonData = JSON.parse(fs.readFileSync(params.saving_attributes.master_folder_path[0]+params.saving_attributes.folder_name_of_file[0]+params.saving_attributes.file_name[0], "utf8"));
        var arr = [];
        var keys = Object.keys(jsonData);
        var keys2 = Object.keys(jsonData[keys[0]]);
        arr.push(keys2);
        for (let i = 0; i < keys.length; i++) {
            arr.push(Object.values(jsonData[keys[i]]));
        };
        //add zeros to make ciks 10 digit long
        var cikIndex = arr[0].indexOf("cik_str");
        for (let i = 1; i < arr.length; i++) {
            arr[i][cikIndex] = "0".repeat(10-String(arr[i][cikIndex]).length)+String(arr[i][cikIndex]);
        }
        //add quotation marks to each element in csv
        arr = arr.map(row => {
            return row.map(x => '"'+x+'"');
        });
        //save csv
        fs.writeFileSync(params.saving_attributes.master_folder_path[0]+params.saving_attributes.folder_name_of_file[0]+params.special_params.processed_file_name[0], arr.join("\n"));
        console.log(new Date(), "LOG:", "Converted json -", params.saving_attributes.file_name[0],"- to csv -", params.special_params.processed_file_name[0]);
        //delete original (now redundant) json file
        fs.unlinkSync(params.saving_attributes.master_folder_path[0]+params.saving_attributes.folder_name_of_file[0]+params.saving_attributes.file_name[0]);
        console.log(new Date(), "LOG:", "Deleted redundant json -", params.saving_attributes.file_name[0]);
    } catch (error) {
        console.log(new Date(), "LOG:", "Something went wrong converting ", params.special_params.processed_file_name[0], "to csv");
    }    
}

var params_json = "./downloadAndProcessCiks_Params.json";
var milliseconds_till_next_request = 100;
main(params_json, milliseconds_till_next_request);