const localtunnel = require('localtunnel');

let currentTunnel = null;

const startTunnel = async () => {
  try {
    console.log('Starting localtunnel...');
    currentTunnel = await localtunnel({ port: 8000, local_host: '127.0.0.1', subdomain: 'lovetrackerdev99' });

    console.log(`your url is: ${currentTunnel.url}`);

    currentTunnel.on('close', () => {
      console.log('Tunnel closed. Restarting...');
      setTimeout(startTunnel, 2000);
    });
    
    currentTunnel.on('error', (err) => {
      console.log('Tunnel error:', err);
      currentTunnel.close();
    });
    
  } catch (err) {
    console.log('Failed to start tunnel:', err);
    setTimeout(startTunnel, 2000);
  }
};

startTunnel();

// Keep event loop alive
setInterval(() => {}, 1000 * 60 * 60);
