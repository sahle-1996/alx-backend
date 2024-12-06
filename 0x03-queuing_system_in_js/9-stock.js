#!/usr/bin/yarn dev
import express from 'express';
import { promisify } from 'util';
import { createClient } from 'redis';

const productsList = [
  {
    id: 1,
    name: 'Travel Case 250',
    cost: 50,
    initialStock: 4
  },
  {
    id: 2,
    name: 'Travel Case 450',
    cost: 100,
    initialStock: 10
  },
  {
    id: 3,
    name: 'Travel Case 650',
    cost: 350,
    initialStock: 2
  },
  {
    id: 4,
    name: 'Travel Case 1050',
    cost: 550,
    initialStock: 5
  },
];

const findProductById = (id) => {
  const product = productsList.find(item => item.id === id);

  if (product) {
    return { ...product };
  }
};

const app = express();
const redisClient = createClient();
const SERVER_PORT = 1245;

/**
 * Reserves stock for a particular product.
 * @param {number} productId - The id of the product.
 * @param {number} quantity - The stock quantity to reserve.
 */
const reserveProductStock = async (productId, quantity) => {
  return promisify(redisClient.SET).bind(redisClient)(`product.${productId}`, quantity);
};

/**
 * Fetches the reserved stock for a given product.
 * @param {number} productId - The id of the product.
 * @returns {Promise<String>}
 */
const getReservedStockForProduct = async (productId) => {
  return promisify(redisClient.GET).bind(redisClient)(`product.${productId}`);
};

app.get('/products', (_, res) => {
  res.json(productsList);
});

app.get('/products/:productId(\\d+)', (req, res) => {
  const productId = parseInt(req.params.productId, 10);
  const product = findProductById(productId);

  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }
  getReservedStockForProduct(productId)
    .then((reservedStock) => parseInt(reservedStock || 0, 10))
    .then((reservedStock) => {
      product.availableStock = product.initialStock - reservedStock;
      res.json(product);
    });
});

app.get('/reserve/:productId', (req, res) => {
  const productId = parseInt(req.params.productId, 10);
  const product = findProductById(productId);

  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }
  getReservedStockForProduct(productId)
    .then((reservedStock) => parseInt(reservedStock || 0, 10))
    .then((reservedStock) => {
      if (reservedStock >= product.initialStock) {
        res.json({ status: 'Insufficient stock available', productId });
        return;
      }
      reserveProductStock(productId, reservedStock + 1)
        .then(() => {
          res.json({ status: 'Reservation successful', productId });
        });
    });
});

const resetStockLevels = () => {
  return Promise.all(
    productsList.map(
      item => promisify(redisClient.SET).bind(redisClient)(`product.${item.id}`, 0),
    )
  );
};

app.listen(SERVER_PORT, () => {
  resetStockLevels()
    .then(() => {
      console.log(`API running on localhost port ${SERVER_PORT}`);
    });
});

export default app;
