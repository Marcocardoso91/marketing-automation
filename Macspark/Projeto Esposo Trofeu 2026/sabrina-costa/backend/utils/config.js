/**
 * Config utilities - read and write configuration values stored in the database.
 */

const { query } = require('../db/connection');

/**
 * Retrieve a configuration value by key.
 * @param {string} key - Config key (e.g. 'thresholds').
 * @param {any} defaultValue - Value returned when key does not exist.
 */
async function getConfigValue(key, defaultValue = null) {
    const result = await query('SELECT value FROM config WHERE key = $1', [key]);
    if (result.rows.length === 0) {
        return defaultValue;
    }
    return result.rows[0].value;
}

/**
 * Set a configuration value, creating or updating as needed.
 * @param {string} key - Config key.
 * @param {object} value - Serializable value.
 */
async function setConfigValue(key, value) {
    await query(
        `INSERT INTO config (key, value)
         VALUES ($1, $2::jsonb)
         ON CONFLICT (key)
         DO UPDATE SET value = EXCLUDED.value, updated_at = NOW()`,
        [key, JSON.stringify(value)]
    );
}

/**
 * Retrieve all configuration values as an object keyed by config key.
 */
async function getAllConfig() {
    const result = await query('SELECT key, value FROM config ORDER BY key ASC');
    return result.rows.reduce((acc, row) => {
        acc[row.key] = row.value;
        return acc;
    }, {});
}

module.exports = {
    getConfigValue,
    setConfigValue,
    getAllConfig,
};
