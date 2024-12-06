#!/usr/bin/yarn dev
import kue from 'kue';

const notifications = [
  {
    phone: '4153518780',
    text: 'Verification code: 1234 to verify your account',
  },
  {
    phone: '4153518781',
    text: 'Verification code: 4562 to verify your account',
  },
  {
    phone: '4153518743',
    text: 'Verification code: 4321 to verify your account',
  },
  {
    phone: '4153538781',
    text: 'Verification code: 4562 to verify your account',
  },
  {
    phone: '4153118782',
    text: 'Verification code: 4321 to verify your account',
  },
  {
    phone: '4153718781',
    text: 'Verification code: 4562 to verify your account',
  },
  {
    phone: '4159518782',
    text: 'Verification code: 4321 to verify your account',
  },
  {
    phone: '4158718781',
    text: 'Verification code: 4562 to verify your account',
  },
  {
    phone: '4153818782',
    text: 'Verification code: 4321 to verify your account',
  },
  {
    phone: '4154318781',
    text: 'Verification code: 4562 to verify your account',
  },
  {
    phone: '4151218782',
    text: 'Verification code: 4321 to verify your account',
  },
];

const notificationQueue = kue.createQueue({ name: 'user_verification_code' });

for (const notification of notifications) {
  const task = notificationQueue.create('user_verification_code', notification);

  task
    .on('job enqueue', () => {
      console.log('Job created with ID:', task.id);
    })
    .on('job complete', () => {
      console.log('Job', task.id, 'completed successfully');
    })
    .on('job failed', (err) => {
      console.log('Job', task.id, 'failed with error:', err.message || err.toString());
    })
    .on('job progress', (progress, _data) => {
      console.log('Job', task.id, `is ${progress}% complete`);
    });

  task.save();
}
