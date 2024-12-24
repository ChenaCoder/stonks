const connection = require('./database');
const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const app = express();
const path = require('path');
const port = 3000;

app.use(bodyParser.urlencoded({ extended: false }))

// parse application/json
app.use(bodyParser.json())
app.set('views',path.join(__dirname,'views'));
app.set('view engine','ejs');
app.engine('html',require('ejs').renderFile);

app.get('/', (req, res) => {
     
     res.render(__dirname + "/views/home.html",{data:""});
})
app.get('/style.css', (req, res) => {
     res.sendFile(__dirname + "/" + "style.css");
})
app.post('/submitFormWithPost',async (req, res) => {
     let json = req.body;
     let amt = json.inputField;
     let month = json.month;
     let date = json.date;
     let sort = json.sort;
     let column = json.column;
     
     let date1 ="mmdd"+month+date;
     
     var data;
     if(sort.length>0){
          if(column.length>0){
               
               var query;
               if(sort =="1"){
               query = `SELECT * FROM ?? ORDER BY ?? ASC LIMIT ?`
               }else{
                    query = `SELECT * FROM ?? ORDER BY ?? DESC LIMIT ?`
               }
               data = await connection.query(query,[date1,column,parseInt(amt)]);
          }
     }else{
          data = await connection.query(`SELECT * FROM ?? LIMIT ?;`,[date1,parseInt(amt)]);
     }
     console.log(data);
     res.render(__dirname + "/views/home.html", { data: data[0] });     
})
app.listen(port, () => {
     console.log(`Example app listening at http://localhost:${port}`);
})
