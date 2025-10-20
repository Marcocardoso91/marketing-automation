/**
 * Alert helpers - evaluate metrics against thresholds and persist alerts.
 */

const dayjs = require('dayjs');
const { query } = require('../db/connection');
const { getConfigValue } = require('./config');

const DEFAULT_THRESHOLDS = {
    ctr_min: 1.5,
    cpc_max: 0.7,
    cpm_max: 10,
    frequency_max: 3,
    cost_per_follower_max: 1.3,
};

/**
 * Generate alerts based on thresholds for a given metric record.
 * @param {object} metric - Metric record from database.
 * @param {object} thresholds - Threshold configuration.
 * @returns {Array<object>} - Alerts to persist.
 */
function buildAlerts(metric, thresholds = DEFAULT_THRESHOLDS) {
    if (!metric) {
        return [];
    }

    const alerts = [];
    const safe = { ...DEFAULT_THRESHOLDS, ...(thresholds || {}) };
    for (const key of Object.keys(safe)) {
        const value = safe[key];
        safe[key] = value !== null && value !== undefined ? Number(value) : DEFAULT_THRESHOLDS[key];
    }

    const metricCtr = metric.ctr !== null && metric.ctr !== undefined ? parseFloat(metric.ctr) : null;
    const metricCpc = metric.cpc !== null && metric.cpc !== undefined ? parseFloat(metric.cpc) : null;
    const metricCpm = metric.cpm !== null && metric.cpm !== undefined ? parseFloat(metric.cpm) : null;
    const metricFrequency = metric.frequency !== null && metric.frequency !== undefined ? parseFloat(metric.frequency) : null;
    const metricCpf = metric.cost_per_follower !== null && metric.cost_per_follower !== undefined
        ? parseFloat(metric.cost_per_follower)
        : null;

    if (metricCtr !== null && metricCtr < safe.ctr_min) {
        alerts.push({
            type: 'ctr_low',
            message: `⚠️ ALERTA: CTR abaixo da meta (${metricCtr}% < ${safe.ctr_min}%)`,
            metadata: {
                date: metric.date,
                ctr: metricCtr,
                threshold: safe.ctr_min,
            },
        });
    }

    if (metricCpc !== null && metricCpc > safe.cpc_max) {
        alerts.push({
            type: 'cpc_high',
            message: `⚠️ ALERTA: CPC acima da meta (R$${metricCpc.toFixed(2)} > R$${safe.cpc_max.toFixed(2)})`,
            metadata: {
                date: metric.date,
                cpc: metricCpc,
                threshold: safe.cpc_max,
            },
        });
    }

    if (metricCpm !== null && metricCpm > safe.cpm_max) {
        alerts.push({
            type: 'cpm_high',
            message: `⚠️ ALERTA: CPM acima da meta (R$${metricCpm.toFixed(2)} > R$${safe.cpm_max.toFixed(2)})`,
            metadata: {
                date: metric.date,
                cpm: metricCpm,
                threshold: safe.cpm_max,
            },
        });
    }

    if (metricFrequency !== null && metricFrequency > safe.frequency_max) {
        alerts.push({
            type: 'frequency_high',
            message: `⚠️ ALERTA: Frequência muito alta (${metricFrequency} > ${safe.frequency_max})`,
            metadata: {
                date: metric.date,
                frequency: metricFrequency,
                threshold: safe.frequency_max,
            },
        });
    }

    if (metricCpf !== null && metricCpf > safe.cost_per_follower_max) {
        alerts.push({
            type: 'cost_per_follower_high',
            message: `⚠️ ALERTA: Custo por seguidor alto (R$${metricCpf.toFixed(2)} > R$${safe.cost_per_follower_max.toFixed(2)})`,
            metadata: {
                date: metric.date,
                costPerFollower: metricCpf,
                threshold: safe.cost_per_follower_max,
            },
        });
    }

    return alerts;
}

/**
 * Persist alerts to the database.
 * @param {Array<object>} alerts - Alerts to save.
 */
async function persistAlerts(alerts) {
    if (!alerts.length) {
        return 0;
    }

    const inserted = [];
    for (const alert of alerts) {
        const result = await query(
            `INSERT INTO alerts (type, message, metadata, sent_at, status)
             VALUES ($1, $2, $3::jsonb, $4, $5)
             RETURNING *`,
            [
                alert.type,
                alert.message,
                JSON.stringify(alert.metadata || {}),
                alert.sent_at || dayjs().toISOString(),
                alert.status || 'sent',
            ]
        );
        inserted.push(result.rows[0]);
    }
    return inserted.length;
}

/**
 * Fetch thresholds from config table using defaults when missing.
 */
async function fetchThresholdConfig() {
    const thresholds = await getConfigValue('thresholds', DEFAULT_THRESHOLDS);
    return { ...DEFAULT_THRESHOLDS, ...(thresholds || {}) };
}

/**
 * Evaluate metric and store alerts in database.
 * @param {object} metric - Metric record from database.
 * @returns {Promise<number>} Number of alerts generated.
 */
async function evaluateAndPersistAlerts(metric) {
    const thresholds = await fetchThresholdConfig();
    const alerts = buildAlerts(metric, thresholds);
    return persistAlerts(alerts);
}

module.exports = {
    buildAlerts,
    persistAlerts,
    fetchThresholdConfig,
    evaluateAndPersistAlerts,
};
