const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

const app = express();
const PORT = 3000;

app.use(express.json());


let users = [
    {
        id:1,
        username:'francis',
        password:bcrypt.hashSync('mypassword',8)
    }
];






app.get('/',(req,res) => {
   res.send('Welcome to my Node.js') 
});


app.post('/products',(req,res) =>{
    const newProduct = req.body;
    res.status(201).json({'message':'Product added',product:newProduct});
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
  });