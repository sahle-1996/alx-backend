#!/usr/bin/yarn dev
import { createClient } from 'redis';

const redisClient = createClient();

redisClient.on('error', (err) => {
  console.error(`Failed to connect to Redis: ${err.message}`);
});

const sendDelayedMessage = (msg, delay) => {
  setTimeout(() => {
    console.log(`Preparing to send: ${msg}`);
    redisClient.publish('holberton_channel', msg);
  }, delay);
};

redisClient.on('ready', () => {
  console.log('Successfully connected to Redis');
});

sendDelayedMessage('Holberton Student #1 begins course', 100);
sendDelayedMessage('Holberton Student #2 begins course', 200);
sendDelayedMessage('KILL_SERVER', 300);
sendDelayedMessage('Holberton Student #3 begins course', 400);
