import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';
import fs from 'fs';
import csv from 'csv-parser';

// Add the Stealth plugin to puppeteer-extra
puppeteer.use(StealthPlugin());

// Function to read CSV and return data as a JSON object
async function readCSV(csvFilePath) {
  return new Promise((resolve, reject) => {
    const results = [];  // Array to store the row objects

    fs.createReadStream(csvFilePath)
      .pipe(csv())  // Convert CSV rows into JavaScript objects
      .on('data', (row) => {
        results.push(row);  // Add each row to the results array
      })
      .on('end', () => {
        resolve(results);  // Resolve the promise with the complete data
      })
      .on('error', (error) => {
        reject(error);  // Handle errors
      });
  });
}

// Function to login and withdraw with retry logic
async function loginAndWithdraw(username, tag, retries = 3) {
  try {
    const browser = await puppeteer.launch({
      headless: false,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    await page.goto('https://xrpspin.com/login.php', { waitUntil: 'networkidle0' });
    
    // Click the alert confirmation button
    const rechargeAlertBtn = await page.waitForSelector('button.swal2-confirm', { timeout: 2000 });
    await rechargeAlertBtn.click();
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Login
    const usernameInput = await page.waitForSelector('input[name="username"]', { timeout: 20000 });
    await usernameInput.type(username);
    await page.type('input[name="password"]', 'Matako');
    const loginButton = await page.waitForSelector('button[id="login"]');
    await loginButton.click();
    await new Promise(resolve => setTimeout(resolve, 5000));
    console.log('Logged in successfully');

    // Withdrawal process
    const withdrawButton = await page.waitForSelector('button[onclick="location.href=\'withdraw.php\'"]', { timeout: 30000 });
    await withdrawButton.click();
    await page.waitForNavigation({ waitUntil: 'networkidle0' });

    const maxButton = await page.waitForSelector('span[onclick="allmoneyXrp()"]', { timeout: 20000, visible: true });
    await maxButton.click();
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Check and fill XRP address and tag if not present
    const xrpAddrInput = await page.$('input[id="xrpAddr"]');
    const currentValue = await page.evaluate(el => el.value, xrpAddrInput);
    if (!currentValue) {
      await page.type('input[id="xrpAddr"]', 'rHcXrn8joXL2Qe7BaMnhB5VRuj1XKEmUW6');
      await new Promise(resolve => setTimeout(resolve, 1000));
      await page.type('input[id="distTag"]', tag);
    }

    await page.waitForSelector('input[name="passwordXrp"]');
    await page.type('input[name="passwordXrp"]', 'Matako');
    await new Promise(resolve => setTimeout(resolve, 2000));
    await page.click('button[id="goXRPbtn"]');
    
    // Take screenshots
    await page.screenshot({ path: 'withdrawPage.png' });

    // Get dialog message
    const successDialog = await page.waitForSelector('div[role="dialog"]', { timeout: 50000 });
    const innerMessage = await successDialog.$('#swal2-html-container');
    const dialogText = await innerMessage.evaluate(el => el.textContent.trim());
    console.log('Status:', dialogText);

    await page.screenshot({ path: `${username}.png` }); // Capture a screenshot for verification
    await browser.close();
    
  } catch (error) {
    console.error(`Error occurred for ${username}:`, error);
    await browser.close();
    
    // Retry logic
    if (retries > 0) {
      console.log(`Retrying... (${retries} retries left)`);
      await new Promise(resolve => setTimeout(resolve, 30000)); // Wait before retrying
      await loginAndWithdraw(username, tag, retries - 1);  // Recursive retry call
    } else {
      console.error(`Failed after multiple retries for ${username}`);
      await browser.close();
    }
  }
}

// Function to shuffle an array
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

// Main
(async () => {
  // Function to wait for a specified duration
  const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

  // Infinite loop to keep running the process
  while (true) {
    // Read the CSV
    const csvData = await readCSV('accounts.csv');
    // Shuffle the accounts
    const shuffledData = shuffleArray(csvData);
    for (const entry of shuffledData) {
      console.log(`Starting ${entry.username}`);
      await loginAndWithdraw(entry.username, entry.tag);  // Ensure this function is asynchronous
      // Optional delay between each account processing (e.g., 10 seconds)
      await delay(8000);  // 8-second delay between processing each entry
    }

    // Delay of 5-6 minutes before starting the next cycle
    console.log("Cycle complete. Waiting for 5-6 minutes...");
    await delay(Math.floor(Math.random() * 60000) + 300000);  // Random delay between 5 to 6 minutes
  }
})();
