# Submission Requirements - IBM Dev Day AI Demystified Hackathon

## Deadline

**February 1, 2026 - 10:00 AM ET (HARD DEADLINE)**

All work must be completed and submitted before this time. Late submissions will NOT be accepted.

## Required Deliverables

### 1. Video Demo (REQUIRED)

**Maximum Length**: 3 minutes
**Minimum Demo Time**: 90 seconds of actual screen demonstration

#### Content Requirements

**Must Include**:
- Problem statement (what you're solving)
- Live demonstration showing watsonx Orchestrate in action
- Screen recording of your solution working
- Clear narration explaining what's happening
- Solution explanation and benefits
- Mention of watsonx Orchestrate usage

**Video Quality**:
- Clear audio (understandable narration)
- Readable screen content
- Smooth playback (no excessive lag)
- Professional presentation

#### Platform Requirements
- Upload to YouTube or Vimeo
- Set to PUBLIC (not unlisted or private)
- Provide direct link
- Test link before submission

#### Demo Script Template

```
[0:00-0:15] Introduction
"LexConductor solves complex business decisions using multi-agent AI orchestration"

[0:15-0:30] Problem Statement
"Traditional decision-making is slow, siloed, and lacks transparency"

[0:30-2:30] Live Demo (90+ seconds)
- Open watsonx Orchestrate Chat UI
- Submit business question
- Show orchestrator routing to agents
- Display each agent's analysis
- Show coordinator synthesis
- Present final decision with action plan

[2:30-2:50] Solution Benefits
"Faster decisions, multiple perspectives, transparent reasoning"

[2:50-3:00] Technology Stack
"Built with watsonx Orchestrate, watsonx.ai, and Granite models"
```

### 2. Problem & Solution Statement (REQUIRED)

**Maximum Length**: 500 words

#### Required Sections

**Problem Description**:
- What business problem are you solving?
- Why is this problem important?
- Who experiences this problem?
- Current limitations or challenges

**Solution Overview**:
- How does your solution address the problem?
- What makes your approach unique?
- Key features and capabilities
- Technology stack used

**Target Users**:
- Who will use this solution?
- What are their needs?
- How does it help them?

**Creativity & Innovation**:
- What's novel about your approach?
- How do you use watsonx Orchestrate innovatively?
- Unique multi-agent patterns
- Creative problem-solving

**Real-World Impact**:
- Business value delivered
- Measurable benefits
- Scalability potential
- Practical applications

#### Example Template

```
PROBLEM:
Complex business decisions require input from multiple domains (strategy, 
finance, risk, operations), but traditional processes are slow, siloed, and 
lack transparency. Decision-makers struggle to synthesize diverse perspectives 
efficiently, leading to delayed decisions and potential blind spots.

SOLUTION:
LexConductor is a multi-agent decision orchestration system powered by IBM 
watsonx Orchestrate. It simulates a boardroom of AI experts that collaborate 
in real-time to analyze business questions from multiple perspectives. The 
system uses specialized agents (Strategy, Finance, Risk, Operations) that 
work together through watsonx Orchestrate to provide comprehensive analysis 
and synthesized recommendations.

TARGET USERS:
- C-suite executives making strategic decisions
- Investment committees evaluating opportunities
- Business strategists planning initiatives
- Corporate development teams assessing options

INNOVATION:
Our hybrid architecture combines watsonx Orchestrate's native orchestration 
with custom external agents, enabling sophisticated business logic while 
maintaining the governance and observability of Orchestrate. Each agent is 
powered by IBM Granite models with domain-specific prompts, ensuring expert-
level analysis across all business dimensions.

IMPACT:
LexConductor reduces decision-making time from days to minutes while improving 
quality through multi-perspective analysis. The transparent reasoning trail 
enables auditable decisions and reduces bias. Organizations can make faster, 
more informed decisions with confidence.

[Word count: 198/500]
```

### 3. Agentic AI + watsonx Orchestrate Statement (REQUIRED)

**No word limit specified**

#### Required Content

**watsonx Orchestrate Usage** (CRITICAL):
- How is watsonx Orchestrate used in your solution?
- Is it the primary orchestration platform?
- What Orchestrate features do you use?
- How do you leverage the Agent Development Kit?

**Agent Inventory**:
- List ALL agents in your system
- Specify which are native vs external
- Identify the orchestrator agent

**Agent Descriptions**:
- What does each agent do?
- What domain expertise does it have?
- What analysis does it provide?
- What tools or knowledge does it use?

**Collaboration Mechanism**:
- How do agents communicate?
- What is the workflow/orchestration pattern?
- How are tasks delegated?
- How are results aggregated?

**Technology Integration**:
- How does watsonx.ai integrate? (if used)
- What models are used?
- How are prompts structured?
- What other technologies are involved?

#### Example Template

```
WATSONX ORCHESTRATE USAGE:

LexConductor uses IBM watsonx Orchestrate as the primary orchestration platform. 
A native Orchestrator Agent (lexconductor_orchestrator) manages the entire decision 
workflow, coordinating five specialized external agents through the Agent Connect 
Framework.

AGENT INVENTORY:

1. LexConductor Orchestrator (Native in watsonx Orchestrate)
2. Strategy Agent (External - FastAPI)
3. Finance Agent (External - FastAPI)
4. Risk Agent (External - FastAPI)
5. Operations Agent (External - FastAPI)
6. Coordinator Agent (External - FastAPI)

AGENT DESCRIPTIONS:

LexConductor Orchestrator:
- Receives business questions from users
- Routes requests to appropriate specialist agents
- Manages parallel execution of analyses
- Aggregates results and coordinates synthesis
- Powered by Granite 3 8B Instruct model

Strategy Agent:
- Analyzes market opportunities and competitive positioning
- Evaluates growth potential and strategic fit
- Assesses long-term implications
- Provides strategic recommendations

Finance Agent:
- Calculates ROI and financial projections
- Analyzes cost structures and capital requirements
- Evaluates financial viability
- Provides budget and resource estimates

Risk Agent:
- Identifies potential threats and uncertainties
- Assesses market volatility and operational risks
- Evaluates failure modes and mitigation strategies
- Provides risk ratings and recommendations

Operations Agent:
- Evaluates implementation feasibility
- Analyzes resource requirements and logistics
- Assesses execution constraints
- Provides operational recommendations

Coordinator Agent:
- Synthesizes analyses from all specialist agents
- Resolves conflicts between perspectives
- Generates final recommendations
- Creates actionable plans

COLLABORATION MECHANISM:

1. User submits business question via watsonx Orchestrate Chat
2. Orchestrator Agent receives and analyzes the question
3. Orchestrator delegates to all four specialist agents in parallel
4. Each specialist agent:
   - Receives request via Agent Connect Framework
   - Processes using domain-specific prompts
   - Calls watsonx.ai Granite models for reasoning
   - Returns structured analysis
5. Orchestrator collects all specialist responses
6. Orchestrator delegates to Coordinator Agent with all outputs
7. Coordinator synthesizes perspectives and generates final decision
8. Orchestrator returns complete decision package to user

TECHNOLOGY INTEGRATION:

- watsonx Orchestrate: Primary orchestration platform
- Agent Connect Framework: External agent communication
- FastAPI: External agent implementation backend
- watsonx.ai: AI inference engine
- Granite 3 8B Instruct: Foundation model for all agents
- Python 3.11+: Agent implementation language
- Pydantic: Data validation and modeling
```

### 4. Code Repository (OPTIONAL but RECOMMENDED)

**Platform**: GitHub, GitLab, or Bitbucket
**Visibility**: PUBLIC

#### Required Content

**README.md**:
- Project description
- Architecture overview
- Setup instructions
- Usage examples
- Technology stack
- Team information

**Code Structure**:
- Organized folder structure
- Clear file naming
- Commented code
- Configuration examples

**Documentation**:
- API documentation
- Agent definitions
- Integration guides
- Deployment instructions

**Security**:
- No committed secrets
- .env.example provided
- .gitignore configured
- API keys excluded

#### What to Include

```
lexconductor/
├── README.md                    # Project overview and setup
├── INTEGRATION-GUIDE.md         # Detailed integration docs
├── requirements.txt             # Python dependencies
├── .env.example                 # Configuration template
├── .gitignore                   # Exclude secrets
├── backend/                     # FastAPI implementation
│   ├── main.py
│   ├── agents/
│   └── ...
├── orchestrate/                 # watsonx Orchestrate configs
│   ├── agents/                  # YAML definitions
│   └── README.md
├── frontend/                    # UI (if applicable)
└── docs/                        # Additional documentation
```

## Submission Process

### Step-by-Step Instructions

1. **Prepare All Deliverables**
   - [ ] Video uploaded and public
   - [ ] Video link tested
   - [ ] Problem statement written
   - [ ] Agentic AI statement written
   - [ ] Repository finalized (if including)

2. **Access Submission Portal**
   - Go to BeMyApp platform
   - Navigate to "My Team" → "Submissions"

3. **Verify Team Information**
   - Confirm all team member emails are correct
   - Ensure all members received confirmation

4. **Submit Deliverables**
   - Paste video link (YouTube/Vimeo)
   - Paste problem & solution statement
   - Paste agentic AI + Orchestrate statement
   - Paste repository link (optional)

5. **Review Before Submitting**
   - Double-check all links work
   - Verify text is complete
   - Ensure video is public
   - Confirm word counts

6. **Click Submit**
   - Submit before deadline
   - Wait for confirmation email
   - Save confirmation for records

7. **Verify Submission**
   - Check confirmation email received
   - Test video link one more time
   - Keep repository public

### Resubmission Policy

- You CAN resubmit before the deadline
- Only the LAST submission is evaluated
- Must resubmit ALL deliverables (not partial)
- Can save drafts before final submission

## AI Submission Advisor

BeMyApp provides automated feedback on submissions:

**Checks**:
- Video accessibility (public link)
- Video duration (≤3 minutes)
- Narration speed (comprehensible)
- Problem clarity (within theme)
- Technical explanation completeness

**Limitations**:
- Only works with YouTube/Vimeo
- Feedback is advisory only
- Does NOT affect judging
- Helps improve submission quality

## Common Mistakes to Avoid

### Video Issues
❌ Video over 3 minutes (may be disqualified)
❌ Video not public (judges can't access)
❌ Less than 90 seconds of demo
❌ No watsonx Orchestrate shown
❌ Poor audio quality
❌ Broken link

### Documentation Issues
❌ Over 500 words in problem statement
❌ Not mentioning watsonx Orchestrate
❌ Vague agent descriptions
❌ Missing collaboration explanation
❌ No real-world impact described

### Repository Issues
❌ Private repository (judges can't access)
❌ Exposed API keys or secrets
❌ No README or setup instructions
❌ Broken or incomplete code
❌ Missing .gitignore

### Submission Issues
❌ Submitting after deadline
❌ Incomplete deliverables
❌ Wrong video link
❌ Incorrect team emails
❌ Not testing links before submit

## Verification Checklist

Before clicking Submit, verify:

### Video
- [ ] Uploaded to YouTube or Vimeo
- [ ] Set to PUBLIC visibility
- [ ] Duration ≤ 3 minutes
- [ ] Demo portion ≥ 90 seconds
- [ ] watsonx Orchestrate clearly shown
- [ ] Audio is clear and understandable
- [ ] Link tested and working

### Problem Statement
- [ ] ≤ 500 words
- [ ] Problem clearly described
- [ ] Solution explained
- [ ] Target users identified
- [ ] Innovation highlighted
- [ ] Real-world impact stated

### Agentic AI Statement
- [ ] watsonx Orchestrate usage explained
- [ ] All agents listed
- [ ] Each agent's role described
- [ ] Collaboration mechanism explained
- [ ] Technology integration detailed

### Repository (if included)
- [ ] Public visibility
- [ ] README.md complete
- [ ] No secrets committed
- [ ] .env.example provided
- [ ] Setup instructions clear
- [ ] Link tested and working

### Submission
- [ ] All team emails correct
- [ ] All deliverables ready
- [ ] Links tested
- [ ] Submitted before deadline
- [ ] Confirmation email received

## After Submission

### What Happens Next
1. Confirmation email sent to all team members
2. Judges review submissions
3. Winners announced (date TBD)
4. Prizes distributed by BeMyApp

### What to Keep
- Confirmation email
- Video link
- Repository access
- All documentation
- Screenshots of submission

### What NOT to Do
- Don't delete video
- Don't make repository private
- Don't modify deliverables after deadline
- Don't delete confirmation email

## Support

### If You Have Issues

**Technical Problems**:
- BeMyApp support: support@bemyapp.com
- IBM Dev Day Slack channels
- Hackathon mentors

**Submission Questions**:
- Check official rules document
- Review hackathon guide
- Contact BeMyApp support

**Last-Minute Issues**:
- Submit early to avoid deadline rush
- Have backup plans ready
- Keep all work saved locally

---

**Deadline Reminder**: February 1, 2026 - 10:00 AM ET
**No Extensions** - Plan to submit early!
