const fs = require('fs');
const mariadb = require("mariadb");
//####################


function JsonArrayToCSV(arr){
    var keys = Object.keys(arr[0]);
    var csv = [];
    var tmp = "";
    for (let j = 0; j < keys.length; j++) {
        if (j == 0) {
            tmp = String(keys[j]);
        } else {
            tmp = tmp + ", " + String(keys[j]);
        }
    }
    csv.push(tmp);
    for (let j = 0; j < arr.length; j++) {
        for (let k = 0; k < keys.length; k++) {
            if (k == 0) {
                tmp = String(arr[j][keys[k]]);
            } else {
                tmp = tmp + ", " + String(arr[j][keys[k]]);
            }
        }
        csv.push(tmp);
    }
    csv = csv.join('\n');
    return csv;
}


//####################
async function main() {
    var conn;
    try {
        // connect to mariadb using the hostname and our login data
        var pool = mariadb.createPool({
            host: "localhost", 
            user:"root", 
            password: "1234"
        });
        conn = await pool.getConnection();
        await conn.query("use cryptodb;");
        tables = await conn.query("SHOW TABLES");
        for (let i = 0; i < tables.length; i++) {
            var tmpData = await conn.query("SELECT * FROM " + tables[i]["Tables_in_cryptodb"]);
            var csv = JsonArrayToCSV(tmpData);
            fs.writeFileSync("table"+tables[i]["Tables_in_cryptodb"]+".csv", csv);
        }
        pool.end();
        conn.end();
    } catch (err) {
        console.log("Something went wrong (export data)");
        console.log(err);
        pool.end();
        conn.end();
    }
}

main();
