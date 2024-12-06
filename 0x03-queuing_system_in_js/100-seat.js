#!/usr/bin/yarn dev
import express from 'express';
import { promisify } from 'util';
import { createQueue } from 'kue';
import { createClient } from 'redis';

const app = express();
const redisClient = createClient({ name: 'seat_reservation_system' });
const reservationQueue = createQueue();
const MAX_SEATS = 50;
let isReservationActive = false;
const SERVER_PORT = 1245;

/**
 * Updates the available seats in the system.
 * @param {number} seatsCount - The number of seats to set.
 */
const updateSeatAvailability = async (seatsCount) => {
  return promisify(redisClient.SET).bind(redisClient)('seats_available', seatsCount);
};

/**
 * Retrieves the current number of available seats.
 * @returns {Promise<String>}
 */
const getAvailableSeats = async () => {
  return promisify(redisClient.GET).bind(redisClient)('seats_available');
};

app.get('/seats_available', (_, res) => {
  getAvailableSeats()
    .then((seats) => {
      res.json({ availableSeats: seats });
    });
});

app.get('/reserve_seat', (_req, res) => {
  if (!isReservationActive) {
    res.json({ status: 'Reservations are currently unavailable' });
    return;
  }
  try {
    const reservationJob = reservationQueue.create('seat_reservation');

    reservationJob.on('failed', (err) => {
      console.log(
        'Seat reservation failed for job',
        reservationJob.id,
        'error: ',
        err.message || err.toString(),
      );
    });

    reservationJob.on('complete', () => {
      console.log(
        'Seat reservation job',
        reservationJob.id,
        'completed successfully'
      );
    });

    reservationJob.save();
    res.json({ status: 'Your reservation is being processed' });
  } catch {
    res.json({ status: 'Reservation could not be processed' });
  }
});

app.get('/process_reservation', (_req, res) => {
  res.json({ status: 'Reservation queue is processing' });

  reservationQueue.process('seat_reservation', (_job, done) => {
    getAvailableSeats()
      .then((seats) => parseInt(seats || 0))
      .then((seatsCount) => {
        if (seatsCount <= 1) {
          isReservationActive = false;
        }
        if (seatsCount >= 1) {
          updateSeatAvailability(seatsCount - 1)
            .then(() => done());
        } else {
          done(new Error('Not enough seats available'));
        }
      });
  });
});

const initializeSeats = async (initialSeats) => {
  return promisify(redisClient.SET)
    .bind(redisClient)('seats_available', Number.parseInt(initialSeats));
};

app.listen(SERVER_PORT, () => {
  initializeSeats(process.env.MAX_SEATS || MAX_SEATS)
    .then(() => {
      isReservationActive = true;
      console.log(`API is running on localhost port ${SERVER_PORT}`);
    });
});

export default app;
