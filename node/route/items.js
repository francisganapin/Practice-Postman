const express = require('express');
const router = express.Router();


let items = [
    {
      id: 1,
      model_name: "iPhone 15 Pro Max",
      brand_name: "Apple",
      price: 1299.00,
      stock: 30,
      created_at: "2025-08-01T10:20:00",
      updated_at: "2025-08-01T10:20:00"
    },
    {
      id: 2,
      model_name: "Galaxy S23 Ultra",
      brand_name: "Samsung",
      price: 1199.99,
      stock: 25,
      created_at: "2025-08-01T10:15:00",
      updated_at: "2025-08-01T10:15:00"
    },
    {
      id: 3,
      model_name: "Pixel 8 Pro",
      brand_name: "Google",
      price: 999.00,
      stock: 18,
      created_at: "2025-08-01T10:25:00",
      updated_at: "2025-08-01T10:25:00"
    },
    {
      id: 4,
      model_name: "Xperia 1 V",
      brand_name: "Sony",
      price: 1099.50,
      stock: 12,
      created_at: "2025-08-01T10:30:00",
      updated_at: "2025-08-01T10:30:00"
    },
    {
      id: 5,
      model_name: "Redmi Note 13 Pro",
      brand_name: "Xiaomi",
      price: 349.99,
      stock: 50,
      created_at: "2025-08-01T10:35:00",
      updated_at: "2025-08-01T10:35:00"
    }
  ];

router.get('/',(req,res) => {
    res.json(items);
});

router.post('/',(req,res) => {
    const item = req.body;
    items.push(item);
    res.status(201).json(items);
});

module.exports = router;