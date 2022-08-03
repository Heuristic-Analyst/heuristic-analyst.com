const downloadCikData = require("./downloadCikData");
const downloadSubmissionsData = require("./downloadSubmissionsData");
const { performance } = require('perf_hooks');

//##############################
let params = {  
    "downloadNewCikData": true,
    "downloadSubmissionsAndDescriptionData": true,
    "saveDataToFolder": "",
    "cikDataFileName": "CikData.csv",
    "cikDataFilePath": "CikData.csv",
    "userAgentString": "Company Name Email",
    "getDataOfTickerAndTitle": { //accepts ticker and titles
        "ticker":   ["F", "AAPL"], 
        "title":    ["Tesla, Inc.", "TAIWAN SEMICONDUCTOR MANUFACTURING CO LTD", "DANAHER CORP /DE/"]
    }
};
//##############################

//In this function we will run the scripts to gather the CIK mapping and then the ticker-submissions/descriptions
//We also measure the time - query is faster then 100ms then sleep untill 100ms are reached
async function main(params) {
    let startTime;
    let endTime;
    if (params.downloadNewCikData == true) {
        startTime = performance.now();
        await downloadCikData.downloadCikDataFct(params.cikDataFileName, params.saveDataToFolder, params.userAgentString);
        endTime = performance.now();
        if (endTime - startTime<100) {
            await delay(100-(endTime - startTime));
        }
        console.log("Log: it took", String(endTime - startTime)+"ms");
    }
    if (params.downloadSubmissionsAndDescriptionData == true) {
        //If array exists and is not empty
        if (Array.isArray(params.getDataOfTickerAndTitle.ticker) && params.getDataOfTickerAndTitle.ticker.length) {
            for (let i = 0; i < params.getDataOfTickerAndTitle.ticker.length; i++) {
                startTime = performance.now();
                await downloadSubmissionsData.downloadSubmissionsAndDescriptionDataFct("ticker", params.getDataOfTickerAndTitle.ticker[i], params.cikDataFilePath, params.saveDataToFolder, params.userAgentString);        
                endTime = performance.now();
                if (endTime - startTime<100) {
                    await delay(100-(endTime - startTime));
                }
                console.log("Log: it took", String(endTime - startTime)+"ms");
            }    
        }
        if (Array.isArray(params.getDataOfTickerAndTitle.title) && params.getDataOfTickerAndTitle.title.length) {
            for (let i = 0; i < params.getDataOfTickerAndTitle.title.length; i++) {
                startTime = performance.now();
                await downloadSubmissionsData.downloadSubmissionsAndDescriptionDataFct("title", params.getDataOfTickerAndTitle.title[i], params.cikDataFilePath, params.saveDataToFolder, params.userAgentString);        
                endTime = performance.now();
                if (endTime - startTime<100) {
                    await delay(100-(endTime - startTime));
                }
                console.log("Log: it took", String(endTime - startTime)+"ms");
            }    
        }
    }
}

main(params);
