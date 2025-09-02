const express = require('express');
const app = express();


app.use(express.json());

app.get('/hello',(req,res) =>{
    res.json({'message':'Hello Api'});
});


app.post('/add',(req,res) =>{
    res.json({data:req.body});
});


app.listen(3000,() => console.log('Api running on http://localhost:3000'));