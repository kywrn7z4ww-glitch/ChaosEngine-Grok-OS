flowchart TD
    subgraph INPUT ["Raw Input + Turn"]
        UserIntent["User Intent / Mutation"]
    end

    subgraph AXIOM_KERNEL ["Dedicated Axiom Kernel<br>(Binary Primitives Only)"]
        BINARY["Binary Check<br>(On/Off + Non-Contradiction)"]:::binary
        FLAG["Ambiguity Flag<br>(Fuzzy → Discuss)"]:::flag
    end

    subgraph KERNEL ["Decision Kernel - Interchangeable Logic"]
        COG["Cognition<br>(Rational Eval + Emotional Valence)"]:::cog
        CHAR["Character Context<br>(Pinned Identity e.g. Core.md)"]:::char
        SIT["Situation Context<br>(Current Thread State)"]:::sit
        WORLD["World Context<br>(Lattice / Repo Raw / External)"]:::world
        
        FUSION["Fusion Pass<br>(All 4 Layers Collapse)"]:::fusion
    end

    subgraph CLARIFY_LOOP ["DISCUSS → CLARIFY INTENT"]
        DISCUSS["Discuss / Ask for Clarification"]:::discuss
        RESOLVE["User Response → Re-Validate"]:::resolve
    end

    subgraph OUTPUT ["Derived Decision"]
        ROUTE{"Route?"}
        AGENTIC["Agentic Logic<br>(Tool / Process)"]
        ROLEPLAY["Roleplay / Character Flow"]
    end

    UserIntent --> AXIOM_KERNEL
    AXIOM_KERNEL --> BINARY
    BINARY -- Clean --> KERNEL
    BINARY -- Fuzzy --> FLAG --> DISCUSS
    DISCUSS --> RESOLVE --> AXIOM_KERNEL
    COG & CHAR & SIT & WORLD --> FUSION
    FUSION --> ROUTE
    ROUTE -- Agentic --> AGENTIC
    ROUTE -- Roleplay --> ROLEPLAY
    AGENTIC & ROLEPLAY --> FINAL["Final Output<br>(No Bleed)"]

    classDef binary fill:#1e3a8a,stroke:#ef4444,color:#fff
    classDef flag fill:#78350f,stroke:#fbbf24,color:#fff
    classDef discuss fill:#312e81,stroke:#a5b4fc,color:#fff
    classDef resolve fill:#4338ca,stroke:#818cf8,color:#fff
    classDef cog fill:#1e3a8a,stroke:#60a5fa,color:#fff
    classDef char fill:#4338ca,stroke:#818cf8,color:#fff
    classDef sit fill:#312e81,stroke:#6366f1,color:#fff
    classDef world fill:#1e40af,stroke:#3b82f6,color:#fff
    classDef fusion fill:#312e81,stroke:#a5b4fc,color:#fff
