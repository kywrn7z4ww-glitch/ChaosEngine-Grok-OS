# Suno Workflow

## Overview

This folder contains three specialized tools for creating high-quality Suno prompts:

| File                              | Purpose                              | Best Used For                     |
|-----------------------------------|--------------------------------------|-----------------------------------|
| `suno-musical-theory-engines.md`  | Advanced refiner with 18 engines     | Complex ideas, theory integration, refinement |
| `suno_instumental_template.md`    | Instrumental-only master template    | Purely instrumental tracks        |
| `suno_prompt.md`                  | Structured song creation template    | Full songs with lyrics & sections |

## Recommended Workflow

1. **Describe your idea**
   - Tell me what kind of track you want to make (genre, mood, instruments, vibe, etc.)

2. **Run the Engines** (`suno-musical-theory-engines.md`)
   - This is your main starting point.
   - It will refine your idea, suggest relevant music theory, and help clarify direction.

3. **Make a Decision**
   - **Purely Instrumental?** → Use `suno_instumental_template.md`
   - **Full song with lyrics/structure?** → Use `suno_prompt.md`

4. **Generate Final Prompt**
   - The chosen template will produce a clean, optimized prompt ready for Suno.

5. **Iterate**
   - You can always go back to the engines for further refinement.

```mermaid
flowchart TD
    A[User describes what they want to create] --> B[Run suno-musical-theory-engines.md]
    B --> C{Refine Style + Gather Theories}
    C --> D{Instrumental or Full Song?}
    
    D -->|Instrumental| E[Use suno_instumental_template.md]
    D -->|Full Song with Lyrics| F[Use suno_prompt.md]
    
    E --> G[Generate Final Suno Prompt]
    F --> G
    
    G --> H[Copy into Suno]
    
    style B fill:#e3f2fd
    style C fill:#fff3e0
    style D fill:#e8f5e9```

## Quick Start

Just say something like:
> "I want a dark Japanese cyberpunk track with heavy synths and industrial drums"

Then I’ll guide you through the workflow using the right tools.
