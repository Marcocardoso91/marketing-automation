/**
 * Hooks library API routes.
 */

const express = require('express');
const { query } = require('../db/connection');
const { authenticateJWT } = require('../utils/jwt');

const router = express.Router();

router.use(authenticateJWT);

/**
 * GET /api/hooks
 * List hooks with optional filters.
 */
router.get('/', async (req, res, next) => {
    try {
        const {
            category,
            search,
            limit = 50,
            offset = 0,
        } = req.query;

        const filters = [];
        const values = [];
        let idx = 1;

        if (category) {
            filters.push(`category = $${idx++}`);
            values.push(category);
        }

        if (search) {
            filters.push(`text ILIKE $${idx++}`);
            values.push(`%${search}%`);
        }

        const where = filters.length ? `WHERE ${filters.join(' AND ')}` : '';
        const safeLimit = Math.min(Number(limit) || 50, 100);
        const safeOffset = Number(offset) || 0;

        const hooksSql = `
            SELECT id, category, text, usage_count, created_at
            FROM hooks
            ${where}
            ORDER BY usage_count DESC, created_at DESC
            LIMIT $${idx++}
            OFFSET $${idx++}
        `;

        const hooksResult = await query(hooksSql, [...values, safeLimit, safeOffset]);

        const countSql = `SELECT COUNT(*) AS total FROM hooks ${where}`;
        const countResult = await query(countSql, values);
        const total = parseInt(countResult.rows[0]?.total || 0, 10);

        const categoriesResult = await query('SELECT DISTINCT category FROM hooks ORDER BY category ASC');

        res.json({
            success: true,
            data: hooksResult.rows.map((row) => ({
                id: row.id,
                category: row.category,
                text: row.text,
                usageCount: row.usage_count,
                createdAt: row.created_at,
            })),
            pagination: {
                total,
                limit: safeLimit,
                offset: safeOffset,
                hasMore: safeOffset + hooksResult.rows.length < total,
            },
            categories: categoriesResult.rows.map((row) => row.category),
        });
    } catch (error) {
        next(error);
    }
});

/**
 * GET /api/hooks/categories
 * List available hook categories.
 */
router.get('/categories/list', async (req, res, next) => {
    try {
        const result = await query('SELECT DISTINCT category FROM hooks ORDER BY category ASC');
        res.json({
            success: true,
            data: result.rows.map((row) => row.category),
        });
    } catch (error) {
        next(error);
    }
});

/**
 * PUT /api/hooks/:id/increment
 * Increment hook usage counter.
 */
router.put('/:id/increment', async (req, res, next) => {
    try {
        const { id } = req.params;

        const result = await query(
            `UPDATE hooks
             SET usage_count = usage_count + 1
             WHERE id = $1
             RETURNING id, usage_count`,
            [id]
        );

        if (result.rows.length === 0) {
            return res.status(404).json({
                success: false,
                error: 'Gancho não encontrado',
            });
        }

        res.json({
            success: true,
            data: {
                id: result.rows[0].id,
                usageCount: result.rows[0].usage_count,
            },
        });
    } catch (error) {
        next(error);
    }
});

module.exports = router;
