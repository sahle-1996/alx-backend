#!/usr/bin/yarn dev
import { createClient as connectRedis } from 'redis';

const redisClient = connectRedis();
const TERMINATION_MESSAGE = 'STOP_SERVER';

redisClient.on('error', (error) => {
  console.error('Failed to connect to Redis:', error.message);
});

redisClient.on('connect', () => {
  console.log('Connected to Redis successfully');
});

redisClient.subscribe('education channel');

redisClient.on('message', (_error, message) => {
  console.log(message);
  if (message === TERMINATION_MESSAGE) {
    redisClient.unsubscribe();
    redisClient.quit();
  }
});
