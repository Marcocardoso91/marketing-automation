#!/bin/bash
set -e

echo "========================================="
echo "Facebook Ads AI Agent - Restore Script"
echo "========================================="

# Check if backup file is provided
if [ -z "$1" ]; then
    echo "Usage: ./scripts/restore.sh <backup_file>"
    echo ""
    echo "Available backups:"
    ls -lh backups/backup_*.sql.gz 2>/dev/null || echo "No backups found!"
    exit 1
fi

BACKUP_FILE=$1

# Check if backup file exists
if [ ! -f "${BACKUP_FILE}" ]; then
    echo "✗ Error: Backup file not found: ${BACKUP_FILE}"
    exit 1
fi

echo "⚠️  WARNING: This will restore the database from backup."
echo "   File: ${BACKUP_FILE}"
echo ""
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

echo ""
echo "Restoring database from ${BACKUP_FILE}..."

# Drop and recreate database
docker-compose exec -T postgres psql -U postgres -c "DROP DATABASE IF EXISTS facebook_ads_ai;"
docker-compose exec -T postgres psql -U postgres -c "CREATE DATABASE facebook_ads_ai;"

# Restore from backup
gunzip -c "${BACKUP_FILE}" | docker-compose exec -T postgres psql -U postgres facebook_ads_ai

echo "✓ Database restored successfully!"
echo ""
echo "Don't forget to run migrations:"
echo "  docker-compose exec app alembic upgrade head"
echo ""

