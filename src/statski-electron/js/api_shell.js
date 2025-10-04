// const {PythonShell} = require('python-shell');
const api_executable = "FlaskAPI.exe";
var python_api = require("child_process").execFile(api_executable);
module.exports = { python_api };

// const api_path = "../python/FlaskAPI.py";

// const python_api = new PythonShell(api_path);

// python_api.on('message', function(message) {
//   console.log(message);
// })

// python_api.end(function (err) {
//   if (err){
//     throw err;
//   };

//   console.log('Finished API Process');
// });

// module.exports = { python_api };