# LexConductor Demo Script
**IBM Dev Day AI Demystified Hackathon 2026**  
**Team**: AI Kings 👑  
**Duration**: ≤3 minutes (≥90 seconds showing watsonx Orchestrate)

---

## 🎬 Video Structure

### [0:00-0:20] Introduction (20 seconds)
**Visual**: Title slide or talking head  
**Script**:

> "Hi, I'm from Team AI Kings. We built LexConductor - a multi-agent AI system that revolutionizes legal contract review using IBM watsonx Orchestrate. Let me show you how it works."

---

### [0:20-0:35] Problem Statement (15 seconds)
**Visual**: Simple diagram or text overlay  
**Script**:

> "Legal teams spend hours reviewing contracts manually, checking for compliance gaps, risks, and precedents. This process is slow, inconsistent, and prone to human error. LexConductor solves this with AI-powered multi-agent collaboration."

---

### [0:35-2:45] Live Demo - watsonx Orchestrate (130 seconds) ⭐
**Visual**: Screen recording of watsonx Orchestrate Chat UI  
**Script**:

#### Step 1: Access watsonx Orchestrate (10 seconds)
> "I'm now in IBM watsonx Orchestrate. This is where all our AI agents live and collaborate."

**Actions**:
- Show watsonx Orchestrate dashboard
- Navigate to Chat interface
- Show LexConductor Orchestrator agent

#### Step 2: Submit Contract for Analysis (15 seconds)
> "Let me submit a Non-Disclosure Agreement for analysis. I'll paste the contract text here."

**Actions**:
- Click on LexConductor Orchestrator
- Paste sample NDA contract:
```
"MUTUAL NON-DISCLOSURE AGREEMENT

This Agreement is entered into as of January 15, 2026, between TechCorp Inc. 
and DataSystems LLC (the 'Parties').

1. CONFIDENTIAL INFORMATION
The Parties agree to maintain confidentiality of all proprietary information 
disclosed during business discussions for a period of 2 years from the date 
of disclosure.

2. OBLIGATIONS
The receiving party shall not disclose such information to any third party 
without prior written consent. The receiving party may share information 
with employees on a need-to-know basis.

3. EXCLUSIONS
This agreement does not apply to information that is publicly available or 
independently developed.

4. TERM
This agreement shall remain in effect for 2 years from the effective date."
```
- Click Send/Submit

#### Step 3: Show Orchestrator Routing (20 seconds)
> "Watch as the Orchestrator Agent analyzes the contract and routes it to our specialist agents. It's classifying this as a STANDARD complexity contract and delegating to four expert agents in parallel."

**Actions**:
- Show Orchestrator's response
- Highlight routing decision
- Show that multiple agents are being called

#### Step 4: Show Agent Collaboration (30 seconds)
> "Now our four specialist agents are working together:
> - The Fusion Agent correlates signals across compliance, risk, and legal domains
> - The Memory Agent retrieves relevant historical precedents
> - The Routing Agent confirms risk classification
> - The Traceability Agent generates the legal reasoning trail"

**Actions**:
- Show each agent's response appearing
- Highlight key findings from each agent
- Show structured outputs

#### Step 5: Show Final Legal Logic Trace (40 seconds)
> "And here's the complete Legal Logic Trace. It shows:
> - Compliance gaps detected: Missing data breach notification clause
> - Risk level: MEDIUM due to 2-year term and employee sharing provisions
> - Historical precedents: 3 similar NDAs with recommended improvements
> - Actionable recommendations: Add breach notification, clarify employee obligations, extend term to 3 years
> 
> All of this analysis happened in under 10 seconds, with full transparency and traceability."

**Actions**:
- Scroll through complete Legal Logic Trace
- Highlight key sections:
  - Signal Correlation results
  - Compliance gaps
  - Risk assessment
  - Historical precedents
  - Recommendations
- Show timestamp/performance metrics

#### Step 6: Explain Architecture (15 seconds)
> "This is powered by a hybrid architecture: a native Orchestrator Agent in watsonx Orchestrate coordinating four external agents running on IBM Code Engine, all using IBM Granite 3 models for AI reasoning."

**Actions**:
- Show architecture diagram (if time permits)
- Or just explain while showing the agents list

---

### [2:45-3:00] Closing & Impact (15 seconds)
**Visual**: Summary slide or talking head  
**Script**:

> "LexConductor reduces contract review time from hours to seconds, provides consistent analysis, and creates an auditable decision trail. Built entirely with IBM watsonx Orchestrate and Granite models. Thank you!"

**Visual**: End screen with:
- Team name: AI Kings 👑
- Project: LexConductor
- Tech: watsonx Orchestrate + Granite 3
- GitHub: [your repo URL]

---

## 📝 Key Points to Emphasize

### watsonx Orchestrate Usage (CRITICAL)
- ✅ Show the Orchestrate Chat UI clearly (≥90 seconds)
- ✅ Mention "watsonx Orchestrate" multiple times
- ✅ Show agent collaboration happening in Orchestrate
- ✅ Demonstrate it's the central orchestration platform

### Multi-Agent Collaboration
- ✅ Show Orchestrator routing to specialists
- ✅ Show parallel agent execution
- ✅ Show aggregated results
- ✅ Explain each agent's role

### Innovation
- ✅ Hybrid architecture (native + external agents)
- ✅ Signal Fusion methodology
- ✅ Legal Logic Trace for explainability
- ✅ Real business value

### Technical Excellence
- ✅ IBM Granite 3 models
- ✅ Fast performance (<10s)
- ✅ Structured outputs
- ✅ Production-ready deployment

---

## 🎥 Recording Tips

### Before Recording
- [ ] Test the workflow end-to-end
- [ ] Prepare the sample contract (copy-paste ready)
- [ ] Clear browser cache/cookies
- [ ] Close unnecessary tabs
- [ ] Set screen resolution to 1920x1080
- [ ] Test audio levels
- [ ] Practice the script 2-3 times

### During Recording
- [ ] Speak clearly and at moderate pace
- [ ] Show mouse cursor for clarity
- [ ] Pause briefly between sections
- [ ] Keep energy level high
- [ ] Smile (even if not on camera - it affects voice)

### After Recording
- [ ] Verify video is ≤3 minutes
- [ ] Verify ≥90 seconds shows Orchestrate
- [ ] Check audio quality
- [ ] Verify screen is readable
- [ ] Upload to YouTube as PUBLIC
- [ ] Test the link

---

## 🚨 Common Mistakes to Avoid

❌ Going over 3 minutes (DISQUALIFICATION)
❌ Less than 90 seconds of Orchestrate demo
❌ Poor audio quality
❌ Unreadable screen text
❌ Not mentioning watsonx Orchestrate
❌ Video not public
❌ Broken YouTube link

---

## 📋 Sample Contracts for Testing

### Option 1: Simple NDA (ROUTINE)
```
"Basic Non-Disclosure Agreement: The parties agree to keep confidential 
information secret for 1 year. Standard terms apply."
```

### Option 2: Standard NDA (STANDARD) - RECOMMENDED
```
[Use the full NDA from Step 2 above]
```

### Option 3: Complex M&A (COMPLEX)
```
"MERGER AND ACQUISITION AGREEMENT

This Agreement governs the acquisition of TargetCo by AcquirerCo for 
$50M, subject to regulatory approval, due diligence, and shareholder 
consent. The transaction includes intellectual property transfer, 
employee retention provisions, earn-out clauses based on performance 
metrics, and indemnification for undisclosed liabilities. Closing 
is contingent on antitrust clearance and third-party consents."
```

---

## ⏱️ Timing Breakdown

| Section | Duration | Cumulative |
|---------|----------|------------|
| Introduction | 20s | 0:20 |
| Problem | 15s | 0:35 |
| **Orchestrate Demo** | **130s** | **2:45** |
| Closing | 15s | 3:00 |

**Total**: 180 seconds (3:00 minutes) ✅  
**Orchestrate shown**: 130 seconds (72%) ✅

---

## 🎯 Success Criteria

After recording, verify:
- [ ] Duration ≤ 3:00 minutes
- [ ] Orchestrate shown ≥ 90 seconds
- [ ] Audio is clear and understandable
- [ ] Screen text is readable
- [ ] watsonx Orchestrate mentioned multiple times
- [ ] All agents shown working
- [ ] Legal Logic Trace displayed
- [ ] Professional presentation
- [ ] Video uploaded to YouTube (PUBLIC)
- [ ] Link tested and working

---

**Good luck with the recording! 🎬**

**Remember**: Quality > Perfection. A working demo is better than a perfect script.

---

**Team**: AI Kings 👑  
**Project**: LexConductor  
**Hackathon**: IBM Dev Day AI Demystified 2026  
**Deadline**: Feb 1, 2026 - 10:00 AM ET
