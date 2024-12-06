#!/usr/bin/yarn dev
import redis from 'redis';
import { promisify } from 'util';

const redisClient = redis.createClient();

redisClient.on('error', (error) => {
  console.error(`Connection error with Redis: ${error.message}`);
});

const storeSchool = (key, value) => {
  redisClient.set(key, value, (err, res) => {
    if (err) console.error(`Error setting value for ${key}: ${err.message}`);
    else console.log(`SET operation result: ${res}`);
  });
};

const getSchoolValue = async (key) => {
  const getAsync = promisify(redisClient.get).bind(redisClient);
  try {
    const value = await getAsync(key);
    console.log(`Value for ${key}: ${value}`);
  } catch (error) {
    console.error(`Error fetching value for ${key}: ${error.message}`);
  }
};

const execute = async () => {
  await getSchoolValue('Holberton');
  storeSchool('HolbertonSanFrancisco', '100');
  await getSchoolValue('HolbertonSanFrancisco');
};

redisClient.on('ready', async () => {
  console.log('Connected to Redis successfully');
  await execute();
});
