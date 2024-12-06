#!/usr/bin/yarn dev
import kue from 'kue';

const notificationQueue = kue.createQueue({ name: 'user_notification_code' });

const notificationJob = notificationQueue.create('user_notification_code', {
  phone: '08115309345',
  text: 'Account successfully registered',
});

notificationJob
  .on('job enqueue', () => {
    console.log(`Job created with ID: ${notificationJob.id}`);
  })
  .on('job complete', () => {
    console.log('Job successfully completed');
  })
  .on('job failed attempt', () => {
    console.log('Job failed during execution');
  });

notificationJob.save();
