#!/bin/bash
# Validation Script - P0 Implementations
# Tests infrastructure directly via SQL/SSH

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW} P0 IMPLEMENTATIONS VALIDATION${NC}"
echo -e "${YELLOW}========================================${NC}\n"

# Test 1: SSH Tunnel
echo -e "${YELLOW}[1/5]${NC} Testing SSH tunnel..."
if netstat -an | grep "5433.*LISTEN" > /dev/null; then
    echo -e "${GREEN}[OK]${NC} SSH tunnel is active (port 5433)"
else
    echo -e "${RED}[FAIL]${NC} SSH tunnel not found. Run: ssh -f -N -L 5433:postgres-prd:5432 marcocardoso@217.196.62.130"
fi

# Test 2: Database Connection
echo -e "\n${YELLOW}[2/5]${NC} Testing database connection..."
TABLE_COUNT=$(ssh marcocardoso@217.196.62.130 "docker exec postgres-prd psql -U postgres -d facebook_ads_marketing -t -c 'SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='"'"'public'"'"';'" 2>&1 | tr -d ' ')
if [ "$TABLE_COUNT" -eq "7" ]; then
    echo -e "${GREEN}[OK]${NC} Database has $TABLE_COUNT tables (expected 7)"
else
    echo -e "${RED}[FAIL]${NC} Database has $TABLE_COUNT tables (expected 7)"
fi

# Test 3: Migration Version
echo -e "\n${YELLOW}[3/5]${NC} Testing Alembic migration..."
MIGRATION=$(ssh marcocardoso@217.196.62.130 "docker exec postgres-prd psql -U postgres -d facebook_ads_marketing -t -c 'SELECT version_num FROM alembic_version;'" 2>&1 | tr -d ' ')
if [ "$MIGRATION" = "002_add_user_auth_fields" ]; then
    echo -e "${GREEN}[OK]${NC} Migration version: $MIGRATION"
else
    echo -e "${RED}[FAIL]${NC} Migration version: $MIGRATION (expected 002_add_user_auth_fields)"
fi

# Test 4: hashed_password column
echo -e "\n${YELLOW}[4/5]${NC} Testing users.hashed_password..."
HAS_COLUMN=$(ssh marcocardoso@217.196.62.130 "docker exec postgres-prd psql -U postgres -d facebook_ads_marketing -t -c \"SELECT COUNT(*) FROM information_schema.columns WHERE table_name='users' AND column_name='hashed_password';\"" 2>&1 | tr -d ' ')
if [ "$HAS_COLUMN" -eq "1" ]; then
    echo -e "${GREEN}[OK]${NC} users.hashed_password column exists"
else
    echo -e "${RED}[FAIL]${NC} users.hashed_password column NOT FOUND"
fi

# Test 5: Redis availability
echo -e "\n${YELLOW}[5/5]${NC} Testing Redis..."
if netstat -an | grep "6379.*LISTEN" > /dev/null; then
    echo -e "${GREEN}[OK]${NC} Redis is running (port 6379)"
else
    echo -e "${YELLOW}[WARN]${NC} Redis not running (optional for now)"
fi

# Summary
echo -e "\n${YELLOW}========================================${NC}"
echo -e "${GREEN}VALIDATION COMPLETE${NC}"
echo -e "${YELLOW}========================================${NC}"

echo -e "\n${GREEN}Next steps:${NC}"
echo -e "  1. Run: cd api && python scripts/test_imports.py"
echo -e "  2. Start API: uvicorn src.main:app --reload"
echo -e "  3. Test endpoint: curl http://localhost:8000/health"
