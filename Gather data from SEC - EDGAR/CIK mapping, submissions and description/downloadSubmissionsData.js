const useful_functions = require("./useful_functions");
const fs = require('fs');
const axios = require("axios");

function createUrlSubmissionsData(url_cikName) {
    return "https://data.sec.gov/submissions/"+ String(url_cikName);
}

async function downloadSubmissionsAndDescriptionDataFct(ticker_or_title, company_ticker_or_title, cik_data_filepath, submissions_data_folder="", user_agent_string, CIK_file_encoding = "utf8") {
  try {
    // open cik mapping csv
    let cikMapping = useful_functions.CSVToArray(fs.readFileSync(cik_data_filepath, CIK_file_encoding));
    // find cik number of ticker in array
    let cikNumberIndex = cikMapping[0].indexOf("cik_str");
    let titleIndex = cikMapping[0].indexOf("title");
    let tickerOrTitleIndex = cikMapping[0].indexOf(ticker_or_title);
    let cikNumber = false;
    let title = false;

    for (let i = 1; i < cikMapping.length; i++) {
      if (cikMapping[i][tickerOrTitleIndex] == company_ticker_or_title) {
        cikNumber = cikMapping[i][cikNumberIndex];
        title = cikMapping[i][titleIndex];
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
      if (!fs.existsSync(submissions_data_folder+cikNumber)) {
        fs.mkdirSync(submissions_data_folder+cikNumber);
      }
      fs.writeFileSync(submissions_data_folder+cikNumber+"/"+cikNumber+"_SubmissionsData.csv", useful_functions.arrayToCSV(filingsData));
      fs.writeFileSync(submissions_data_folder+cikNumber+"/"+cikNumber+"_DescriptionData.json", JSON.stringify(descriptionData));
      console.log("Log: Downloaded new data of:", title)
      console.log("     Saved in:", submissions_data_folder+cikNumber+"/", "- Saved as:" , cikNumber+"_SubmissionsData.csv and", cikNumber+"_DescriptionData.csv");
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