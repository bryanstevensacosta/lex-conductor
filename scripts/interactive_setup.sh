#!/bin/bash
# LexConductor - Interactive Setup Guide
# IBM Dev Day AI Demystified Hackathon 2026

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

clear

echo -e "${BLUE}"
cat << "EOF"
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║           LexConductor - Interactive Setup Guide               ║
║           IBM Dev Day AI Demystified Hackathon 2026            ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${CYAN}This guide will help you set up all IBM Cloud services step by step.${NC}"
echo ""
echo -e "${YELLOW}⏱️  Estimated time: 35 minutes${NC}"
echo -e "${YELLOW}💰 Estimated cost: <$5 (all Lite plans)${NC}"
echo ""

read -p "Press Enter to begin..."

# ============================================================================
# Step 1: IBM Cloud API Key
# ============================================================================
clear
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Step 1/5: Create IBM Cloud API Key${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}This API key will be used for watsonx.ai, Cloudant, and COS.${NC}"
echo ""
echo -e "${YELLOW}Instructions:${NC}"
echo "1. Open: ${CYAN}https://cloud.ibm.com/iam/apikeys${NC}"
echo "2. Click 'Create' button"
echo "3. Name: ${GREEN}lexconductor-api-key${NC}"
echo "4. Description: ${GREEN}LexConductor Hackathon API Key${NC}"
echo "5. Click 'Create'"
echo "6. ${RED}IMPORTANT: Copy the API key immediately!${NC}"
echo ""

read -p "Press Enter when you have your API key ready..."

echo ""
echo -e "${GREEN}Please paste your IBM Cloud API key:${NC}"
read -s IBM_CLOUD_API_KEY
echo ""

if [ -z "$IBM_CLOUD_API_KEY" ]; then
    echo -e "${RED}✗ No API key provided${NC}"
    exit 1
fi

echo -e "${GREEN}✓ API key saved${NC}"
echo ""

# Save to temp file
echo "# IBM Cloud API Key" > .env.setup
echo "WATSONX_API_KEY=$IBM_CLOUD_API_KEY" >> .env.setup
echo "CLOUDANT_API_KEY=$IBM_CLOUD_API_KEY" >> .env.setup
echo "COS_API_KEY=$IBM_CLOUD_API_KEY" >> .env.setup
echo "" >> .env.setup

read -p "Press Enter to continue to Step 2..."

# ============================================================================
# Step 2: watsonx.ai Project
# ============================================================================
clear
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Step 2/5: watsonx.ai Project${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}💡 IMPORTANT: watsonx.ai creates a Sandbox Project automatically!${NC}"
echo -e "${CYAN}You can use the Sandbox Project instead of creating a new one.${NC}"
echo ""
echo -e "${YELLOW}Option 1: Use Sandbox Project (Recommended)${NC}"
echo "1. Open: ${CYAN}https://dataplatform.cloud.ibm.com/wx/home${NC}"
echo "2. Click 'Projects' → 'View all projects'"
echo "3. Find and select the ${GREEN}'Sandbox'${NC} project"
echo "4. Go to 'Manage' tab"
echo "5. In 'General' → 'Details', copy the 'Project ID'"
echo ""
echo -e "${YELLOW}Option 2: Create New Project (Optional)${NC}"
echo "1. Open: ${CYAN}https://dataplatform.cloud.ibm.com/wx/home${NC}"
echo "2. Click 'Projects' → 'New project'"
echo "3. Select 'Create an empty project'"
echo "4. Name: ${GREEN}lexconductor-hackathon${NC}"
echo "5. Click 'Create'"
echo "6. Go to 'Manage' tab → Copy 'Project ID'"
echo ""

read -p "Press Enter when you have your Project ID ready..."

echo ""
echo -e "${GREEN}Please paste your watsonx.ai Project ID:${NC}"
read WATSONX_PROJECT_ID
echo ""

if [ -z "$WATSONX_PROJECT_ID" ]; then
    echo -e "${RED}✗ No Project ID provided${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Project ID saved${NC}"
echo ""

# Save to temp file
echo "# watsonx.ai" >> .env.setup
echo "WATSONX_PROJECT_ID=$WATSONX_PROJECT_ID" >> .env.setup
echo "WATSONX_URL=https://us-south.ml.cloud.ibm.com" >> .env.setup
echo "" >> .env.setup

read -p "Press Enter to continue to Step 3..."

# ============================================================================
# Step 3: Cloudant
# ============================================================================
clear
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Step 3/5: Create Cloudant Instance${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Instructions:${NC}"
echo "1. Open: ${CYAN}https://cloud.ibm.com/catalog/services/cloudant${NC}"
echo "2. Plan: ${GREEN}Lite (Free)${NC}"
echo "3. Region: ${GREEN}US South${NC}"
echo "4. Service name: ${GREEN}lexconductor-cloudant${NC}"
echo "5. Click 'Create'"
echo "6. Go to 'Service credentials' → 'New credential'"
echo "7. Name: ${GREEN}lexconductor-credentials${NC}"
echo "8. Role: ${GREEN}Manager${NC}"
echo "9. Click 'Add' → 'View credentials'"
echo "10. Copy the 'url' value"
echo ""

read -p "Press Enter when you have your Cloudant URL ready..."

echo ""
echo -e "${GREEN}Please paste your Cloudant URL:${NC}"
read CLOUDANT_URL
echo ""

if [ -z "$CLOUDANT_URL" ]; then
    echo -e "${RED}✗ No Cloudant URL provided${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Cloudant URL saved${NC}"
echo ""

# Save to temp file
echo "# Cloudant" >> .env.setup
echo "CLOUDANT_URL=$CLOUDANT_URL" >> .env.setup
echo "" >> .env.setup

echo -e "${YELLOW}Now create the databases:${NC}"
echo "1. Click 'Launch Dashboard'"
echo "2. Click 'Create Database' (3 times):"
echo "   - ${GREEN}golden_clauses${NC}"
echo "   - ${GREEN}historical_decisions${NC}"
echo "   - ${GREEN}regulatory_mappings${NC}"
echo ""

read -p "Press Enter when databases are created..."

echo -e "${GREEN}✓ Cloudant setup complete${NC}"
echo ""

read -p "Press Enter to continue to Step 4..."

# ============================================================================
# Step 4: Cloud Object Storage
# ============================================================================
clear
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Step 4/5: Create Cloud Object Storage Instance${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Instructions:${NC}"
echo "1. Open: ${CYAN}https://cloud.ibm.com/catalog/services/cloud-object-storage${NC}"
echo "2. Plan: ${GREEN}Lite (Free - 25GB)${NC}"
echo "3. Service name: ${GREEN}lexconductor-cos${NC}"
echo "4. Click 'Create'"
echo "5. Go to 'Service credentials' → 'New credential'"
echo "6. Name: ${GREEN}lexconductor-cos-credentials${NC}"
echo "7. Role: ${GREEN}Writer${NC}"
echo "8. ${RED}IMPORTANT: Include HMAC Credential: ON${NC}"
echo "9. Click 'Add' → 'View credentials'"
echo "10. Copy the 'iam_serviceid_crn' value"
echo ""

read -p "Press Enter when you have your COS Instance ID ready..."

echo ""
echo -e "${GREEN}Please paste your COS Instance ID (iam_serviceid_crn):${NC}"
read COS_INSTANCE_ID
echo ""

if [ -z "$COS_INSTANCE_ID" ]; then
    echo -e "${RED}✗ No COS Instance ID provided${NC}"
    exit 1
fi

echo -e "${GREEN}✓ COS Instance ID saved${NC}"
echo ""

# Save to temp file
echo "# Cloud Object Storage" >> .env.setup
echo "COS_INSTANCE_ID=$COS_INSTANCE_ID" >> .env.setup
echo "COS_ENDPOINT=s3.us-south.cloud-object-storage.appdomain.cloud" >> .env.setup
echo "" >> .env.setup

echo -e "${YELLOW}Now create the bucket:${NC}"
echo "1. Go to 'Buckets' → 'Create bucket' → 'Customize your bucket'"
echo "2. Name: ${GREEN}watsonx-hackathon-regulations-[your-name]${NC}"
echo "3. Resiliency: ${GREEN}Regional${NC}"
echo "4. Location: ${GREEN}us-south${NC}"
echo "5. Storage class: ${GREEN}Standard${NC}"
echo "6. Create folders: ${GREEN}EU/, UK/, US/, templates/${NC}"
echo ""

read -p "Enter your bucket name: " COS_BUCKET_NAME

echo "COS_BUCKET_NAME=$COS_BUCKET_NAME" >> .env.setup
echo "" >> .env.setup

read -p "Press Enter when bucket is created..."

echo -e "${GREEN}✓ COS setup complete${NC}"
echo ""

read -p "Press Enter to continue to Step 5..."

# ============================================================================
# Step 5: Code Engine
# ============================================================================
clear
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Step 5/5: Create Code Engine Project${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Instructions:${NC}"
echo "1. Open: ${CYAN}https://cloud.ibm.com/codeengine/overview${NC}"
echo "2. Click 'Start creating' or 'Create project'"
echo "3. Location: ${GREEN}Osaka (jp-osa)${NC} ${RED}← REQUIRED!${NC}"
echo "4. Project name: ${GREEN}lexconductor-agents${NC}"
echo "5. Click 'Create'"
echo ""

read -p "Press Enter when Code Engine project is created..."

# Save to temp file
echo "# Code Engine" >> .env.setup
echo "CODE_ENGINE_PROJECT=lexconductor-agents" >> .env.setup
echo "CODE_ENGINE_REGION=jp-osa" >> .env.setup
echo "" >> .env.setup

echo -e "${GREEN}✓ Code Engine setup complete${NC}"
echo ""

# ============================================================================
# watsonx Orchestrate (Manual)
# ============================================================================
clear
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Additional: watsonx Orchestrate Credentials${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Instructions:${NC}"
echo "1. Open: ${CYAN}https://cloud.ibm.com/${NC}"
echo "2. Resource list → AI/Machine Learning → watsonx Orchestrate"
echo "3. Settings ⚙️ → API details"
echo "4. Copy 'Service Instance URL'"
echo "5. Click 'Generate API Key'"
echo ""

read -p "Press Enter when you have your Orchestrate credentials ready..."

echo ""
echo -e "${GREEN}Please paste your watsonx Orchestrate Instance URL:${NC}"
read WO_INSTANCE
echo ""

echo -e "${GREEN}Please paste your watsonx Orchestrate API Key:${NC}"
read -s WO_API_KEY
echo ""

# Save to temp file
echo "# watsonx Orchestrate" >> .env.setup
echo "WO_INSTANCE=$WO_INSTANCE" >> .env.setup
echo "WO_API_KEY=$WO_API_KEY" >> .env.setup
echo "" >> .env.setup

# ============================================================================
# Summary
# ============================================================================
clear
echo -e "${GREEN}"
cat << "EOF"
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║                    ✓ Setup Complete!                           ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${CYAN}All credentials have been collected!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Review the credentials in .env.setup"
echo "2. Copy them to your .env file:"
echo "   ${GREEN}cat .env.setup >> .env${NC}"
echo "3. Verify the setup:"
echo "   ${GREEN}python scripts/verify_setup.py${NC}"
echo "4. Test connections:"
echo "   ${GREEN}python scripts/test_connections.py${NC}"
echo "5. Delete .env.setup for security:"
echo "   ${GREEN}rm .env.setup${NC}"
echo ""

echo -e "${RED}⚠ IMPORTANT: Never commit .env or .env.setup to git!${NC}"
echo ""

read -p "Would you like to see the collected credentials? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    cat .env.setup
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
fi

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}How would you like to save the credentials?${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "  ${GREEN}1)${NC} Append to .env file ${CYAN}(recommended)${NC}"
echo "     → Adds credentials to your existing .env file"
echo ""
echo "  ${YELLOW}2)${NC} Keep in .env.setup ${CYAN}(manual)${NC}"
echo "     → You copy them manually later"
echo ""
echo "  ${RED}3)${NC} Discard ${CYAN}(cancel)${NC}"
echo "     → Don't save, start over"
echo ""

read -p "Choose option (1/2/3): " -n 1 -r
echo
echo ""

case $REPLY in
    1)
        # Append to .env
        if [ -f .env ]; then
            echo "" >> .env
            echo "# ============================================================================" >> .env
            echo "# Credentials added by interactive_setup.sh on $(date)" >> .env
            echo "# ============================================================================" >> .env
            cat .env.setup >> .env
            echo -e "${GREEN}✓ Credentials successfully appended to .env file!${NC}"
            echo ""
            echo -e "${YELLOW}Next steps:${NC}"
            echo "1. Verify the setup:"
            echo "   ${GREEN}source .venv/bin/activate${NC}"
            echo "   ${GREEN}python scripts/verify_setup.py${NC}"
            echo "2. Test connections:"
            echo "   ${GREEN}python scripts/test_connections.py${NC}"
            echo "3. Delete .env.setup for security:"
            echo "   ${GREEN}rm .env.setup${NC}"
        else
            cp .env.setup .env
            echo -e "${GREEN}✓ Credentials saved to new .env file!${NC}"
            echo ""
            echo -e "${YELLOW}Next steps:${NC}"
            echo "1. Verify the setup:"
            echo "   ${GREEN}source .venv/bin/activate${NC}"
            echo "   ${GREEN}python scripts/verify_setup.py${NC}"
            echo "2. Test connections:"
            echo "   ${GREEN}python scripts/test_connections.py${NC}"
            echo "3. Delete .env.setup for security:"
            echo "   ${GREEN}rm .env.setup${NC}"
        fi
        ;;
    2)
        # Keep in .env.setup
        echo -e "${CYAN}✓ Credentials saved in .env.setup${NC}"
        echo ""
        echo -e "${YELLOW}To copy to .env later, run:${NC}"
        echo "  ${GREEN}cat .env.setup >> .env${NC}"
        echo "  ${GREEN}rm .env.setup${NC}"
        ;;
    3)
        # Discard
        rm .env.setup
        echo -e "${RED}✗ Credentials discarded${NC}"
        echo ""
        echo -e "${YELLOW}You'll need to run the script again to collect credentials${NC}"
        ;;
    *)
        # Invalid option - default to keep in .env.setup
        echo -e "${YELLOW}⚠ Invalid option. Credentials kept in .env.setup${NC}"
        echo ""
        echo -e "${YELLOW}To copy to .env later, run:${NC}"
        echo "  ${GREEN}cat .env.setup >> .env${NC}"
        echo "  ${GREEN}rm .env.setup${NC}"
        ;;
esac

echo ""
echo -e "${GREEN}Setup guide completed successfully!${NC}"
echo -e "${CYAN}Good luck with the hackathon! 🚀${NC}"
echo ""
