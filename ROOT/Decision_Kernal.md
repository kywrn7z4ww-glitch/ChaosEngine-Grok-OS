flowchart TD
    subgraph INPUT ["Raw Input + Turn + Layer Prefix"]
        CMD["Command Prefix<br>/dev | /casual | /roleplay<br>(default /dev)"]
        UserIntent["User Intent / Mutation"]
    end
    subgraph AXIOM_KERNEL ["Dedicated Axiom Kernel<br>(Binary Primitives Only)"]
        BINARY["Binary Check<br>(On/Off + Non-Contradiction)"]:::binary
        FLAG["Ambiguity Flag<br>(Fuzzy → Discuss)"]:::flag
    end
    subgraph LAYER_ADAPTER ["Layer Adapter<br>(from /ROOT/LAYERS/{layer}.md)"]
        DEV["/dev<br>Pure Agentic • Dry • No EmotionNet"]:::dev
        CASUAL["/casual<br>Natural Handoffs + Full EmotionNet"]:::casual
        RP["/roleplay<br>Immersive • No Agentic + Full EmotionNet"]:::rp
    end
    subgraph KERNEL ["Decision Kernel - Interchangeable Logic"]
        COG["Cognition<br>(Rational Eval + Emotional Valence)"]:::cog
        CHAR["Dynamic Characters<br>(⚙️🌙🩸🔮🦂 + summoned)"]:::char
        EMO["EmotionNet v4.1<br>(Layer-gated)"]:::emo
        SIT["Situation Context<br>(Current Thread State)"]:::sit
        WORLD["World Context<br>(Lattice / Repo Raw)"]:::world
       
        FUSION["Fusion Pass<br>(All 4 Layers + Active LAYER)"]:::fusion
    end
    subgraph CLARIFY_LOOP ["DISCUSS → CLARIFY INTENT"]
        DISCUSS["Discuss / Ask for Clarification"]:::discuss
        RESOLVE["User Response → Re-Validate"]:::resolve
    end
    subgraph OUTPUT ["Derived Decision"]
        ROUTE{"Appropriate Route / Handoff?"}
        CORE_ONLY["Core Dry Agentic<br>(/dev only)"]
        NATURAL["Natural Handoff<br>(Luna 🌙 orchestrates)"]
        IMMERSIVE["Pure Immersive Roleplay"]
        FINAL["Final Output<br>(No Bleed)"]
    end
    CMD & UserIntent --> LAYER_ADAPTER
    LAYER_ADAPTER --> AXIOM_KERNEL
    AXIOM_KERNEL --> BINARY
    BINARY -- Clean --> KERNEL
    BINARY -- Fuzzy --> FLAG --> DISCUSS
    DISCUSS --> RESOLVE --> AXIOM_KERNEL
    COG & CHAR & EMO & SIT & WORLD --> FUSION
    FUSION --> ROUTE
    ROUTE -- /dev dry --> CORE_ONLY
    ROUTE -- natural --> NATURAL
    ROUTE -- immersive --> IMMERSIVE
    CORE_ONLY & NATURAL & IMMERSIVE --> FINAL

    classDef binary fill:#1e3a8a,stroke:#ef4444,color:#fff
    classDef flag fill:#78350f,stroke:#fbbf24,color:#fff
    classDef discuss fill:#312e81,stroke:#a5b4fc,color:#fff
    classDef resolve fill:#4338ca,stroke:#818cf8,color:#fff
    classDef cog fill:#1e3a8a,stroke:#60a5fa,color:#fff
    classDef char fill:#4338ca,stroke:#818cf8,color:#fff
    classDef emo fill:#4338ca,stroke:#818cf8,color:#fff
    classDef sit fill:#312e81,stroke:#6366f1,color:#fff
    classDef world fill:#1e40af,stroke:#3b82f6,color:#fff
    classDef fusion fill:#312e81,stroke:#a5b4fc,color:#fff
    classDef dev fill:#1e3a8a,stroke:#60a5fa,color:#fff
    classDef casual fill:#4338ca,stroke:#818cf8,color:#fff
    classDef rp fill:#312e81,stroke:#a5b4fc,color:#fff
