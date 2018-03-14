#!/usr/bin/env node

const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');

// Connection URL
const url = 'mongodb://localhost:27017';

// Database Name
const dbName = 'storj-sandbox';

// Use connect method to connect to the server
MongoClient.connect(url, function(err, client) {
  assert.equal(null, err);
  console.log("Connected successfully to server");

  const db = client.db(dbName);

  // find and update all users to be activated
  db.collection('users').updateMany({activated: false}, {$set:
    {
      activated: true,
      activator: null
    }
  }, function(err) {
      if (err) {
          console.error(err);
      }

      client.close();
  });
});