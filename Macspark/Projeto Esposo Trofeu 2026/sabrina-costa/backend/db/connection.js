/**
 * Database Connection Pool
 * Dashboard Sabrina Blogueira
 */

const { Pool } = require('pg');
require('dotenv').config();

// Create connection pool
const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: process.env.NODE_ENV === 'production' ? {
        rejectUnauthorized: false
    } : false,
    max: 20, // Maximum number of clients in the pool
    idleTimeoutMillis: 30000, // Close idle clients after 30 seconds
    connectionTimeoutMillis: 2000, // Return an error after 2 seconds if connection could not be established
});

// Log connection
pool.on('connect', () => {
    console.log('✓ Connected to PostgreSQL database');
});

// Log errors
pool.on('error', (err) => {
    console.error('Unexpected error on idle client', err);
    process.exit(-1);
});

// Test connection
async function testConnection() {
    try {
        const client = await pool.connect();
        const result = await client.query('SELECT NOW()');
        console.log('✓ Database connection test successful:', result.rows[0].now);
        client.release();
        return true;
    } catch (error) {
        console.error('✗ Database connection test failed:', error.message);
        return false;
    }
}

// Query helper function
async function query(text, params) {
    const start = Date.now();
    try {
        const res = await pool.query(text, params);
        const duration = Date.now() - start;
        console.log('Executed query', { text, duration, rows: res.rowCount });
        return res;
    } catch (error) {
        console.error('Query error:', { text, error: error.message });
        throw error;
    }
}

// Transaction helper
async function transaction(callback) {
    const client = await pool.connect();
    try {
        await client.query('BEGIN');
        const result = await callback(client);
        await client.query('COMMIT');
        return result;
    } catch (error) {
        await client.query('ROLLBACK');
        throw error;
    } finally {
        client.release();
    }
}

module.exports = {
    pool,
    query,
    transaction,
    testConnection
};

