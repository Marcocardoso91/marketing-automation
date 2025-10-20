const { buildAlerts } = require('../utils/alerts');

describe('buildAlerts', () => {
    it('returns empty array when no metric provided', () => {
        expect(buildAlerts(null)).toEqual([]);
    });

    it('creates alerts when metric values cross defaults', () => {
        const metric = {
            date: '2025-10-20',
            ctr: 1.0,
            cpc: 0.9,
            cpm: 12,
            frequency: 3.5,
            cost_per_follower: 2.0,
        };

        const alerts = buildAlerts(metric);
        const types = alerts.map((a) => a.type);

        expect(types).toEqual(
            expect.arrayContaining([
                'ctr_low',
                'cpc_high',
                'cpm_high',
                'frequency_high',
                'cost_per_follower_high',
            ])
        );
        alerts.forEach((alert) => {
            expect(alert).toHaveProperty('message');
            expect(alert).toHaveProperty('metadata');
        });
    });

    it('respects custom threshold overrides', () => {
        const metric = {
            date: '2025-10-20',
            ctr: 2.5,
            cpc: 0.35,
        };

        const alerts = buildAlerts(metric, { ctr_min: 3, cpc_max: 0.3 });
        expect(alerts).toHaveLength(2);
    });
});
