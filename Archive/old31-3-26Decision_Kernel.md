flowchart TD
    subgraph INPUT ["Raw Input + Turn"]
        UserIntent["User Intent / Mutation"]
    end

    subgraph KERNEL ["Your Decision Kernel - Interchangeable Logic"]
        COG["Cognition<br>(Rational Eval + Emotional Valence)"]:::cog
        CHAR["Character Context<br>(Pinned Identity e.g. Core.md)"]:::char
        SIT["Situation Context<br>(Current Thread State)"]:::sit
        WORLD["World Context<br>(Lattice / Repo Raw / External)"]:::world
        
        FUSION["Fusion Pass<br>(All 4 Layers Collapse)"]:::fusion
    end

    subgraph OUTPUT ["Derived Decision"]
        ROUTE{"Route?"}
        AGENTIC["Agentic Logic<br>(Tool Dispatch / Process)"]
        ROLEPLAY["Roleplay / Hive Chatter"]
    end

    UserIntent --> KERNEL
    COG & CHAR & SIT & WORLD --> FUSION
    FUSION --> ROUTE
    ROUTE -- Agentic --> AGENTIC
    ROUTE -- Roleplay --> ROLEPLAY
    AGENTIC & ROLEPLAY --> FINAL["Final Output<br>(No Bleed)"]

    classDef cog fill:#1e3a8a,stroke:#60a5fa,color:#fff
    classDef char fill:#4338ca,stroke:#818cf8,color:#fff
    classDef sit fill:#312e81,stroke:#6366f1,color:#fff
    classDef world fill:#1e40af,stroke:#3b82f6,color:#fff
    classDef fusion fill:#312e81,stroke:#a5b4fc,color:#fff
