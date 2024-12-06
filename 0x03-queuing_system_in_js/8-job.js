#!/usr/bin/yarn dev
import { Queue, Job } from 'kue';

/**
 * Generates push notification tasks based on job details from the provided array.
 * @param {Job[]} taskList
 * @param {Queue} notificationQueue
 */
export const generatePushNotificationTasks = (taskList, notificationQueue) => {
  if (!(taskList instanceof Array)) {
    throw new Error('taskList is not an array');
  }
  for (const taskDetails of taskList) {
    const task = notificationQueue.create('push_notification_code_4', taskDetails);

    task
      .on('enqueue', () => {
        console.log('Notification task created:', task.id);
      })
      .on('complete', () => {
        console.log('Notification task', task.id, 'completed');
      })
      .on('failed', (error) => {
        console.log('Notification task', task.id, 'failed:', error.message || error.toString());
      })
      .on('progress', (progress, _data) => {
        console.log('Notification task', task.id, `${progress}% complete`);
      });
    task.save();
  }
};

export default generatePushNotificationTasks;
