#!/usr/bin/yarn dev
import { createQueue, Job } from 'kue';

const BLOCKED_PHONE_NUMBERS = ['4153518780', '4153518781'];
const notificationQueue = createQueue();

/**
 * Sends a notification to a phone number with a message.
 * @param {String} phone
 * @param {String} text
 * @param {Job} task
 * @param {*} callback
 */
const deliverNotification = (phone, text, task, callback) => {
  let totalSteps = 2, remainingSteps = 2;
  let interval = setInterval(() => {
    if (totalSteps - remainingSteps <= totalSteps / 2) {
      task.progress(totalSteps - remainingSteps, totalSteps);
    }
    if (BLOCKED_PHONE_NUMBERS.includes(phone)) {
      callback(new Error(`Phone number ${phone} is blocked`));
      clearInterval(interval);
      return;
    }
    if (totalSteps === remainingSteps) {
      console.log(
        `Delivering notification to ${phone}, with message: ${text}`,
      );
    }
    --remainingSteps || callback();
    remainingSteps || clearInterval(interval);
  }, 1000);
};

notificationQueue.process('push_notification_code_3', 2, (task, callback) => {
  deliverNotification(task.data.phone, task.data.message, task, callback);
});
