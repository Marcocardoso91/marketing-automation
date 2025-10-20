/**
 * Config API routes.
 */

const express = require('express');
const { authenticateJWT, requireAdmin } = require('../utils/jwt');
const { getAllConfig, getConfigValue, setConfigValue } = require('../utils/config');

const router = express.Router();

router.use(authenticateJWT);

/**
 * GET /api/config
 * Return all configuration objects.
 */
router.get('/', async (req, res, next) => {
    try {
        const config = await getAllConfig();
        res.json({
            success: true,
            data: {
                thresholds: config.thresholds || {},
                whatsapp: config.whatsapp || {},
                alertsSchedule: config.alerts_schedule || {},
                general: config.general || {},
            },
        });
    } catch (error) {
        next(error);
    }
});

/**
 * GET /api/config/:key
 * Return a specific configuration section.
 */
router.get('/:key', async (req, res, next) => {
    try {
        const { key } = req.params;
        const dbKey = key === 'alertsSchedule' ? 'alerts_schedule' : key;
        const value = await getConfigValue(dbKey, null);

        if (value === null) {
            return res.status(404).json({
                success: false,
                error: 'Configuração não encontrada',
            });
        }

        res.json({
            success: true,
            data: value,
        });
    } catch (error) {
        next(error);
    }
});

/**
 * PUT /api/config
 * Update multiple configuration keys at once. Admin only.
 */
router.put('/', requireAdmin, async (req, res, next) => {
    try {
        const updates = req.body || {};
        const keyMap = {
            thresholds: 'thresholds',
            whatsapp: 'whatsapp',
            alertsSchedule: 'alerts_schedule',
            general: 'general',
        };

        let updated = false;

        for (const [key, value] of Object.entries(updates)) {
            const dbKey = keyMap[key];
            if (!dbKey || value === undefined) {
                continue;
            }
            await setConfigValue(dbKey, value);
            updated = true;
        }

        if (!updated) {
            return res.status(400).json({
                success: false,
                error: 'Nenhuma configuração válida para atualizar',
            });
        }

        const config = await getAllConfig();
        res.json({
            success: true,
            message: 'Configurações atualizadas com sucesso',
            data: {
                thresholds: config.thresholds || {},
                whatsapp: config.whatsapp || {},
                alertsSchedule: config.alerts_schedule || {},
                general: config.general || {},
            },
        });
    } catch (error) {
        next(error);
    }
});

module.exports = router;
