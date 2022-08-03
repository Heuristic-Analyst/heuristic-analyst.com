const useful_functions = require("./useful_functions");
const fs = require('fs');
const axios = require("axios");

async function downloadCikDataFct(cik_create_filename, cik_data_folder, user_agent_string) {
  const url_CikData = "https://www.sec.gov/files/company_tickers.json";
  try {
    let response = await axios.get(url_CikData, {
      headers:{
        "User-Agent":user_agent_string
      }
    });
    console.log("Log: downloaded new CIK numbers");
    // Bundle Jsons to one CSV array
    let cikDataArr = useful_functions.JsonToArrayType1(response.data, "key");
    // cik numbers need to be length 10 - filling with zeros before the gathered number -> e.g. 313807 to 0000313807
    cikNumberIndex = cikDataArr[0].indexOf("cik_str");
    // skip first row
    for (let i = 1; i < cikDataArr.length; i++) {
      cikDataArr[i][cikNumberIndex] = "0".repeat(10-String(cikDataArr[i][cikNumberIndex]).length)+String(cikDataArr[i][cikNumberIndex]);
    }
    fs.writeFileSync(cik_data_folder+cik_create_filename, useful_functions.arrayToCSV(cikDataArr, ","));
    console.log("Log: Downloaded new data:", cik_create_filename, "- saved in:", cik_data_folder);
  } catch (error) {
    console.log(error);
  }
};

//export module
module.exports = {
  downloadCikDataFct
}