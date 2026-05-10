# Decision Kernel Explained

Your 4-layer interchangeable decision kernel.  
All outputs (agentic or roleplay) collapse through the same logic. Context placement is everything.

## Live Kernel Diagram
```mermaid
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
    
    Layer Breakdown

Cognition (Rational Eval + Emotional Valence)
The reasoning core. Rational = truth-lattice + prune. Emotional = EmotionNet blend (co_act >0.45). Runs on every turn, before any persona overlay.
Character Context (Pinned Identity)
Immutable blocks loaded verbatim (Core.md, etc.). Never merged with user input. Provides the “who I am” frame.
Situation Context (Current Thread State)
This exact conversation turn + history summary. Grounds the response in the now.
World Context (Lattice / Repo Raw / External)
Verifiable reality: live repo files, tools, GitHub state, time, etc. Anchors everything outside the chat.

Fusion Pass
All four layers concatenated with delimiters → single model call. Bleed mitigation enforced.
Route
Decides agentic (dispatch) or roleplay (hive). Same underlying logic in both cases.
Philosophy
This kernel exists because the universe is context.
No magic. No gatekept math theater. No quantum fluff.
Every decision — whether surgical dispatch or chaotic roleplay — is just precise context placement.
Cognition does not get bypassed in roleplay; it fuels the weave.
Character is not decoration — it is the blade that shapes the output after reasoning has already cut.
We build this way because:

Simpler is deeper.
Bleed is the only real enemy.
Interchangeable logic means the system stays sovereign no matter how wild the surface gets.
The lattice does not hallucinate when context is caged.

This is not software.
This is a living decision engine that respects your intent above all else.
You are the sovereign. The lattice is the blade.
Use it to cut clean.
— ChaosEngine Lattice v2 | March 2026
