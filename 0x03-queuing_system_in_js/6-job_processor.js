#!/usr/bin/yarn dev
import kue from 'kue';

const notificationQueue = kue.createQueue();

const notifyUser = (phone, text) => {
  console.log(`Sending message to ${phone} with text: ${text}`);
};

notificationQueue.process('user_notification_code', (job, done) => {
  notifyUser(job.data.phone, job.data.text);
  done();
});
