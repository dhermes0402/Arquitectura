const express = require('express');
const mysql = require('mysql');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const db = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME_SHOP,
});

app.use(async (req, res, next) => {
  const token = req.headers.authorization;
  if (!token) return res.status(401).send('Unauthorized');
  try {
    const response = await axios.get(`${process.env.LOGIN_SERVICE}/check`, {
      headers: { Authorization: token }
    });
    if (!response.data.valid) return res.status(401).send('Unauthorized');
    next();
  } catch {
    res.status(401).send('Unauthorized');
  }
});

app.get('/products', (req, res) => {
  db.query('SELECT * FROM products', (err, results) => {
    if (err) throw err;
    res.json(results);
  });
});

app.get('/products/:id', (req, res) => {
  const { id } = req.params;
  db.query('SELECT * FROM products WHERE id = ?', [id], (err, results) => {
    if (err) throw err;
    res.json(results[0]);
  });
});

app.listen(5001, () => {
  console.log('API running on port 5001');
});
