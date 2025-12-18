const { spawn } = require('child_process');
const path = require('path');

exports.handler = async (event, context) => {
  return new Promise((resolve, reject) => {
    const pythonPath = path.join(__dirname, '../../.venv/bin/python');
    
    const djangoServer = spawn('python', [
      path.join(__dirname, '../../manage.py'),
      'runserver',
      '0.0.0.0:8000'
    ]);

    let output = '';
    let error = '';

    djangoServer.stdout.on('data', (data) => {
      output += data.toString();
    });

    djangoServer.stderr.on('data', (data) => {
      error += data.toString();
    });

    setTimeout(() => {
      resolve({
        statusCode: 200,
        body: output || error
      });
    }, 100);
  });
};
