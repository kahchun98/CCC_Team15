// Author: Kah
/*
 *  Importing external modules/ libraries
*/
const express = require("express");
const path = require("path");


/*
 *  App Variables
*/
const app = express();
const port = "8080";

//Imports Static fie (CSS, app logic JS, Images etc)
app.use(express.static(__dirname + '/public'));

/*
 *  Routes
*/

//Default Route
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname+'/html/webpage.html'));
});

app.get("/getjson", (req, res) => {
  res.sendFile(path.join(__dirname+'/public/json/test.json'));
});


/*
 *  Runs the web server
*/
app.listen(port, () => {
  console.log(`Listening to requests on http://localhost:${port}`);
});
