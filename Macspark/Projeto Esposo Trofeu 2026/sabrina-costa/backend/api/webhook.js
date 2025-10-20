/**
 * Webhook API routes for integrations (n8n, etc.).
 */

const express = require('express');
const dayjs = require('dayjs');
const { parse } = require('csv-parse/sync');
const { query } = require('../db/connection');
const { evaluateAndPersistAlerts } = require('../utils/alerts');

const router = express.Router();

const WEBHOOK_SECRET = process.env.WEBHOOK_SECRET || process.env.WEBHOOK_TOKEN;

function ensureWebhookAuth(req, res, next) {
    const token = req.headers['x-webhook-token'];
    if (!WEBHOOK_SECRET || token !== WEBHOOK_SECRET) {
        return res.status(401).json({
            success: false,
            error: 'Token de webhook inválido',
        });
    }
    next();
}

function parseNumber(value) {
    if (value === undefined || value === null || value === '') {
        return null;
    }
    const num = Number(value);
    return Number.isNaN(num) ? null : num;
}

function normalizeMetricPayload(payload) {
    const errors = [];

    const date = payload.date;
    const parsedDate = date ? dayjs(date) : null;

    if (!date || !parsedDate || !parsedDate.isValid() || parsedDate.format('YYYY-MM-DD') !== date) {
        errors.push('Data inválida');
    } else if (parsedDate.isAfter(dayjs(), 'day')) {
        errors.push('Data não pode ser futura');
    }

    const ctr = parseNumber(payload.ctr);
    if (ctr !== null && (ctr < 0 || ctr > 100)) {
        errors.push('CTR deve estar entre 0 e 100');
    }

    const cpc = parseNumber(payload.cpc);
    const cpm = parseNumber(payload.cpm);
    const frequency = parseNumber(payload.frequency);
    const visits = parseNumber(payload.visits);
    const newFollowers = parseNumber(payload.newFollowers ?? payload.new_followers);
    const cost = parseNumber(payload.cost);
    const impressions = parseNumber(payload.impressions);
    const clicks = parseNumber(payload.clicks);

    const costPerFollower = newFollowers && newFollowers > 0 && cost !== null
        ? Number((cost / newFollowers).toFixed(2))
        : null;

    if (!cost && cost !== 0) {
        errors.push('Custo (cost) é obrigatório');
    }

    if (!ctr && ctr !== 0) {
        errors.push('CTR é obrigatório');
    }

    if (!cpc && cpc !== 0) {
        errors.push('CPC é obrigatório');
    }

    return {
        data: {
            date,
            ctr,
            cpc,
            cpm,
            frequency,
            visits,
            new_followers: newFollowers,
            cost,
            impressions,
            clicks,
            cost_per_follower: costPerFollower,
        },
        errors,
    };
}

async function upsertMetric(metric) {
    const result = await query(
        `INSERT INTO metrics (date, ctr, cpc, cpm, frequency, visits, new_followers, cost, impressions, clicks, cost_per_follower)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
         ON CONFLICT (date)
         DO UPDATE SET
             ctr = EXCLUDED.ctr,
             cpc = EXCLUDED.cpc,
             cpm = EXCLUDED.cpm,
             frequency = EXCLUDED.frequency,
             visits = EXCLUDED.visits,
             new_followers = EXCLUDED.new_followers,
             cost = EXCLUDED.cost,
             impressions = EXCLUDED.impressions,
             clicks = EXCLUDED.clicks,
             cost_per_follower = EXCLUDED.cost_per_follower,
             updated_at = NOW()
         RETURNING *`,
        [
            metric.date,
            metric.ctr,
            metric.cpc,
            metric.cpm,
            metric.frequency,
            metric.visits,
            metric.new_followers,
            metric.cost,
            metric.impressions,
            metric.clicks,
            metric.cost_per_follower,
        ]
    );

    return result.rows[0];
}

/**
 * POST /api/webhook/metrics
 * Receive JSON metrics payload.
 */
router.post('/metrics', ensureWebhookAuth, async (req, res, next) => {
    try {
        const payload = Array.isArray(req.body) ? req.body : [req.body];

        const saved = [];
        const errors = [];
        let alertsGenerated = 0;

        for (const item of payload) {
            const { data, errors: validationErrors } = normalizeMetricPayload(item || {});
            if (validationErrors.length) {
                errors.push({ data: item, errors: validationErrors });
                continue;
            }

            const metric = await upsertMetric(data);
            const generated = await evaluateAndPersistAlerts(metric);
            alertsGenerated += generated;
            saved.push({
                id: metric.id,
                date: metric.date,
                costPerFollower: metric.cost_per_follower,
            });
        }

        res.json({
            success: errors.length === 0,
            message: `Métricas processadas: ${saved.length}`,
            savedRecords: saved.length,
            alertsGenerated,
            data: saved,
            errors,
        });
    } catch (error) {
        next(error);
    }
});

/**
 * POST /api/webhook/metrics/csv
 * Receive CSV metrics payload.
 */
router.post('/metrics/csv', ensureWebhookAuth, async (req, res, next) => {
    try {
        if (!req.body) {
            return res.status(400).json({
                success: false,
                error: 'Arquivo CSV vazio',
            });
        }

        const records = parse(req.body, {
            columns: true,
            skip_empty_lines: true,
            trim: true,
        });

        const saved = [];
        const errors = [];
        let alertsGenerated = 0;

        let index = 1;
        for (const record of records) {
            const { data, errors: validationErrors } = normalizeMetricPayload(record);
            if (validationErrors.length) {
                errors.push({
                    row: index,
                    errors: validationErrors,
                });
                index += 1;
                continue;
            }

            const metric = await upsertMetric(data);
            const generated = await evaluateAndPersistAlerts(metric);
            alertsGenerated += generated;
            saved.push({
                id: metric.id,
                date: metric.date,
                costPerFollower: metric.cost_per_follower,
            });
            index += 1;
        }

        res.json({
            success: errors.length === 0,
            message: 'CSV processado com sucesso',
            savedRecords: saved.length,
            alertsGenerated,
            data: saved,
            errors,
        });
    } catch (error) {
        next(error);
    }
});

module.exports = router;
