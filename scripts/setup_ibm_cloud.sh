#!/bin/bash
# LexConductor - IBM Cloud Setup Automation Script
# IBM Dev Day AI Demystified Hackathon 2026
# Team: AI Kings 👑

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  LexConductor - IBM Cloud Setup Automation                    ║${NC}"
echo -e "${BLUE}║  IBM Dev Day AI Demystified Hackathon 2026                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if IBM Cloud CLI is installed
if ! command -v ibmcloud &> /dev/null; then
    echo -e "${RED}✗ IBM Cloud CLI not found${NC}"
    echo -e "${YELLOW}Please install it from: https://cloud.ibm.com/docs/cli${NC}"
    exit 1
fi

echo -e "${GREEN}✓ IBM Cloud CLI found${NC}"
echo ""

# Check if logged in
if ! ibmcloud target &> /dev/null; then
    echo -e "${YELLOW}⚠ Not logged in to IBM Cloud${NC}"
    echo -e "${BLUE}Please login first:${NC}"
    echo "  ibmcloud login --sso"
    echo ""
    read -p "Press Enter after logging in..."
fi

echo -e "${GREEN}✓ Logged in to IBM Cloud${NC}"
echo ""

# Variables
RESOURCE_GROUP="Default"
REGION_CLOUDANT="us-south"
REGION_COS="us-south"
REGION_CODE_ENGINE="jp-osa"
PROJECT_NAME="lexconductor"

echo -e "${BLUE}Configuration:${NC}"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Cloudant Region: $REGION_CLOUDANT"
echo "  COS Region: $REGION_COS"
echo "  Code Engine Region: $REGION_CODE_ENGINE"
echo ""

read -p "Continue with this configuration? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Setup cancelled${NC}"
    exit 0
fi

# ============================================================================
# 1. Create API Key
# ============================================================================
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}1. Creating IBM Cloud API Key${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"

API_KEY_NAME="${PROJECT_NAME}-api-key-$(date +%Y%m%d)"
echo "Creating API key: $API_KEY_NAME"

# Create API key and save to file
API_KEY_OUTPUT=$(ibmcloud iam api-key-create "$API_KEY_NAME" \
    --description "LexConductor Hackathon API Key" \
    --output json)

if [ $? -eq 0 ]; then
    API_KEY=$(echo "$API_KEY_OUTPUT" | jq -r '.apikey')
    echo -e "${GREEN}✓ API Key created successfully${NC}"
    echo -e "${YELLOW}⚠ IMPORTANT: Save this API key - it won't be shown again!${NC}"
    echo ""
    echo -e "${GREEN}API_KEY=${API_KEY}${NC}"
    echo ""
    
    # Save to temporary file
    echo "WATSONX_API_KEY=$API_KEY" > .env.temp
    echo "CLOUDANT_API_KEY=$API_KEY" >> .env.temp
    echo "COS_API_KEY=$API_KEY" >> .env.temp
else
    echo -e "${RED}✗ Failed to create API key${NC}"
    exit 1
fi

# ============================================================================
# 2. Create Cloudant Instance
# ============================================================================
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}2. Creating Cloudant Instance${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"

CLOUDANT_NAME="${PROJECT_NAME}-cloudant"
echo "Creating Cloudant instance: $CLOUDANT_NAME"

ibmcloud resource service-instance-create "$CLOUDANT_NAME" \
    cloudantnosqldb lite "$REGION_CLOUDANT" \
    -g "$RESOURCE_GROUP"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Cloudant instance created${NC}"
    
    # Wait for instance to be ready
    echo "Waiting for instance to be ready..."
    sleep 10
    
    # Create service credentials
    CLOUDANT_CRED_NAME="${CLOUDANT_NAME}-credentials"
    ibmcloud resource service-key-create "$CLOUDANT_CRED_NAME" Manager \
        --instance-name "$CLOUDANT_NAME" \
        --output json > cloudant_creds.json
    
    if [ $? -eq 0 ]; then
        CLOUDANT_URL=$(jq -r '.credentials.url' cloudant_creds.json)
        CLOUDANT_USERNAME=$(jq -r '.credentials.username' cloudant_creds.json)
        CLOUDANT_PASSWORD=$(jq -r '.credentials.password' cloudant_creds.json)
        
        echo -e "${GREEN}✓ Cloudant credentials created${NC}"
        echo "  URL: $CLOUDANT_URL"
        
        # Save to temp file
        echo "CLOUDANT_URL=$CLOUDANT_URL" >> .env.temp
        echo "CLOUDANT_USERNAME=$CLOUDANT_USERNAME" >> .env.temp
        echo "CLOUDANT_PASSWORD=$CLOUDANT_PASSWORD" >> .env.temp
        
        rm cloudant_creds.json
    fi
else
    echo -e "${YELLOW}⚠ Cloudant instance may already exist or creation failed${NC}"
fi

# ============================================================================
# 3. Create Cloud Object Storage Instance
# ============================================================================
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}3. Creating Cloud Object Storage Instance${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"

COS_NAME="${PROJECT_NAME}-cos"
echo "Creating COS instance: $COS_NAME"

ibmcloud resource service-instance-create "$COS_NAME" \
    cloud-object-storage lite global \
    -g "$RESOURCE_GROUP"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ COS instance created${NC}"
    
    # Wait for instance to be ready
    echo "Waiting for instance to be ready..."
    sleep 10
    
    # Create service credentials with HMAC
    COS_CRED_NAME="${COS_NAME}-credentials"
    ibmcloud resource service-key-create "$COS_CRED_NAME" Writer \
        --instance-name "$COS_NAME" \
        --parameters '{"HMAC":true}' \
        --output json > cos_creds.json
    
    if [ $? -eq 0 ]; then
        COS_INSTANCE_ID=$(jq -r '.credentials.iam_serviceid_crn' cos_creds.json)
        
        echo -e "${GREEN}✓ COS credentials created${NC}"
        echo "  Instance ID: $COS_INSTANCE_ID"
        
        # Save to temp file
        echo "COS_INSTANCE_ID=$COS_INSTANCE_ID" >> .env.temp
        echo "COS_ENDPOINT=s3.us-south.cloud-object-storage.appdomain.cloud" >> .env.temp
        
        rm cos_creds.json
    fi
else
    echo -e "${YELLOW}⚠ COS instance may already exist or creation failed${NC}"
fi

# ============================================================================
# 4. Create Code Engine Project
# ============================================================================
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}4. Creating Code Engine Project${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"

# Install Code Engine plugin if not installed
if ! ibmcloud plugin list | grep -q code-engine; then
    echo "Installing Code Engine plugin..."
    ibmcloud plugin install code-engine
fi

CE_PROJECT_NAME="${PROJECT_NAME}-agents"
echo "Creating Code Engine project: $CE_PROJECT_NAME"

ibmcloud ce project create --name "$CE_PROJECT_NAME" --region "$REGION_CODE_ENGINE"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Code Engine project created${NC}"
    
    # Save to temp file
    echo "CODE_ENGINE_PROJECT=$CE_PROJECT_NAME" >> .env.temp
    echo "CODE_ENGINE_REGION=$REGION_CODE_ENGINE" >> .env.temp
else
    echo -e "${YELLOW}⚠ Code Engine project may already exist or creation failed${NC}"
fi

# ============================================================================
# Summary
# ============================================================================
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Setup Complete!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

if [ -f .env.temp ]; then
    echo -e "${GREEN}✓ Credentials saved to .env.temp${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Review the credentials in .env.temp"
    echo "2. Copy them to your .env file:"
    echo "   cat .env.temp >> .env"
    echo "3. Add watsonx Orchestrate and watsonx.ai credentials manually"
    echo "4. Delete .env.temp for security:"
    echo "   rm .env.temp"
    echo ""
    echo -e "${YELLOW}⚠ IMPORTANT: Never commit .env or .env.temp to git!${NC}"
    echo ""
    
    echo -e "${BLUE}Generated credentials:${NC}"
    cat .env.temp
fi

echo ""
echo -e "${GREEN}Setup script completed successfully!${NC}"
echo ""
