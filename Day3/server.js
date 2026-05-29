const express = require('express');
const app = express();
const port = 8080;

app.get('/', (req, res) =>{
    res.send('<h1>Hello from Athitthiyan!</h1><p>Pod Name: ${process.env.HOSTNAME}</p>');
});

app.listen(port, ()=>{
    console.log(`Server is running on port ${port}`);
})