#!/usr/bin/yarn dev
import redis from 'redis';

const redisClient = redis.createClient();

redisClient.on('error', (error) => {
  console.error(`Unable to connect to Redis: ${error.message}`);
});

redisClient.on('ready', () => {
  console.log('Successfully connected to the Redis server');
});

const addSchool = (key, value) => {
  redisClient.set(key, value, (err, res) => {
    if (err) console.error(err.message);
    else console.log(`SET operation successful: ${res}`);
  });
};

const fetchSchool = (key) => {
  redisClient.get(key, (error, result) => {
    if (error) console.error(`GET operation failed: ${error.message}`);
    else console.log(`Value retrieved: ${result}`);
  });
};

fetchSchool('Holberton');
addSchool('HolbertonSanFrancisco', '100');
fetchSchool('HolbertonSanFrancisco');
