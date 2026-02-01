# Testing Instructions - LexConductor Demo

## ✅ DEPLOYMENT STATUS

**Backend:** ✅ DEPLOYED
- URL: https://lexconductor-agents.25rf0qd39xzz.jp-osa.codeengine.appdomain.cloud
- Status: Running with corrected Agent Connect format
- Response time: <1 second (mock responses for demo)

**Agents:** ✅ ALL IMPORTED
- Contract_Compliance_Advisor (Conductor - Native)
- fusion_agent (External)
- routing_agent (External)
- memory_agent (External)
- traceability_agent (External)

**Agent Connect Format:** ✅ FIXED
- Endpoints now return proper OpenAI chat completion format
- Messages array included for context passing
- All agents respond with structured analysis

---

## 🎯 HOW TO TEST IN WATSONX ORCHESTRATE UI

### Step 1: Access watsonx Orchestrate
1. Go to: https://eu-de.watson-orchestrate.cloud.ibm.com
2. Login with your IBM Cloud credentials
3. Navigate to Chat interface

### Step 2: Select the Agent
1. Click on the agent selector
2. Find and select: **Contract_Compliance_Advisor**
3. You should see the welcome message

### Step 3: Test with Sample Queries

**Test Query 1 (Simple NDA):**
```
Analyze this NDA: Confidentiality for 2 years. US jurisdiction.
```

**Expected Behavior:**
- Conductor should IMMEDIATELY delegate to all 4 external agents
- You should see responses from:
  - fusion_agent (Signal Fusion Analysis)
  - routing_agent (Risk Assessment & Routing)
  - memory_agent (Historical Precedents)
  - traceability_agent (Legal Logic Trace)
- Total response time: <5 seconds

**Test Query 2 (More Detailed):**
```
Review this MSA clause: "Vendor shall maintain $5M liability insurance. 
Indemnification covers direct damages only. 90-day termination notice required."
```

**Test Query 3 (Full Contract - Use sample from docs):**
```
Analyze this complete NDA:

MUTUAL NON-DISCLOSURE AGREEMENT

This Agreement is entered into as of January 31, 2026.

1. CONFIDENTIAL INFORMATION
Each party agrees to maintain confidentiality of proprietary information 
disclosed during business discussions.

2. TERM
This Agreement shall remain in effect for two (2) years from the Effective Date.

3. JURISDICTION
This Agreement shall be governed by the laws of the United States.

4. OBLIGATIONS
Receiving party shall not disclose Confidential Information to third parties 
without prior written consent.
```

---

## 🔍 WHAT TO LOOK FOR

### ✅ SUCCESS INDICATORS:
1. **Conductor delegates immediately** - No asking for more information
2. **All 4 agents respond** - You see output from fusion, routing, memory, traceability
3. **Fast response** - Complete analysis in <10 seconds
4. **Structured output** - Clear sections for each agent's contribution
5. **No errors** - No "Invalid JSON" or connection errors

### ❌ FAILURE INDICATORS:
1. Conductor asks "What is the full NDA text?" - Should NOT happen anymore
2. "Transferring to fusion_agent" but no response - Agent Connect issue
3. Timeout errors - Backend not responding
4. "Invalid JSON output" - Format issue (should be fixed now)

---

## 🐛 TROUBLESHOOTING

### If Conductor Asks for More Info:
- The instructions update may not have taken effect
- Try: `orchestrate agents import --file agents/conductor_agent.yaml` again
- Wait 1-2 minutes for cache to clear

### If External Agents Don't Respond:
1. Check backend is running:
   ```bash
   curl https://lexconductor-agents.25rf0qd39xzz.jp-osa.codeengine.appdomain.cloud/health
   ```

2. Test fusion agent directly:
   ```bash
   curl -X POST https://lexconductor-agents.25rf0qd39xzz.jp-osa.codeengine.appdomain.cloud/fusion/v1/chat \
     -H "Content-Type: application/json" \
     -d '{"messages":[{"role":"user","content":"Test"}],"stream":false}'
   ```

3. Reimport external agents:
   ```bash
   orchestrate env activate prod
   orchestrate agents import --file agents/fusion_agent_external.yaml
   orchestrate agents import --file agents/routing_agent_external.yaml
   orchestrate agents import --file agents/memory_agent_external.yaml
   orchestrate agents import --file agents/traceability_agent_external.yaml
   ```

### If Response is Slow:
- Mock responses should be <1 second
- If slow, check Code Engine logs:
  ```bash
  ibmcloud ce application logs --name lexconductor-agents --follow
  ```

---

## 📹 VIDEO DEMO PREPARATION

### Demo Script (90+ seconds):

**[0:00-0:15] Introduction**
"LexConductor is a multi-agent AI system for legal contract analysis, powered by IBM watsonx Orchestrate."

**[0:15-0:30] Show watsonx Orchestrate UI**
- Open Chat interface
- Show Contract_Compliance_Advisor agent selected
- Explain: "This conductor agent orchestrates 4 specialized external agents"

**[0:30-2:00] Live Demo (90 seconds)**
1. Paste NDA query
2. Show conductor delegating to agents
3. Highlight each agent's response:
   - Fusion Agent: Compliance gaps detected
   - Routing Agent: Risk assessment and workflow routing
   - Memory Agent: Historical precedents found
   - Traceability Agent: Decision provenance
4. Show final synthesized recommendation

**[2:00-2:30] Explain Architecture**
- "Hybrid architecture: Native conductor + External agents"
- "External agents run on Code Engine, powered by Granite models"
- "Agent Connect Framework enables seamless communication"

**[2:30-3:00] Value Proposition**
- "Faster contract review: Minutes instead of hours"
- "Transparent reasoning: Full audit trail"
- "Compliance confidence: Multi-perspective analysis"

---

## 🎬 RECORDING TIPS

1. **Clear Screen**: Close unnecessary tabs/windows
2. **Zoom In**: Make text readable (Cmd/Ctrl + +)
3. **Slow Down**: Pause between steps so viewers can read
4. **Narrate**: Explain what's happening as you demo
5. **Show Orchestrate**: Make sure watsonx Orchestrate branding is visible
6. **Highlight Agents**: Point out when each agent responds
7. **Keep Time**: Aim for 2:30-2:45 to stay under 3 minutes

---

## ✅ PRE-DEMO CHECKLIST

- [ ] Backend is running (check health endpoint)
- [ ] All agents imported successfully
- [ ] Conductor instructions updated (no asking for more info)
- [ ] Test query works end-to-end
- [ ] Response time is acceptable (<10s)
- [ ] Screen recording software ready
- [ ] Browser zoom level appropriate
- [ ] Sample queries prepared
- [ ] Narration script ready

---

## 🚨 CRITICAL REMINDERS

- **Deadline**: February 1, 2026 - 10:00 AM ET (~10 hours remaining!)
- **Video**: Must be ≤3 minutes with ≥90 seconds of demo
- **Platform**: Must show watsonx Orchestrate clearly
- **Agents**: Must demonstrate multi-agent collaboration
- **Upload**: YouTube or Vimeo, set to PUBLIC

---

## 📞 SUPPORT

If issues persist:
1. Check deployment logs: `ibmcloud ce application logs --name lexconductor-agents`
2. Verify agent status: `orchestrate agents list`
3. Test endpoints directly with curl
4. Review error messages carefully

**Last Updated**: January 31, 2026 - 23:30 JST
**Status**: READY FOR DEMO ✅
