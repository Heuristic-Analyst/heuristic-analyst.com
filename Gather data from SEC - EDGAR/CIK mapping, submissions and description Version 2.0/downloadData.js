const fs = require('fs');
const axios = require("axios");

async function downloadData(url_options, saving_folder_path, saving_folder_name, saving_file_name) {
  try {
    const url_CikData = "https://www.sec.gov/files/company_tickers.json";
    if (!fs.existsSync(saving_folder_path+saving_folder_name)) {
      fs.mkdirSync(saving_folder_path+saving_folder_name);
    }
    let response = await axios.get("https://"+url_options.host+url_options.path, {
      headers:
        url_options.header
    });
    fs.writeFileSync(saving_folder_path+saving_folder_name+"/"+saving_file_name, JSON.stringify(response.data));
    console.log(new Date(), "LOG:", "Download Completed", saving_file_name, "- Saving path:", saving_folder_path+saving_folder_name+"/");
  } catch (error) {
    console.log(new Date(), "LOG:", "Something went wrong downloading", saving_file_name, "- Saving path:", saving_folder_path+saving_folder_name+"/");
  }
}

module.exports = {
  downloadData
}
