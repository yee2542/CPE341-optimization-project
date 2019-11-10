const fs = require('fs')

fs.readFile('./place.csv', 'utf8', (err, data) => {
    console.log(data)
    const line = data.split(`\n`)
    console.log(line)
})