const db = require('../models/db');

exports.getItems = async(req,res) =>{
    try {
        const [rows] = await db.query('SELECT * FROM items');
        res.json(rows);
    }catch(err){
        res.status(500),json({error:err.message});
    }
};

// add item
exports.createItem = async(req,res) =>{
    try{
        const {name,price,stock} = req.body;
        const [result] = await db.query(
            'INSERT INTO items (name,price,stock) VALUES (?,?,?)',
            [name,price,stock]
        );
        res.status(201).json({id:result.insertID,name,price,stock});
    }catch(err){
        res.status(500).json({error:err.messa});
    }
};