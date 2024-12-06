#!/usr/bin/yarn test
import sinon from 'sinon';
import { expect } from 'chai';
import { createQueue } from 'kue';
import generatePushNotificationTasks from './8-job.js';

describe('generatePushNotificationTasks', () => {
  const SPY = sinon.spy(console);
  const TEST_QUEUE = createQueue({ name: 'push_notification_code_testing' });

  before(() => {
    TEST_QUEUE.testMode.enter(true);
  });

  after(() => {
    TEST_QUEUE.testMode.clear();
    TEST_QUEUE.testMode.exit();
  });

  afterEach(() => {
    SPY.log.resetHistory();
  });

  it('throws an error if tasks is not an array', () => {
    expect(
      generatePushNotificationTasks.bind(generatePushNotificationTasks, {}, TEST_QUEUE)
    ).to.throw('tasks is not an array');
  });

  it('adds tasks to the queue with the correct type', (done) => {
    expect(TEST_QUEUE.testMode.jobs.length).to.equal(0);
    const taskDetails = [
      {
        phoneNumber: '44556677889',
        message: 'Use the code 1982 to verify your account',
      },
      {
        phoneNumber: '98877665544',
        message: 'Use the code 1738 to verify your account',
      },
    ];
    generatePushNotificationTasks(taskDetails, TEST_QUEUE);
    expect(TEST_QUEUE.testMode.jobs.length).to.equal(2);
    expect(TEST_QUEUE.testMode.jobs[0].data).to.deep.equal(taskDetails[0]);
    expect(TEST_QUEUE.testMode.jobs[0].type).to.equal('push_notification_code_4');
    TEST_QUEUE.process('push_notification_code_4', () => {
      expect(
        SPY.log
          .calledWith('Notification task created:', TEST_QUEUE.testMode.jobs[0].id)
      ).to.be.true;
      done();
    });
  });

  it('registers the progress event handler for a task', (done) => {
    TEST_QUEUE.testMode.jobs[0].addListener('progress', () => {
      expect(
        SPY.log
          .calledWith('Notification task', TEST_QUEUE.testMode.jobs[0].id, '25% complete')
      ).to.be.true;
      done();
    });
    TEST_QUEUE.testMode.jobs[0].emit('progress', 25);
  });

  it('registers the failed event handler for a task', (done) => {
    TEST_QUEUE.testMode.jobs[0].addListener('failed', () => {
      expect(
        SPY.log
          .calledWith('Notification task', TEST_QUEUE.testMode.jobs[0].id, 'failed:', 'Failed to send')
      ).to.be.true;
      done();
    });
    TEST_QUEUE.testMode.jobs[0].emit('failed', new Error('Failed to send'));
  });

  it('registers the complete event handler for a task', (done) => {
    TEST_QUEUE.testMode.jobs[0].addListener('complete', () => {
      expect(
        SPY.log
          .calledWith('Notification task', TEST_QUEUE.testMode.jobs[0].id, 'completed')
      ).to.be.true;
      done();
    });
    TEST_QUEUE.testMode.jobs[0].emit('complete');
  });
});
