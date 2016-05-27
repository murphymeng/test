var MongoClient = require('mongodb').MongoClient;
var assert = require('assert');

var url = 'mongodb://localhost:27017/stock';

var insertDocument = function(db, callback) {
   db.collection('day').insertOne( {
       symbol: 'aaaadfsdf'
   }, function(err, result) {
    assert.equal(err, null);
    console.log("Inserted a document into the restaurants collection.");
    callback();
  });
};

var find = function(db, callback) {
   var cursor =db.collection('day').find( );
   cursor.each(function(err, doc) {
      assert.equal(err, null);
      if (doc != null) {
         console.dir(doc);
      } else {
         callback();
      }
   });
};

MongoClient.connect(url, function(err, db) {
  assert.equal(null, err);
  console.log("Connected correctly to server.");

  find(db, function() {
      db.close();
  });

  // insertDocument(db, function() {
  //    db.close();
  // });

  // var cursor = db.collection('day').find();
  // cursor.each(function(err, doc) {
  //   console.dir(doc);
  // });
});
