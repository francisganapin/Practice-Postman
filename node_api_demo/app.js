const express = require('express');
const app = express();
const itemRoutes = require('./routes/itemsRoutes');


app.use(express.json());


app.use('/api/items',itemRoutes);

app.listen(3000,() => console.log('Server running on port 3000'));