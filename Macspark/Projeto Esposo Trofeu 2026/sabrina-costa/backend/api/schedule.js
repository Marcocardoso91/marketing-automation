/**
 * Schedule (posts) API routes.
 */

const express = require('express');
const dayjs = require('dayjs');
const { query } = require('../db/connection');
const { authenticateJWT, requireAdmin } = require('../utils/jwt');

const router = express.Router();

router.use(authenticateJWT);

/**
 * GET /api/schedule
 * Fetch posts with optional filters.
 */
router.get('/', async (req, res, next) => {
    try {
        const {
            week,
            status,
            date,
            format,
            limit = 20,
            offset = 0,
        } = req.query;

        const filters = [];
        const values = [];
        let idx = 1;

        if (week) {
            filters.push(`week_number = $${idx++}`);
            values.push(Number(week));
        }

        if (status) {
            filters.push(`status = $${idx++}`);
            values.push(status);
        }

        if (date) {
            filters.push(`date = $${idx++}`);
            values.push(date);
        }

        if (format) {
            filters.push(`format = $${idx++}`);
            values.push(format);
        }

        const where = filters.length ? `WHERE ${filters.join(' AND ')}` : '';
        const safeLimit = Math.min(Number(limit) || 20, 100);
        const safeOffset = Number(offset) || 0;

        const dataSql = `
            SELECT id, date, week_number, format, theme, hook, cta, objective,
                   stories_ideas, status, posted_at, created_at, updated_at
            FROM posts
            ${where}
            ORDER BY date ASC
            LIMIT $${idx++}
            OFFSET $${idx++}
        `;

        const dataResult = await query(dataSql, [...values, safeLimit, safeOffset]);
        const countSql = `SELECT COUNT(*) AS total FROM posts ${where}`;
        const countResult = await query(countSql, values);

        res.json({
            success: true,
            data: dataResult.rows.map((row) => ({
                id: row.id,
                date: row.date,
                weekNumber: row.week_number,
                format: row.format,
                theme: row.theme,
                hook: row.hook,
                cta: row.cta,
                objective: row.objective,
                storiesIdeas: row.stories_ideas,
                status: row.status,
                postedAt: row.posted_at,
                createdAt: row.created_at,
                updatedAt: row.updated_at,
            })),
            count: parseInt(countResult.rows[0]?.total || 0, 10),
        });
    } catch (error) {
        next(error);
    }
});

/**
 * POST /api/schedule
 * Create a new post entry (admin only).
 */
router.post('/', requireAdmin, async (req, res, next) => {
    try {
        const {
            date,
            weekNumber,
            format,
            theme,
            hook,
            cta,
            objective,
            storiesIdeas,
            status = 'planned',
        } = req.body;

        if (!date || !weekNumber || !format || !theme) {
            return res.status(400).json({
                success: false,
                error: 'Campos obrigatórios: date, weekNumber, format, theme',
            });
        }

        const result = await query(
            `INSERT INTO posts (date, week_number, format, theme, hook, cta, objective, stories_ideas, status)
             VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
             RETURNING id, date, week_number, format, theme, hook, cta, objective,
                       stories_ideas, status, posted_at, created_at, updated_at`,
            [
                date,
                Number(weekNumber),
                format,
                theme,
                hook || null,
                cta || null,
                objective || null,
                storiesIdeas || null,
                status,
            ]
        );

        const row = result.rows[0];

        res.status(201).json({
            success: true,
            data: {
                id: row.id,
                date: row.date,
                weekNumber: row.week_number,
                format: row.format,
                theme: row.theme,
                hook: row.hook,
                cta: row.cta,
                objective: row.objective,
                storiesIdeas: row.stories_ideas,
                status: row.status,
                postedAt: row.posted_at,
                createdAt: row.created_at,
                updatedAt: row.updated_at,
            },
        });
    } catch (error) {
        next(error);
    }
});

/**
 * PUT /api/schedule/:id
 * Update a post entry.
 */
router.put('/:id', async (req, res, next) => {
    try {
        const { id } = req.params;
        const updates = req.body || {};

        const fieldMap = {
            date: 'date',
            weekNumber: 'week_number',
            format: 'format',
            theme: 'theme',
            hook: 'hook',
            cta: 'cta',
            objective: 'objective',
            storiesIdeas: 'stories_ideas',
            status: 'status',
            postedAt: 'posted_at',
        };

        const setClauses = [];
        const values = [];
        let idx = 1;

        Object.entries(fieldMap).forEach(([key, column]) => {
            if (updates[key] !== undefined) {
                setClauses.push(`${column} = $${idx++}`);
                values.push(updates[key]);
            }
        });

        if (!setClauses.length) {
            return res.status(400).json({
                success: false,
                error: 'Nenhum campo para atualizar',
            });
        }

        // Automatically set posted_at when status moves to posted
        if (
            updates.status === 'posted' &&
            updates.postedAt === undefined &&
            !setClauses.some((clause) => clause.includes('posted_at'))
        ) {
            setClauses.push(`posted_at = $${idx++}`);
            values.push(dayjs().toISOString());
        }

        const sql = `
            UPDATE posts
            SET ${setClauses.join(', ')}, updated_at = NOW()
            WHERE id = $${idx}
            RETURNING id, date, week_number, format, theme, hook, cta, objective,
                      stories_ideas, status, posted_at, created_at, updated_at
        `;

        values.push(id);
        const result = await query(sql, values);

        if (result.rows.length === 0) {
            return res.status(404).json({
                success: false,
                error: 'Post não encontrado',
            });
        }

        const row = result.rows[0];

        res.json({
            success: true,
            data: {
                id: row.id,
                date: row.date,
                weekNumber: row.week_number,
                format: row.format,
                theme: row.theme,
                hook: row.hook,
                cta: row.cta,
                objective: row.objective,
                storiesIdeas: row.stories_ideas,
                status: row.status,
                postedAt: row.posted_at,
                createdAt: row.created_at,
                updatedAt: row.updated_at,
            },
        });
    } catch (error) {
        next(error);
    }
});

module.exports = router;
