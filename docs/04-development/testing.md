# Testing Guide

Complete testing strategy and guidelines for Lex Conductor.

## Testing Philosophy

- **Test Early**: Write tests as you develop
- **Test Often**: Run tests frequently
- **Test Thoroughly**: Cover edge cases
- **Test Realistically**: Use realistic data

## Test Structure

```
tests/
├── unit/              # Unit tests (fast, isolated)
│   ├── test_agents.py
│   └── test_utils.py
├── integration/       # Integration tests (slower, dependencies)
│   ├── test_orchestrate.py
│   └── test_watsonx.py
└── e2e/              # End-to-end tests (slowest, full system)
    └── test_workflows.py
```

## Running Tests

### All Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Specific Tests

```bash
# Run unit tests only
pytest tests/unit/

# Run specific test file
pytest tests/unit/test_agents.py

# Run specific test function
pytest tests/unit/test_agents.py::test_conductor_agent

# Run tests matching pattern
pytest -k "conductor"
```

### Test Options

```bash
# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l

# Run last failed tests
pytest --lf

# Run tests in parallel
pytest -n auto
```

## Unit Testing

### Example Unit Test

```python
import pytest
from src.agents.conductor import ConductorAgent

def test_conductor_initialization():
    """Test conductor agent initializes correctly."""
    agent = ConductorAgent()
    assert agent is not None
    assert agent.name == "conductor-agent"

def test_conductor_routing():
    """Test conductor routes queries correctly."""
    agent = ConductorAgent()
    query = "Analyze market expansion"
    
    result = agent.route_query(query)
    
    assert result["status"] == "success"
    assert "routing" in result
    assert len(result["agents"]) > 0

@pytest.mark.parametrize("query,expected_agents", [
    ("Analyze market", ["routing", "memory"]),
    ("Get history", ["memory"]),
    ("Synthesize results", ["fusion"]),
])
def test_conductor_agent_selection(query, expected_agents):
    """Test conductor selects appropriate agents."""
    agent = ConductorAgent()
    result = agent.select_agents(query)
    assert set(result) == set(expected_agents)
```

### Mocking External Dependencies

```python
from unittest.mock import Mock, patch
import pytest

@patch('src.agents.conductor.orchestrate_client')
def test_conductor_with_mock(mock_client):
    """Test conductor with mocked Orchestrate client."""
    # Setup mock
    mock_client.call_agent.return_value = {
        "status": "success",
        "result": "mocked response"
    }
    
    # Test
    agent = ConductorAgent(client=mock_client)
    result = agent.process_query("test query")
    
    # Verify
    assert result["status"] == "success"
    mock_client.call_agent.assert_called_once()
```

## Integration Testing

### Testing with watsonx Orchestrate

```python
import pytest
from src.integrations.orchestrate import OrchestrateClient

@pytest.mark.integration
def test_orchestrate_connection():
    """Test connection to watsonx Orchestrate."""
    client = OrchestrateClient()
    status = client.check_connection()
    assert status["connected"] is True

@pytest.mark.integration
def test_agent_deployment():
    """Test agent can be deployed to Orchestrate."""
    client = OrchestrateClient()
    result = client.deploy_agent("conductor-agent")
    assert result["status"] == "deployed"

@pytest.mark.integration
@pytest.mark.slow
def test_agent_execution():
    """Test agent executes successfully."""
    client = OrchestrateClient()
    response = client.execute_agent(
        "conductor-agent",
        {"query": "test query"}
    )
    assert response["status"] == "success"
    assert "result" in response
```

### Testing Agent Collaboration

```python
@pytest.mark.integration
async def test_multi_agent_workflow():
    """Test multiple agents working together."""
    conductor = ConductorAgent()
    
    # Execute workflow
    result = await conductor.execute_workflow({
        "query": "Analyze market expansion",
        "agents": ["routing", "memory", "fusion"]
    })
    
    # Verify all agents responded
    assert len(result["agent_responses"]) == 3
    assert result["final_decision"] is not None
```

## End-to-End Testing

### Full Workflow Test

```python
@pytest.mark.e2e
@pytest.mark.slow
async def test_complete_decision_workflow():
    """Test complete decision-making workflow."""
    # Setup
    query = "Should we expand into the European market?"
    
    # Execute
    conductor = ConductorAgent()
    result = await conductor.process_decision(query)
    
    # Verify
    assert result["status"] == "success"
    assert result["decision"] is not None
    assert result["reasoning"] is not None
    assert result["confidence"] > 0.7
    assert len(result["agent_analyses"]) >= 4
```

## Test Fixtures

### Common Fixtures

```python
import pytest
from src.agents.conductor import ConductorAgent

@pytest.fixture
def conductor_agent():
    """Provide a conductor agent instance."""
    return ConductorAgent()

@pytest.fixture
def sample_query():
    """Provide a sample query."""
    return {
        "text": "Analyze market expansion",
        "context": {"user_id": "test-user"},
        "metadata": {"priority": "high"}
    }

@pytest.fixture
def mock_orchestrate_client():
    """Provide a mocked Orchestrate client."""
    with patch('src.integrations.orchestrate.OrchestrateClient') as mock:
        yield mock

# Use fixtures in tests
def test_with_fixtures(conductor_agent, sample_query):
    """Test using fixtures."""
    result = conductor_agent.process(sample_query)
    assert result is not None
```

## Test Configuration

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (slower, dependencies)
    e2e: End-to-end tests (slowest, full system)
    slow: Slow tests (skip by default)

addopts =
    -v
    --strict-markers
    --tb=short
    --cov=src
    --cov-report=term-missing
    --cov-report=html
```

### Running by Marker

```bash
# Run only unit tests
pytest -m unit

# Run integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# Run unit and integration, skip e2e
pytest -m "unit or integration"
```

## Coverage Requirements

### Target Coverage
- **Overall**: >80%
- **Critical paths**: >90%
- **New code**: 100%

### Check Coverage

```bash
# Generate coverage report
pytest --cov=src --cov-report=term-missing

# Generate HTML report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Fail if coverage below threshold
pytest --cov=src --cov-fail-under=80
```

## Performance Testing

### Response Time Tests

```python
import time
import pytest

@pytest.mark.performance
def test_conductor_response_time():
    """Test conductor responds within acceptable time."""
    agent = ConductorAgent()
    query = "test query"
    
    start = time.time()
    result = agent.process(query)
    duration = time.time() - start
    
    assert duration < 10.0  # Must respond in <10 seconds
    assert result["status"] == "success"

@pytest.mark.performance
@pytest.mark.parametrize("num_queries", [1, 10, 100])
def test_throughput(num_queries):
    """Test system throughput."""
    agent = ConductorAgent()
    
    start = time.time()
    for i in range(num_queries):
        agent.process(f"query {i}")
    duration = time.time() - start
    
    throughput = num_queries / duration
    assert throughput > 1.0  # At least 1 query/second
```

## Testing Best Practices

### Do's
- ✅ Write tests for new features
- ✅ Test edge cases
- ✅ Use descriptive test names
- ✅ Keep tests independent
- ✅ Mock external dependencies
- ✅ Test error handling
- ✅ Maintain high coverage

### Don'ts
- ❌ Don't test implementation details
- ❌ Don't write flaky tests
- ❌ Don't skip failing tests
- ❌ Don't test third-party code
- ❌ Don't make tests dependent on each other
- ❌ Don't ignore test failures

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v2
```

## Troubleshooting Tests

### Tests Failing Locally

```bash
# Clear pytest cache
pytest --cache-clear

# Run with more verbose output
pytest -vv

# Show print statements
pytest -s

# Drop into debugger on failure
pytest --pdb
```

### Tests Pass Locally but Fail in CI

- Check Python version consistency
- Verify all dependencies installed
- Check environment variables
- Review test isolation
- Check for timing issues

## Related Documentation

- [Local Setup](./local-setup.md)
- [Deployment](./deployment.md)
- [Agent Architecture](../03-agents/agent-architecture.md)

---

**Test Framework**: pytest  
**Coverage Tool**: pytest-cov  
**Target Coverage**: >80%
