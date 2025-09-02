const express =require('express');
const app = express();
app.use(express.json());



const itemsRoutes = require('./route/items');

app.use('/items',itemsRoutes);

app.listen(3000,() => console.log('Server running on port 3000'));