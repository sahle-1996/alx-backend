#!/usr/bin/yarn dev
import { createClient as connectRedis } from 'redis';

const redisConnection = connectRedis();

redisConnection.on('error', (error) => {
  console.error('Failed to connect to Redis:', error.message);
});

redisConnection.on('connect', () => {
  console.log('Successfully connected to Redis');
});
