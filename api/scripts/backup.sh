#!/bin/bash
set -e

echo "========================================="
echo "Facebook Ads AI Agent - Backup Script"
echo "========================================="

# Create backups directory if not exists
mkdir -p backups

# Generate timestamp
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backups/backup_${DATE}.sql.gz"

echo "Creating backup: ${BACKUP_FILE}"

# Backup PostgreSQL database
docker-compose exec -T postgres pg_dump -U postgres facebook_ads_ai | gzip > "${BACKUP_FILE}"

# Check if backup was successful
if [ -f "${BACKUP_FILE}" ]; then
    BACKUP_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
    echo "✓ Backup created successfully: ${BACKUP_FILE} (${BACKUP_SIZE})"
else
    echo "✗ Backup failed!"
    exit 1
fi

# Cleanup old backups (keep last 7 days)
echo "Cleaning up old backups..."
find backups/ -name "backup_*.sql.gz" -mtime +7 -delete
REMAINING=$(ls -1 backups/backup_*.sql.gz 2>/dev/null | wc -l)
echo "✓ Cleanup complete. ${REMAINING} backups remaining."

echo ""
echo "========================================="
echo "Backup completed successfully!"
echo "========================================="

