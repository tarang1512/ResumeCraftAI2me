// Quick redeploy to force Vercel
const fs = require('fs');
console.log('Index.html size:', fs.statSync('index.html').size);