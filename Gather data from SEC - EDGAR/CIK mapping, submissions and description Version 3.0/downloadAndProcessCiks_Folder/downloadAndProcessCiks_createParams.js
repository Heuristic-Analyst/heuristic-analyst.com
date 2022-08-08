const fs = require('fs');

function createParams(params_file_path) {
    var params = JSON.parse(fs.readFileSync(params_file_path, "utf8"));
    return params;
}

module.exports = {
    createParams
}