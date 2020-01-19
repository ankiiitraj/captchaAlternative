var path = require('path');
var express = require('express');
var app = express();
var multer  = require('multer');

const fileUpload = require('express-fileupload');

var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, './public/audio/');
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + file.originalname);
  }
});

var upload = multer({ storage: storage });

app.use(express.static(path.join(__dirname, 'public')));


app.use(fileUpload());
app.post('/upload', upload.single('audio'), function (req, res) {
//   var audioPath = req.file.path.replace(/^public\//, '');
//   fs.writeFile('sample.wav', req.files.upload_file, function(err) {
//     res.sendStatus(err ? 500 : 200);
//   });
//   res.redirect(audioPath);


  if (!req.files || Object.keys(req.files).length === 0) {
    return res.status(400).send('No files were uploaded.');
  }

  // The name of the input field (i.e. "sampleFile") is used to retrieve the uploaded file
  let upload_file = req.files.upload_file;

  // Use the mv() method to place the file somewhere on your server
  upload_file.mv('sample.wav', function(err) {
    if (err)
      return res.status(500).send(err);

    res.send('File uploaded!');
  });
});
app.get('/', function(req, res){
    res.sendFile(path.join(__dirname + '/index.html'));
});
app.use(function (err, req, res, next) {
  if (err instanceof multer.MulterError) res.status(500).send(err.message);
  else next(err);
});

app.listen(5500);