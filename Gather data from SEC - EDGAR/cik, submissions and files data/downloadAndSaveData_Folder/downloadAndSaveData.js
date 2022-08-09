const fs = require('fs');
const axios = require("axios");
const { performance } = require('perf_hooks');

async function downloadAndSaveData(params, milliseconds_till_next_request) {
  try {
    var startTime;
    var endTime;
    for (let i = 0; i < params.url_attributes.host.length; i++) {
      startTime = performance.now();
      if (!fs.existsSync(params.saving_attributes.master_folder_path[i]+params.saving_attributes.folder_name_of_file[i])) {
        fs.mkdirSync(params.saving_attributes.master_folder_path[i]+params.saving_attributes.folder_name_of_file[i]);
      }
      let response = await axios.get(params.url_attributes.host[i]+params.url_attributes.path[i], {
        headers: params.url_attributes.headers[i]
      });
      fs.writeFileSync(params.saving_attributes.master_folder_path[i]+params.saving_attributes.folder_name_of_file[i]+params.saving_attributes.file_name[i], JSON.stringify(response.data));
      console.log(new Date(), "LOG:", "Download completed of", params.saving_attributes.file_name[i]);
      endTime = performance.now();
      if (endTime - startTime < milliseconds_till_next_request) {
        await sleep(100-(endTime - startTime));
    }
    }
  } catch (error) {
    console.log("----------------");
    console.log(new Date(), "LOG:", "Something went wrong downloading", params.saving_attributes.file_name[i]);
    console.log("This were the params:");
    console.log(params);
    console.log("----------------");
  }
}

function sleep(milliseconds) {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}

module.exports = {
    downloadAndSaveData
}
