/**
 * Alerts API routes.
 */

const express = require('express');
const dayjs = require('dayjs');
const { query } = require('../db/connection');
const { authenticateJWT, requireAdmin } = require('../utils/jwt');
const { getConfigValue, setConfigValue } = require('../utils/config');

const router = express.Router();

// All alerts routes require authentication
router.use(authenticateJWT);

/**
 * GET /api/alerts
 * List alerts with optional filters.
 */
router.get('/', async (req, res, next) => {
    try {
        const {
            limit = 10,
            offset = 0,
            status,
            type,
            from,
            to,
        } = req.query;

        const filters = [];
        const filterValues = [];
        let filterIdx = 1;

        if (status) {
            filters.push(`status = $${filterIdx++}`);
            filterValues.push(status);
        }

        if (type) {
            filters.push(`type = $${filterIdx++}`);
            filterValues.push(type);
        }

        if (from) {
            filters.push(`sent_at >= $${filterIdx++}`);
            filterValues.push(dayjs(from).toISOString());
        }

        if (to) {
            filters.push(`sent_at <= $${filterIdx++}`);
            filterValues.push(dayjs(to).endOf('day').toISOString());
        }

        const baseQuery = 'FROM alerts';
        const whereClause = filters.length ? ` WHERE ${filters.join(' AND ')}` : '';

        const safeLimit = Math.min(Number(limit) || 10, 100);
        const safeOffset = Number(offset) || 0;

        const dataSql = `
            SELECT id, type, message, sent_at, status, metadata, created_at
            ${baseQuery}
            ${whereClause}
            ORDER BY sent_at DESC
            LIMIT $${filterValues.length + 1}
            OFFSET $${filterValues.length + 2}
        `;

        const dataParams = [...filterValues, safeLimit, safeOffset];
        const result = await query(dataSql, dataParams);

        const countSql = `SELECT COUNT(*) AS total ${baseQuery}${whereClause}`;
        const countResult = await query(countSql, filterValues);

        const total = parseInt(countResult.rows[0]?.total || 0, 10);

        res.json({
            success: true,
            data: result.rows.map((row) => ({
                id: row.id,
                type: row.type,
                message: row.message,
                sentAt: row.sent_at,
                status: row.status,
                metadata: row.metadata,
                createdAt: row.created_at,
            })),
            pagination: {
                total,
                limit: safeLimit,
                offset: safeOffset,
                hasMore: safeOffset + result.rows.length < total,
            },
        });
    } catch (error) {
        next(error);
    }
});

/**
 * POST /api/alerts
 * Create a manual alert (typically triggered by automation).
 */
router.post('/', async (req, res, next) => {
    try {
        const { type, message, metadata, status = 'sent', sentAt } = req.body;

        if (!type || !message) {
            return res.status(400).json({
                success: false,
                error: 'Campos obrigatórios: type, message',
            });
        }

        const result = await query(
            `INSERT INTO alerts (type, message, metadata, status, sent_at)
             VALUES ($1, $2, $3::jsonb, $4, $5)
             RETURNING id, type, message, sent_at, status, metadata, created_at`,
            [
                type,
                message,
                JSON.stringify(metadata || {}),
                status,
                sentAt ? dayjs(sentAt).toISOString() : dayjs().toISOString(),
            ]
        );

        res.status(201).json({
            success: true,
            data: {
                id: result.rows[0].id,
                type: result.rows[0].type,
                message: result.rows[0].message,
                sentAt: result.rows[0].sent_at,
                status: result.rows[0].status,
                metadata: result.rows[0].metadata,
            },
        });
    } catch (error) {
        next(error);
    }
});

/**
 * GET /api/alerts/config
 * Fetch alert-related configuration.
 */
router.get('/config', async (req, res, next) => {
    try {
        const thresholds = await getConfigValue('thresholds', {});
        const whatsapp = await getConfigValue('whatsapp', {});
        const schedule = await getConfigValue('alerts_schedule', {});

        res.json({
            success: true,
            data: {
                thresholds,
                whatsapp,
                schedule,
            },
        });
    } catch (error) {
        next(error);
    }
});

/**
 * PUT /api/alerts/config
 * Update alert thresholds or WhatsApp settings. Admin only.
 */
router.put('/config', requireAdmin, async (req, res, next) => {
    try {
        const { thresholds, whatsapp, schedule } = req.body;

        if (thresholds) {
            await setConfigValue('thresholds', thresholds);
        }
        if (whatsapp) {
            await setConfigValue('whatsapp', whatsapp);
        }
        if (schedule) {
            await setConfigValue('alerts_schedule', schedule);
        }

        const updatedConfig = {
            thresholds: await getConfigValue('thresholds', {}),
            whatsapp: await getConfigValue('whatsapp', {}),
            schedule: await getConfigValue('alerts_schedule', {}),
        };

        res.json({
            success: true,
            message: 'Configurações de alertas atualizadas com sucesso',
            data: updatedConfig,
        });
    } catch (error) {
        next(error);
    }
});

module.exports = router;
