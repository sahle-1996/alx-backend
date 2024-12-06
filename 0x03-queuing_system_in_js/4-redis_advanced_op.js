#!/usr/bin/yarn dev
import { createClient as redisConnect, print as redisPrint } from 'redis';

const redisClient = redisConnect();

redisClient.on('error', (error) => {
  console.error('Unable to connect to Redis server:', error.message);
});

const setHashField = (hash, key, value) => {
  redisClient.HSET(hash, key, value, redisPrint);
};

const displayHash = (hash) => {
  redisClient.HGETALL(hash, (_error, result) => console.log(result));
};

const execute = () => {
  const locations = {
    Portland: 50,
    Seattle: 80,
    'New York': 20,
    Bogota: 20,
    Cali: 40,
    Paris: 2,
  };
  for (const [key, value] of Object.entries(locations)) {
    setHashField('SchoolLocations', key, value);
  }
  displayHash('SchoolLocations');
};

redisClient.on('connect', () => {
  console.log('Connected to Redis successfully');
  execute();
});
