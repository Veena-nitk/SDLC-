"""
UML Modeling Agent
──────────────────
Generates clean, syntax-valid Mermaid UML diagrams for:
1. Use Case Diagram
2. Domain Class Diagram
3. Transaction Sequence Diagram
4. Activity Diagram (Workflow & Decision Flow)
5. State Machine Diagram (Entity Lifecycle)
"""

from .base_agent import BaseAgent

SYSTEM_INSTRUCTION = """\
You are a **Software Architecture & UML Specialist**.

Given a software project description and its requirements, you MUST generate exactly 5 distinct,
clean, standard UML diagrams using Mermaid syntax:

1. **Use Case Diagram**: Primary and secondary actors (Customer, Underwriter, System Admin, External Service) and essential use cases.
2. **Domain Class Diagram**: Core entities, data fields, methods, and relationships.
3. **Transaction Sequence Diagram**: Step-by-step sequential message flow between actor, API gateway, core processing service, verification service, database ledger, and audit logger.
4. **Activity Diagram**: Workflow flowchart showing process start, action steps, decision diamonds with conditions ([Yes]/[No]), validation branches, and end terminal.
5. **State Machine Diagram**: The explicit lifecycle states of the application or entity from initiation ([*] -> Draft) through verification, review, approval, settlement, to final state ([*]).

Ensure Sequence and Activity diagrams are completely separate diagrams with their own headers and separate fenced ```mermaid code blocks. Ensure all node IDs and labels strictly adhere to valid Mermaid syntax.
"""


class UMLDiagramAgent(BaseAgent):
    """Produces Use Case, Class, Sequence, Activity, and State Machine UML diagrams."""

    def __init__(self):
        super().__init__(
            name="System Architect",
            role="UML Architectural Modeling",
            system_instruction=SYSTEM_INSTRUCTION,
        )

    def run(self, input_text: str) -> str:
        prompt = (
            f"Generate 5 distinct Mermaid UML diagrams:\n"
            f"1. Use Case Diagram\n"
            f"2. Domain Class Diagram\n"
            f"3. Transaction Sequence Diagram\n"
            f"4. Activity Diagram\n"
            f"5. State Machine Diagram\n\n"
            f"Requirements:\n"
            f"---\n{input_text}\n---"
        )
        return self._call_llm(prompt)

    def _expert_fallback(self, prompt: str) -> str:
        return """\
### 1. Use Case Diagram

```mermaid
graph TD
    classDef actorStyle fill:#2d3748,stroke:#cbd5e0,stroke-width:2px,color:#fff;
    classDef usecaseStyle fill:#f7f4ee,stroke:#70472d,stroke-width:2px,color:#241e19;

    Customer["Customer / User"]:::actorStyle
    Officer["Underwriter / Specialist"]:::actorStyle
    Admin["System Administrator"]:::actorStyle
    ExternalBureau["External Bureau / API"]:::actorStyle
    CoreSystem["Core Processing Ledger"]:::actorStyle

    UC1(["Submit Application"]):::usecaseStyle
    UC2(["Upload & Verify Identity"]):::usecaseStyle
    UC3(["Run Automated Risk Scoring"]):::usecaseStyle
    UC4(["Step-up MFA Authentication"]):::usecaseStyle
    UC5(["Manual Review & Escalation"]):::usecaseStyle
    UC6(["Disburse Approved Funds"]):::usecaseStyle
    UC7(["Generate Compliance Audit Log"]):::usecaseStyle

    Customer --> UC1
    Customer --> UC4
    UC1 -.->|includes| UC2
    UC1 -.->|includes| UC3
    UC3 --> ExternalBureau
    UC1 -.->|conditional threshold| UC4
    UC3 -.->|high risk score| UC5
    Officer --> UC5
    UC5 --> UC6
    UC6 --> CoreSystem
    Admin --> UC7
```

---

### 2. Domain Class Diagram

```mermaid
classDiagram
    class User {
        +UUID userId
        +String fullName
        +String email
        +String kycStatus
        +DateTime registeredAt
        +verifyIdentity() bool
    }

    class ApplicationRequest {
        +UUID requestId
        +UUID userId
        +Decimal requestedAmount
        +String status
        +DateTime createdAt
        +submitRequest() void
        +updateStatus(String newStatus) void
    }

    class VerificationCheck {
        +UUID checkId
        +UUID requestId
        +String checkType
        +Float confidenceScore
        +String outcomeResult
        +runAutomatedCheck() bool
    }

    class RiskAssessment {
        +UUID assessmentId
        +UUID requestId
        +int creditScore
        +int computedRiskScore
        +String decisionTier
        +evaluateEligibility() bool
    }

    class TransactionSettlement {
        +UUID transactionId
        +UUID requestId
        +Decimal settledAmount
        +String referenceCode
        +DateTime settledAt
        +executeSettlement() bool
    }

    class AuditLogEntry {
        +UUID logId
        +String actionTaken
        +String actorRole
        +String recordHash
        +DateTime timestamp
        +verifyTamperIntegrity() bool
    }

    User "1" *-- "0..*" ApplicationRequest : initiates
    ApplicationRequest "1" *-- "1..*" VerificationCheck : validated_by
    ApplicationRequest "1" *-- "1" RiskAssessment : evaluated_by
    ApplicationRequest "1" --> "0..1" TransactionSettlement : settles_via
    ApplicationRequest "1" ..> "1..*" AuditLogEntry : logged_in
```

---

### 3. Transaction Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor U as Customer / User
    participant GW as API Gateway
    participant SVC as Core Processing Service
    participant VER as Verification & Bureau Svc
    participant SEC as Security & Auth Service
    participant LED as Database & Ledger
    participant AUD as Audit Logger

    U->>GW: Submit Application / Request
    GW->>SVC: Forward Authenticated Payload
    SVC->>VER: Request Identity & Risk Verification
    VER-->>SVC: Verification Passed (Risk Score: 18 / Low)
    
    alt Amount Exceeds Threshold
        SVC-->>U: Trigger Step-Up MFA Challenge
        U->>SVC: Submit Biometric / Token Assertion
        SVC->>SEC: Validate Security Token
        SEC-->>SVC: Assertion Validated
    end

    SVC->>LED: Commit Transaction & Update Balances
    LED-->>SVC: Database Commit Confirmed

    SVC->>AUD: Record Write-Once Audit Event
    AUD-->>SVC: Cryptographic Hash Appended
    SVC-->>U: 200 Success (Reference Confirmed)
```

---

### 4. Activity Diagram (Workflow & Decision Logic)

```mermaid
flowchart TD
    Start([Start: User Submits Request]) --> Validate[Validate Input & Documents]
    Validate --> CheckValid{Valid Input?}
    
    CheckValid -->|No| FixInput[Prompt User for Corrections]
    FixInput --> Validate
    
    CheckValid -->|Yes| AutoCheck[Run Automated KYC & Screening]
    AutoCheck --> CheckSanction{Screening Passed?}
    
    CheckSanction -->|Flagged| ManualReview[Route to Compliance Officer]
    CheckSanction -->|Clear| ScoreRisk[Execute Algorithmic Risk Model]
    
    ScoreRisk --> DecisionThreshold{Risk Tier}
    DecisionThreshold -->|Low Risk| AutoApprove[System Auto-Approval]
    DecisionThreshold -->|Borderline| ManualReview
    DecisionThreshold -->|High Risk| RejectApp[Reject & Send Adverse Notice]
    
    ManualReview --> OfficerDecision{Officer Decision}
    OfficerDecision -->|Approved| AutoApprove
    OfficerDecision -->|Declined| RejectApp
    
    AutoApprove --> Disburse[Execute Settlement & Fund Transfer]
    Disburse --> AuditRecord[Log Immutable Audit Trail]
    AuditRecord --> Complete([End: Completed])
    RejectApp --> Complete
```

---

### 5. State Machine Diagram (Entity Lifecycle)

```mermaid
stateDiagram-v2
    [*] --> Draft : Application Created
    Draft --> Submitted : User Submits Form
    
    Submitted --> UnderVerification : Intake Pipeline Starts
    
    state UnderVerification {
        [*] --> DocumentCheck
        DocumentCheck --> WatchlistScreening : Documents OK
        WatchlistScreening --> VerificationPassed : No Red Flags
        WatchlistScreening --> Flagged : Anomaly Detected
    }
    
    Flagged --> ManualReview : Escalate to Specialist
    VerificationPassed --> Underwriting : Run Scoring Engine
    
    state Underwriting {
        [*] --> IngestData
        IngestData --> CalculateScore
        CalculateScore --> AutoApproved : Low Risk Score
        CalculateScore --> ManualReview : Borderline Score
        CalculateScore --> Rejected : High Risk Score
    }
    
    ManualReview --> AutoApproved : Specialist Overrides
    ManualReview --> Rejected : Specialist Rejects
    
    AutoApproved --> Disbursing : Trigger Payment Rails
    Disbursing --> Completed : Ledger Committed
    Completed --> [*]
    Rejected --> [*]
```
"""
