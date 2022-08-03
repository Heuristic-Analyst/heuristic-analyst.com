const JsonToArrayType1 = function(jsonData, OuterKeysName) {
    // Type: -> 1 and 2 is OuterKey
    // {
    //     1:{
    //         "name":"hello world",
    //         ...
    //     },
    //     2:{
    //         ...
    //     }
    // }
    let arr = [];
    let keys = Object.keys(jsonData);
    let keys2 = Object.keys(jsonData[keys[0]]);
    arr.push([OuterKeysName]);
    arr[0] = arr[0].concat(keys2);
    for (let i = 0; i < keys.length; i++) {
        arr.push([keys[i]]);
        arr[i+1] = arr[i+1].concat(Object.values(jsonData[keys[i]]));
    }
    return arr;
};

const JsonToArrayType2 = function(jsonData) {
    // Type:
    // {
    //     "name":[...],
    //     "year":[...],
    //     "xyz": [...],
    // }
    let arr = [];
    let keys = Object.keys(jsonData);
    arr.push(keys);
    for (let i = 0; i < jsonData[keys[0]].length; i++) {
        arr.push([]);
        for (let j = 0; j < keys.length; j++) {
            arr[i+1].push(jsonData[keys[j]][i]);
        }
    }
    return arr;
};


const arrayToCSV = function(arr) {
    let csv = arr.map(v => 
        v.map(x => '"'+x+'"').join(",")
        )
        .join("\n");
    return csv;
};


const CSVToArray = function(csv) {
    let arr = csv.split('\n').map(x => x.split('","').map(element =>
        element.replaceAll('"',"")));
    return arr;
};


//export modules
module.exports = {
    JsonToArrayType1,
    JsonToArrayType2,
    arrayToCSV,
    CSVToArray
}