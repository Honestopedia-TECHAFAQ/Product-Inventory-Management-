const axios = require('axios');

const API_KEY = 'AIzaSyC1RHav3wTQqoMgx6jlcwiAbfJn_3k28UQ';
const SHEET_ID = '1qq7vJyjsptOOhgGZowXJ00O6GZ6KzFHRT7D3AYwNuIY';
const SHEET_RANGE = 'Sheet1!A2:D'; 

const fetchData = async () => {
    const url = `https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/${SHEET_RANGE}?key=${API_KEY}`;

    try {
        const response = await axios.get(url);
        const rows = response.data.values || []; 
        return rows.map(row => ({
            companyName: row[0] || 'N/A',  
            productName: row[1] || 'N/A',
            certifications: row[2] || 'N/A',
            country: row[3] || 'N/A'
        }));
    } catch (error) {
        console.error('Error fetching data from Google Sheets:', error);
        throw error;
    }
};

module.exports = fetchData;
