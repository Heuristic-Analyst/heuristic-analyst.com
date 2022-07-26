//####################
// import library to connect with mariadb
const mariadb = require("mariadb");
//####################

//####################
async function createDB() {
    var conn;
    try {
        // connect to mariadb using the hostname and our login data
        var pool = mariadb.createPool({
            host: "localhost", 
            user:"root", 
            password: "1234"
        });

        conn = await pool.getConnection();
        // create the database
        await conn.query("DROP DATABASE IF EXISTS cryptodb;");
        await conn.query("CREATE DATABASE cryptodb;");
        // in the created database: create tables "symbols" and "trades"
        await conn.query("use cryptodb;");
        await conn.query("CREATE TABLE symbols(\
            ID INT(11) NOT NULL AUTO_INCREMENT,\
            Name VARCHAR(50),\
            PRIMARY KEY (ID)\
            )\
            engine=innodb\
            DEFAULT CHARACTER SET = utf8;");
        await conn.query("CREATE TABLE trades(\
            ID INT(11) NOT NULL AUTO_INCREMENT,\
            SymbolID INT(11) NOT NULL,\
            EventTime BIGINT(11) NOT NULL,\
            Price FLOAT(11, 6) NOT NULL,\
            Quantity FLOAT(11, 6) NOT NULL,\
            TradeTime BIGINT(11) NOT NULL,\
            PRIMARY KEY (ID),\
            CONSTRAINT fk_SymbolID\
            FOREIGN KEY (SymbolID) REFERENCES Symbols (ID)\
            ON DELETE NO ACTION\
            ON UPDATE NO ACTION\
            )\
            engine=innodb\
            DEFAULT CHARACTER SET = utf8;");
        pool.end();
        conn.end();
    } catch {
        console.log("Something went wrong (creating database)");
        console.log(err);
        pool.end();
        conn.end();
    }
}
//####################

//####################
async function insertData(trades, n) {
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

        // insert every trade
        for (let i = 0; i < trades.length; i++) {
            // get symbol name id - if not existing -> create it
            var SymbolIDQuery = await conn.query("SELECT ID FROM symbols WHERE Name='"+String(trades[i]["s"])+"';");
            if (SymbolIDQuery.length == 1) {
                SymbolIDQuery = SymbolIDQuery[0]["ID"];
            } else {
                await conn.query("INSERT INTO symbols (Name) VALUES ('"+String(trades[i]["s"])+"');");
                SymbolIDQuery = await conn.query("SELECT ID FROM symbols WHERE Name='"+String(trades[i]["s"])+"';");
                SymbolIDQuery = SymbolIDQuery[0]["ID"];
                console.log("New entry in symbols: " + String(trades[i]["s"]));
            }
            // create insert sql query
            var sqlQueryValues = "(" + String(SymbolIDQuery);
            sqlQueryValues = sqlQueryValues + ", " + String(trades[i]["E"]);
            sqlQueryValues = sqlQueryValues + ", " + String(trades[i]["p"]);
            sqlQueryValues = sqlQueryValues + ", " + String(trades[i]["q"]);
            sqlQueryValues = sqlQueryValues + ", " + String(trades[i]["T"]);
            sqlQueryValues = sqlQueryValues + ")";
            sqlQuery = "INSERT INTO trades (SymbolID, EventTime, Price, Quantity, TradeTime) VALUES " + sqlQueryValues;
            await conn.query(sqlQuery);
            
        trades.splice(0, n);
        }
        pool.end();
        conn.end();
    } catch (err) {
        console.log("Something went wrong (insert data)");
        console.log(err);
        pool.end();
        conn.end();
    }
}
//###################################################################

//###################################################################
// import ws library
const WebSocket = require("ws");
//####################

//####################
// log date and time when program started
var date = new Date();
console.log(`${date.toGMTString()} | Program started`);
//####################

//####################
// save last n (maxNEntries) trades to this array
let tradesData = []
let maxNEntries = 1000
//####################

//####################
async function RunWebsocketBinance() {
  // Create an array with our streams which we want to get from Binance and connect to the Binance Websocket
  // With the '.join("/")' we can join the elements of the array to a single string seperated by "/"
  const streamsBinance = ["btcusdt@trade", "ethusdt@trade"];
  var wsBinance = new WebSocket("wss://fstream.binance.com/stream?streams="+streamsBinance.join("/"));
  //####################

  //####################
  // There are different actions this websocket client can have: 
  // When establishing the connection -> "open"
  // When retrieving a message from binance -> "message"
  // To keep the connection alive -> "ping" and "pong"
  // -> https://www.npmjs.com/package/ws: Pong messages are automatically sent in response to ping messages as required by the spec
  // all the work after each action is done in their functions
  wsBinance.on("open", function openWsBinance() {
    console.log(`${date.toGMTString()} | Connected to Binance Websocket`);
  });

  wsBinance.on("message", function incomingWsBinance(data) {
    //console.log(tradesData.length);//data.toString());
    tradesData.push(JSON.parse(data.toString())["data"]);
    // when we collected 1000 messages -> write them into our sql db and empty the messages array
    if (tradesData.length == maxNEntries) {
      insertData(tradesData, maxNEntries);
    }
  });

  wsBinance.on("ping", function heartbeatWsBinance() {
    date = new Date();
    console.log(`${date.toGMTString()} | Got a Ping from Binance | Pong has been sent automatically`);
  });

  wsBinance.on("pong", function heartbeatWsBinance() {
    date = new Date();
    console.log(`${date.toGMTString()} | Got a Pong from Binance`);
  });
}
//####################

//####################
async function main() {
  await createDB();
  RunWebsocketBinance();
}
//####################

//####################
main()
//####################

