/**
 * Metrics API Endpoints
 * Dashboard Sabrina Costa
 */

const express = require('express');
const { query } = require('../db/connection');
const { authenticateJWT } = require('../utils/jwt');
const { evaluateAndPersistAlerts } = require('../utils/alerts');

const router = express.Router();

// All routes require authentication
router.use(authenticateJWT);

/**
 * GET /api/metrics
 * Get metrics with optional filters
 */
router.get('/', async (req, res, next) => {
    try {
        const { date, period, startDate, endDate, limit = 30, offset = 0 } = req.query;
        
        let sql = 'SELECT * FROM metrics WHERE 1=1';
        const params = [];
        let paramIndex = 1;
        
        // Filter by specific date
        if (date) {
            sql += ` AND date = $${paramIndex++}`;
            params.push(date);
        }
        
        // Filter by period (7d, 30d, 90d)
        if (period && !startDate && !endDate) {
            const days = parseInt(period.replace('d', ''));
            sql += ` AND date >= CURRENT_DATE - INTERVAL '${days} days'`;
        }
        
        // Filter by date range
        if (startDate) {
            sql += ` AND date >= $${paramIndex++}`;
            params.push(startDate);
        }
        if (endDate) {
            sql += ` AND date <= $${paramIndex++}`;
            params.push(endDate);
        }
        
        sql += ' ORDER BY date DESC';
        sql += ` LIMIT $${paramIndex++} OFFSET $${paramIndex++}`;
        params.push(parseInt(limit), parseInt(offset));
        
        const result = await query(sql, params);
        
        // Get total count
        let countSql = 'SELECT COUNT(*) as total FROM metrics WHERE 1=1';
        const countParams = [];
        let countIndex = 1;
        
        if (date) {
            countSql += ` AND date = $${countIndex++}`;
            countParams.push(date);
        }
        if (period && !startDate && !endDate) {
            const days = parseInt(period.replace('d', ''));
            countSql += ` AND date >= CURRENT_DATE - INTERVAL '${days} days'`;
        }
        if (startDate) {
            countSql += ` AND date >= $${countIndex++}`;
            countParams.push(startDate);
        }
        if (endDate) {
            countSql += ` AND date <= $${countIndex++}`;
            countParams.push(endDate);
        }
        
        const countResult = await query(countSql, countParams);
        const total = parseInt(countResult.rows[0].total);
        
        res.json({
            success: true,
            data: result.rows,
            pagination: {
                total,
                limit: parseInt(limit),
                offset: parseInt(offset),
                hasMore: (parseInt(offset) + result.rows.length) < total
            }
        });
        
    } catch (error) {
        next(error);
    }
});

/**
 * POST /api/metrics
 * Create new metric
 */
router.post('/', async (req, res, next) => {
    try {
        const {
            date, ctr, cpc, cpm, frequency,
            visits, newFollowers, cost,
            impressions, clicks
        } = req.body;
        
        // Validate required fields
        if (!date || ctr === undefined || cpc === undefined || cost === undefined) {
            return res.status(400).json({
                success: false,
                error: 'Campos obrigatórios: date, ctr, cpc, cost'
            });
        }
        
        // Validate date
        const metricDate = new Date(date);
        if (isNaN(metricDate.getTime())) {
            return res.status(400).json({
                success: false,
                error: 'Data inválida'
            });
        }
        
        if (metricDate > new Date()) {
            return res.status(400).json({
                success: false,
                error: 'Data não pode ser futura'
            });
        }
        
        // Validate CTR
        if (ctr < 0 || ctr > 100) {
            return res.status(400).json({
                success: false,
                error: 'CTR deve estar entre 0 e 100'
            });
        }
        
        // Calculate cost per follower
        const costPerFollower = newFollowers > 0 ? (cost / newFollowers).toFixed(2) : null;
        
        // Insert into database
        const result = await query(
            `INSERT INTO metrics (
                date, ctr, cpc, cpm, frequency, visits, new_followers, cost,
                impressions, clicks, cost_per_follower
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            RETURNING *`,
            [date, ctr, cpc, cpm, frequency, visits, newFollowers, cost, impressions, clicks, costPerFollower]
        );
        
        const created = result.rows[0];
        await evaluateAndPersistAlerts(created);

        res.status(201).json({
            success: true,
            data: created
        });
        
    } catch (error) {
        if (error.code === '23505') { // Unique violation
            return res.status(409).json({
                success: false,
                error: 'Métrica para esta data já existe'
            });
        }
        next(error);
    }
});

/**
 * PUT /api/metrics/:id
 * Update existing metric
 */
router.put('/:id', async (req, res, next) => {
    try {
        const { id } = req.params;
        const updateFields = req.body;
        
        // Build dynamic update query
        const allowedFields = ['ctr', 'cpc', 'cpm', 'frequency', 'visits', 'newFollowers', 'cost', 'impressions', 'clicks'];
        const updates = [];
        const values = [];
        let paramIndex = 1;
        
        for (const field of allowedFields) {
            if (updateFields[field] !== undefined) {
                const dbField = field === 'newFollowers' ? 'new_followers' : field;
                updates.push(`${dbField} = $${paramIndex++}`);
                values.push(updateFields[field]);
            }
        }
        
        if (updates.length === 0) {
            return res.status(400).json({
                success: false,
                error: 'Nenhum campo para atualizar'
            });
        }
        
        // Recalculate cost_per_follower if cost or newFollowers changed
        if (updateFields.cost || updateFields.newFollowers) {
            // Get current values
            const current = await query('SELECT cost, new_followers FROM metrics WHERE id = $1', [id]);
            if (current.rows.length > 0) {
                const finalCost = updateFields.cost || current.rows[0].cost;
                const finalFollowers = updateFields.newFollowers || current.rows[0].new_followers;
                const costPerFollower = finalFollowers > 0 ? (finalCost / finalFollowers).toFixed(2) : null;
                updates.push(`cost_per_follower = $${paramIndex++}`);
                values.push(costPerFollower);
            }
        }
        
        values.push(id);
        
        const sql = `UPDATE metrics SET ${updates.join(', ')}, updated_at = NOW() WHERE id = $${paramIndex} RETURNING *`;
        
        const result = await query(sql, values);
        
        if (result.rows.length === 0) {
            return res.status(404).json({
                success: false,
                error: 'Métrica não encontrada'
            });
        }
        
        const updated = result.rows[0];
        await evaluateAndPersistAlerts(updated);

        res.json({
            success: true,
            data: updated
        });
        
    } catch (error) {
        next(error);
    }
});

/**
 * DELETE /api/metrics/:id
 * Delete metric (admin only)
 */
router.delete('/:id', async (req, res, next) => {
    try {
        // Check if admin
        if (req.user.role !== 'admin') {
            return res.status(403).json({
                success: false,
                error: 'Apenas administradores podem deletar métricas'
            });
        }
        
        const { id } = req.params;
        
        const result = await query('DELETE FROM metrics WHERE id = $1 RETURNING id', [id]);
        
        if (result.rows.length === 0) {
            return res.status(404).json({
                success: false,
                error: 'Métrica não encontrada'
            });
        }
        
        res.json({
            success: true,
            message: 'Métrica deletada com sucesso'
        });
        
    } catch (error) {
        next(error);
    }
});

/**
 * GET /api/metrics/summary
 * Get summary statistics
 */
router.get('/summary', async (req, res, next) => {
    try {
        const { period = '30d' } = req.query;
        const days = parseInt(period.replace('d', ''));
        
        const result = await query(`
            SELECT 
                COUNT(*) as total_days,
                ROUND(AVG(ctr), 2) as avg_ctr,
                ROUND(AVG(cpc), 2) as avg_cpc,
                ROUND(AVG(cpm), 2) as avg_cpm,
                ROUND(AVG(frequency), 2) as avg_frequency,
                ROUND(AVG(visits), 0) as avg_visits_per_day,
                ROUND(AVG(new_followers), 0) as avg_new_followers_per_day,
                ROUND(AVG(cost), 2) as avg_cost_per_day,
                SUM(visits) as total_visits,
                SUM(new_followers) as total_new_followers,
                SUM(cost) as total_cost,
                CASE 
                    WHEN SUM(new_followers) > 0 
                    THEN ROUND(SUM(cost) / SUM(new_followers), 2)
                    ELSE NULL
                END as cost_per_follower
            FROM metrics
            WHERE date >= CURRENT_DATE - INTERVAL '${days} days'
        `);
        
        res.json({
            success: true,
            data: {
                period,
                totalDays: parseInt(result.rows[0].total_days),
                averages: {
                    ctr: parseFloat(result.rows[0].avg_ctr),
                    cpc: parseFloat(result.rows[0].avg_cpc),
                    cpm: parseFloat(result.rows[0].avg_cpm),
                    frequency: parseFloat(result.rows[0].avg_frequency),
                    visitsPerDay: parseInt(result.rows[0].avg_visits_per_day),
                    newFollowersPerDay: parseInt(result.rows[0].avg_new_followers_per_day),
                    costPerDay: parseFloat(result.rows[0].avg_cost_per_day)
                },
                totals: {
                    visits: parseInt(result.rows[0].total_visits) || 0,
                    newFollowers: parseInt(result.rows[0].total_new_followers) || 0,
                    cost: parseFloat(result.rows[0].total_cost) || 0,
                    costPerFollower: parseFloat(result.rows[0].cost_per_follower) || 0
                }
            }
        });
        
    } catch (error) {
        next(error);
    }
});

module.exports = router;

