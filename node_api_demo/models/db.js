const sqlite3 = require('sqlite3').verbose();

const db = new sqlite3.Database("test.db",(err) => {
    if(err){
        console.error('failed to connect to database:',err.message);
    }else{
        console.log('Connected to SQLite database');
    }
});

module.export = db;


db.run(`
    CREATE TABLE IF NOT EXISTS items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )`);

    module.exports = db;