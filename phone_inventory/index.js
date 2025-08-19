const express = require('express');
const axios = require('axios');


const app = express();
const PORT = 5000;



app.get('brands',async(req,res) => {
    try{
        const response = await axios.get("http://127.0.0.1:8000/api/brands/");
        res.json(response.data);
    }catch(error){
        res.status(500).json({error:error.message});
    }
});


app.get('/phones',async(req,res) =>{
    try{
        const response = await axios.get("http://127.0.0.1:8000/api/phones/");
        res.json(response.data);
    }catch (error){
        res.status(500).json({error:error.message});
    }
});


app.listen(PORT, () => {
    console.log(`Node.js server running at http://localhost:${PORT}`);
  });