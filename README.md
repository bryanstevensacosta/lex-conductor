<div align="center">

# IBM Dev Day: AI Demystified Hackathon

<img src="https://v.fastcdn.co/t/0bc8903d/3c2af0ae/1765713579-65752783-649x258x649x258x0x1-Be-my-app-Virtual-de.png" alt="IBM Logo" width="200"/>

### Team **AI Kings** 👑

**Building the Future with Agentic AI**

[![IBM watsonx](https://img.shields.io/badge/IBM-watsonx_Orchestrate-0f62fe?style=for-the-badge&logo=ibm)](https://www.ibm.com/watsonx)
[![Hackathon](https://img.shields.io/badge/Hackathon-AI_Demystified-00539a?style=for-the-badge)](https://bemyapp.com/)
[![Deadline](https://img.shields.io/badge/Deadline-Feb_1_10AM_ET-red?style=for-the-badge)](https://bemyapp.com/)

</div>

---

## 💡 Project: Lex Conductor

Multi-agent decision orchestration system powered by IBM watsonx Orchestrate.

**Key Features**:
- 🎯 Multi-perspective business analysis (Strategy, Finance, Risk, Operations)
- 🤖 Hybrid architecture (Native + External agents)
- 🧠 IBM Granite models for AI reasoning
- 📊 Transparent decision trails

**Documentation**:
- 📋 [Product Requirements](docs/impl/PRD.md)
- 🏗️ [Architecture Overview](docs/impl/Arch.md)
- 🔧 [Technical Details](docs/impl/Technical.md)
- 🚀 [Integration Guide](docs/impl/INTEGRATION-GUIDE.md)

---

## 🎯 Hackathon Overview

**Event**: IBM Dev Day: AI Demystified  
**Format**: Virtual Event + Hackathon  
**Theme**: "From idea to deployment"  
**Event Date**: January 29, 2026  
**Hackathon Period**: January 30 - February 1, 2026  
**Submission Deadline**: **February 1, 2026 - 10:00 AM ET** ⏰

### Event Highlights
- 🎓 **19 Hours** of programming content
- 🛠️ **3 Technical Tracks** covering AI development
- 💰 **$10,000** in prizes up for grabs
- 🚀 Apply your learning and compete in the hackathon

### Critical Requirements
- ✅ **IBM watsonx Orchestrate** (MANDATORY)
- ✅ Multi-agent AI collaboration
- ✅ Video demo (≤3 min, ≥90s showing Orchestrate)
- ✅ Problem & solution statement (≤500 words)
- ✅ Agentic AI technical statement

---

## 📁 Repository Structure

```
lex-conductor/
├── docs/                        # 📚 Complete documentation
│   ├── 01-getting-started/      # Setup and prerequisites
│   ├── 02-project/              # Project overview and architecture
│   ├── 03-agents/               # Agent documentation and definitions
│   ├── 04-development/          # Development guides
│   ├── 05-integration/          # watsonx integration
│   ├── 06-hackathon/            # Hackathon requirements
│   └── 07-infrastructure/       # Infrastructure and security
├── terraform/                   # ☁️ Infrastructure as code
├── .env.example                 # Environment template
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### 📚 Documentation Map

| Document | Purpose | Location |
|----------|---------|----------|
| **Documentation Index** | Complete documentation overview | [`docs/README.md`](docs/README.md) |
| **Getting Started** | Setup and prerequisites | [`docs/01-getting-started/`](docs/01-getting-started/) |
| **Project Overview** | Architecture, PRD, technical specs | [`docs/02-project/`](docs/02-project/) |
| **Agents** | Agent documentation and YAML definitions | [`docs/03-agents/`](docs/03-agents/) |
| **Development** | Development guides and testing | [`docs/04-development/`](docs/04-development/) |
| **Integration** | watsonx Orchestrate and AI setup | [`docs/05-integration/`](docs/05-integration/) |
| **Hackathon** | Submission requirements and compliance | [`docs/06-hackathon/`](docs/06-hackathon/) |
| **Infrastructure** | IBM Cloud and Terraform setup | [`docs/07-infrastructure/`](docs/07-infrastructure/) |


--- 

| Document | Purpose | Location |
|----------|---------|----------|
| **Hackathon Guide** | Event details, requirements, judging | [`.kiro/steering/hackathon.md`](.kiro/steering/hackathon.md) |
| **Submission Guide** | Deliverables, templates, process | [`.kiro/steering/submission.md`](.kiro/steering/submission.md) |
| **Compliance Rules** | Eligibility, code of conduct | [`.kiro/steering/compliance.md`](.kiro/steering/compliance.md) |
| **Technical Resources** | Tools, frameworks, setup | [`.kiro/steering/tech.md`](.kiro/steering/tech.md) |
| **Implementation Docs** | Architecture, PRD, technical specs | [`docs/impl/`](docs/impl/) |
| **Orchestrate Setup** | Agent definitions, deployment | [`docs/orchestrate/`](docs/orchestrate/) |

---

## 🚀 Quick Start

### 1️⃣ Review Documentation
```bash
# Start here:
1. docs/README.md                        # Documentation index
2. docs/02-project/overview.md           # Project overview
3. docs/06-hackathon/requirements.md     # Hackathon requirements
```

### 2️⃣ Setup Environment
```bash
# IBM Cloud account
- Accept team invitation email
- Access watsonx Orchestrate
- Verify $100 credits

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# 📖 Detailed Setup Guides:
# English: docs/IBM_CLOUD_SETUP.md
# Español: docs/GUIA_CREDENCIALES_ES.md (Guía completa)
# Español: docs/GUIA_RAPIDA_ES.md (Guía rápida - 35 min)
```

### 3️⃣ Deploy & Test
```bash
# Deploy agents to watsonx Orchestrate
cd docs/03-agents/agent-definitions/
orchestrate agents import -f conductor_agent.yaml
# Import other agents...

# Test the system
orchestrate chat --agent conductor-agent

# Follow detailed guide
# See docs/05-integration/
```

### 4️⃣ Submit
- 📹 Record video demo (≤3 min, ≥90s showing Orchestrate)
- 📝 Write problem statement (≤500 words)
- 🤖 Write agentic AI statement
- ✅ Follow checklist in [`docs/06-hackathon/checklist.md`](docs/06-hackathon/checklist.md)

---

## 🏆 Judging Criteria

| Criterion | Points | Focus |
|-----------|--------|-------|
| **Completeness & Feasibility** | 5 | Functional, realistic, watsonx Orchestrate integration |
| **Effectiveness & Efficiency** | 5 | Solves problem, good performance, practical |
| **Design & Usability** | 5 | User-friendly, professional, clear UX |
| **Creativity & Innovation** | 5 | Novel approach, unique patterns, real value |

**Minimum Score**: 12.5/20 points required for prizes

---

## 📚 Resources

### IBM Technologies
- [watsonx Orchestrate Documentation](https://www.ibm.com/docs/en/watson-orchestrate)
- [Agent Development Kit (ADK)](https://developer.watson-orchestrate.ibm.com/)
- [watsonx.ai Platform](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [IBM Granite Models](https://www.ibm.com/granite)

### Support Channels
- 💬 **Slack**: IBM Dev Day #watsonx-orchestrate
- � **Email**: support@bemyapp.com
- 👥 **Mentors**: Available via BeMyApp platform

### Useful Links
- [BeMyApp Platform](https://bemyapp.com/)
- [Hackathon Official Page](https://bemyapp.com/)
- [IBM Cloud Console](https://cloud.ibm.com/)

---

## ⚠️ Critical Reminders

### ✅ MUST DO
- Use IBM watsonx Orchestrate (MANDATORY)
- Submit before Feb 1, 10:00 AM ET
- Video ≤3 min with ≥90s demo showing Orchestrate
- Problem statement ≤500 words
- Make repository public
- Remove all secrets/API keys

### ❌ MUST NOT DO
- Use prohibited data (PII, client data, social media)
- Expose API keys in public repos
- Submit after deadline
- Work before contest period (Jan 30)
- Use prohibited models (llama-3-405b, mistral-medium-2505, mistral-small-3-1-24b)
- Violate code of conduct

---

## 📅 Timeline

| Date | Event |
|------|-------|
| **Jan 29** | 🎓 IBM Dev Day event (19 hours of programming) |
| **Jan 30** | 🚀 Hackathon work period begins |
| **Jan 30 - Feb 1** | 💻 Build your solution (3 days) |
| **Feb 1, 10:00 AM ET** | 🚨 **SUBMISSION DEADLINE** |
| **Feb 4** | ☁️ IBM Cloud accounts close |
| **Feb 25** | 📊 Feedback survey closes |

---

## 💰 Prizes & Recognition

### Total Prize Pool: $10,000 USD

- 🥇 **1st Place**: $5,000 USD
- 🥈 **2nd Place**: $3,000 USD
- 🥉 **3rd Place**: $2,000 USD

**Plus**: IBM Digital Badges, networking opportunities, potential acceleration program participation

---

## 📝 Project Progress

- [x] Repository structure organized
- [x] Documentation created
- [x] Project architecture defined
- [x] Agent designs completed
- [x] Environment setup complete
- [x] Backend implementation
- [x] Agents deployed to Orchestrate
- [x] End-to-end testing
- [x] Video demo recorded
- [x] Submission statements written
- [x] Final submission completed

---

## 🔐 Security Notes

- All API keys stored in `.env` (never committed)
- `.gitignore` configured properly
- `.env.example` provided as template
- No secrets in public repository
- Regular credential rotation recommended

---

<div align="center">

### Built with ❤️ by Team AI Kings

| Member | Role | LinkedIn | GitHub | Others |
|--------|------|----------|--------|---------|
| **Bryan Stevens Nuñez Acosta** | Team Lead | [LinkedIn](https://linkedin.com/in/bryan-stevens-acosta) | [GitHub](https://github.com/bryanstevensacosta) | [Portfolio/Website](https://bryanacosta.vercel.app) |
| **Umer Ahmed** | Team PM | [LinkedIn](https://www.linkedin.com/in/umerahmed245/) | [GitHub](https://github.com/umerahmed245) | [Portfolio/Website](https://flowcv.me/umer-ahmed) |
| **David Adenuga** | Team Member | [LinkedIn](https://www.linkedin.com/in/adenuga-david-chemicalengineering/) | [GitHub]((https://github.com/Nuga-D)) |
| **Samuel Akinnusi** | Team Member | [LinkedIn](https://www.linkedin.com/in/samuel-akinnusi-487255193/) | [GitHub](https://github.com/Samiozy) |


> 💡 **Team Philosophy**: Leveraging collective intelligence through AI orchestration to solve complex business challenges.

---

<img src="https://www.ibm.com/brand/experience-guides/developer/b1db1ae501d522a1a4b49613fe07c9f4/02_8-bar-reverse.svg" alt="IBM Logo" width="150"/>

**Powered by IBM watsonx Orchestrate**

---

**Last Updated**: January 30, 2026  
**License**: MIT 
**Status**: 🚧 Active Development

</div>
