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


function verifyToken(req,res,next){
    const token = req.headers['authorization']?.split('')[1];
    if (!token) return res.status(403).json({message:'No token provided'});

    jwt.verify(token,JWT_SECRET,(err,decoded) =>{
        if(err) return res.status(401).json({message:'Unauthorized'});
        req.userId = decoded.id;
        next();
    });
}




app.post('/login',(req,res) => {
    const { username,password } = req.body;

    const user = users.find(u => u.username === username);
    if(!user) return res.status(404).json({message:'User not found'});

    const passwordIsValid = bcrypt.compareSync(password,user.password);
    
    });

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