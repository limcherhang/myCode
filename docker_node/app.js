const { exec } = require('child_process');

id = '65b9b22e3bb61226a5bc5d4c';
year = '2022';

const pythonProcess = exec(`cd ./python_scripts && python3 ghg_report.py ${id} ${year}`, (error, stdout, stderr) => {
    if (error) {
        console.error(`Execute Error: ${error}`);
        return;
    }
    console.log(`Python script output: ${stdout}`);
});

pythonProcess.stdout.on('data', (data) => {
    console.log(`Python script output: ${data}`);
});

pythonProcess.stderr.on('data', (data) => {
    console.error(`Python script error: ${data}`);
});