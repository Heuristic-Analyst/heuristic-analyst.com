const useful_functions = require("./useful_functions");
const fs = require('fs');
const axios = require("axios");

function createUrlSubmissionsData(url_cikName) {
    return "https://data.sec.gov/submissions/"+ String(url_cikName);
}

async function downloadSubmissionsAndDescriptionDataFct(company_ticker, cik_filepath, submissions_data_folder="", user_agent_string, CIK_file_encoding = "utf8") {
  try {
    // open cik mapping csv
    let CikMapping = useful_functions.CSVToArray(fs.readFileSync(cik_filepath, CIK_file_encoding));
    // find cik number of ticker in array
    let CikIndex = CikMapping[0].indexOf("cik_str");
    let tickerIndex = CikMapping[0].indexOf("ticker");
    let cikNumber = false; 
    for (let i = 1; i < CikMapping.length; i++) {
        if (CikMapping[i][tickerIndex] == company_ticker) {
          cikNumber = CikMapping[i][CikIndex];
        }
    }
    if (cikNumber != false) {
      // download submissions - recent and old ones
      let response = await axios.get(createUrlSubmissionsData("CIK"+cikNumber+".json"), {
          headers:{
          "User-Agent":user_agent_string
          }
      });
      // save description about company
      let descriptionData = {
        "cik": response.data.cik,
        "name": response.data.name,
        "sic": response.data.sic,
        "sicDescription": response.data.sicDescription,
        "tickers": response.data.tickers,
        "exchanges": response.data.exchanges,
        "addresses": response.data.addresses
      };

      // save all filings in "filings"
      let filingsDataTmp = [response.data.filings.recent];
      let filingsOrder = response.data.filings.files.map((x) => {
        return [new Date(x.filingFrom), x.name];
      });
      // sort dates - newest first
      filingsOrder.sort((a, b) => {
        return b[0] - a[0];
      });
      // download older submissions filings in order
      for (let i = 0; i < filingsOrder.length; i++) {
        response = await axios.get(createUrlSubmissionsData(filingsOrder[i][1]), {
          headers:{
            "User-Agent":user_agent_string
            }
        });
        filingsDataTmp.push(await response.data);
      }
      for (let i = 0; i < filingsDataTmp.length; i++) {
        filingsDataTmp[i] = useful_functions.JsonToArrayType2(filingsDataTmp[i]);
      }
      let filingsData = [filingsDataTmp[0][0]];
      for (let i = 0; i < filingsDataTmp.length; i++) {
        for (let j = 1; j < filingsDataTmp[i].length; j++) {
          filingsData.push(filingsDataTmp[i][j]);
        }
      }
      if (!fs.existsSync(submissions_data_folder+company_ticker)) {
        fs.mkdirSync(submissions_data_folder+company_ticker);
      }
      fs.writeFileSync(submissions_data_folder+company_ticker+"/"+company_ticker+"_SubmissionsData.csv", useful_functions.arrayToCSV(filingsData));
      fs.writeFileSync(submissions_data_folder+company_ticker+"/"+company_ticker+"_DescriptionData.json", JSON.stringify(descriptionData));
      console.log("Log: Downloaded new data:", company_ticker+"_SubmissionsData.csv and", company_ticker+"_DescriptionData.csv", "- saved in:", submissions_data_folder+company_ticker+"/");
    } else {
        console.log("Log: Could not download submissions data - ticker not found in list");
    }
  } catch (error) {
    console.log(error);
  }
};

//export module
module.exports = {
  downloadSubmissionsAndDescriptionDataFct
}