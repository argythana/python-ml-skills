---
name: lazy-imports
description: >
  Use this skill when the user wants to lazily import Python modules,
  defer module loading until first use, or reduce Python or CLI startup
  cost by changing import behavior. Trigger on requests like "import X
  lazily", "don't load pandas until it's used", "use PEP 810", "use
  `wrapt.lazy_import()`", or "make this CLI's imports lazy". If the
  target code or supported Python version is missing and cannot be
  inferred from the repo, ask for it after routing. Do NOT use it just
  because a Python file has heavy dependencies, or for general import
  cleanup, generic startup tuning that is not about imports, or
  dependency-management requests where the main task is adding or
  updating packages; use `uv-deps` for that work.
---

# Lazy imports

Generate Python code that defers module loading until first use. Pick the
right mechanism based on the target Python version:

- **Python >= 3.15**: use the native `lazy` soft keyword (PEP 810).
- **Python 3.9-3.14**: use `wrapt.lazy_import()` (requires `wrapt >= 2.1.0`).

Use this skill when the task is to change Python import behavior. Do not
use it for generic import cleanup, dependency-only work, or startup tuning
that does not hinge on import deferral.

## Step 1 — determine the Python version

Check the project for version clues in this order:

1. `python_requires` in `pyproject.toml` or `setup.cfg`
2. `.python-version` file
3. The user's explicit statement ("I'm on 3.13", etc.)
4. Runtime shebang or CI config

If the minimum supported version is **>= 3.15**, use the native syntax.
If it is **3.9-3.14**, use `wrapt`. If it is **< 3.9** or unknown,
**ask the user** before proceeding because this skill's guidance assumes
Python 3.9+.

## Step 2 — write the imports

### Python 3.15+ — native `lazy` keyword

```python
# Whole module
lazy import numpy as np

# From-import
lazy from pathlib import Path

# Mix with eager imports freely
import argparse            # eager — lightweight, needed immediately
lazy import torch          # deferred until first use
lazy import pandas as pd   # deferred until first use
```

Constraints enforced by the interpreter — produce a `SyntaxError` if
violated:

- `lazy` imports are only allowed at **module scope**. Not inside
  functions, class bodies, or `try`/`except`/`finally` blocks.
- Star imports cannot be lazy: `lazy from mod import *` is illegal.
- Future imports cannot be lazy: `lazy from __future__ import ...` is
  illegal.

Errors such as `ModuleNotFoundError` surface at **first use**, not at the
import statement. The traceback includes both the use site and the
original import line.

### Python 3.9-3.14 — `wrapt.lazy_import()`

Requires `wrapt >= 2.1.0`. Add it to the project's dependencies.

```python
import wrapt

# Whole module
np = wrapt.lazy_import("numpy")

# Submodule via dotted path
pd_core = wrapt.lazy_import("pandas.core")

# Specific attribute from a module
dumps = wrapt.lazy_import("json", "dumps")
```

Key behaviours:

- Returns a `LazyObjectProxy` — a transparent proxy that triggers the
  real import on first attribute access or call.
- Does **not** patch `sys.modules` until the module is actually loaded.
  No global side effects.
- For callable attributes, the proxy is automatically callable
  (`wrapt >= 2.1`). For non-callable objects with special dunder methods,
  pass `interface=` with the appropriate `collections.abc` type.
- Supports Python 3.9+.

### Type checking with `wrapt` (Python 3.9-3.14)

`wrapt.LazyObjectProxy` is opaque to static type checkers — they cannot
see the real type behind the proxy. To restore full IDE support
(autocompletion, type inference, go-to-definition), **always** pair every
`wrapt.lazy_import()` call with a `TYPE_CHECKING` guard that performs the
real import statically. The `TYPE_CHECKING` constant is `False` at
runtime, so the eager import never executes — it exists purely for type
checkers and IDEs.

```python
from __future__ import annotations   # makes all annotations strings, avoiding runtime evaluation
import typing as ty
import wrapt

numpy = wrapt.lazy_import("numpy")
pd = wrapt.lazy_import("pandas")
dumps = wrapt.lazy_import("json", "dumps")

if ty.TYPE_CHECKING:
    import numpy
    import pandas as pd
    from json import dumps
```

Rules:

- The names inside the `TYPE_CHECKING` block **must match** the variable
  names bound by `wrapt.lazy_import()` so that type checkers associate the
  correct type with the correct name.
- Use `from __future__ import annotations` at the top of the file. This
  ensures annotations are treated as strings and never trigger a runtime
  import of the type-checked module.
- Keep the `TYPE_CHECKING` block immediately after the `wrapt` lazy
  imports so the pairing is obvious.
- On Python 3.15+ this is unnecessary — the native `lazy` keyword is
  understood by type checkers natively.

## Step 3 — decide what should stay eager

Default to lazy. Only keep an import eager when one of these applies:

| Reason to stay eager | Example |
|---|---|
| Module has **import-time side effects** that must run immediately | `logging.config`, monkey-patching libs like `gevent.monkey` |
| Import is inside a `try/except ImportError` block for **optional dependency detection** — the point is to fail eagerly | `try: import ujson except ImportError: import json` |
| Module is **trivially cheap** and used on every code path | `os`, `sys`, `typing`, `collections` |
| The module is a **`__future__`** import | `from __future__ import annotations` |

When generating code, add a short comment next to any eager import
explaining why it is not lazy, so the intent is clear:

```python
import sys                  # eager — trivial, always needed
lazy import numpy as np     # deferred
```

## Example transformations

### "Lazily import numpy, pandas, and torch"

Python >= 3.15:
```python
lazy import numpy as np
lazy import pandas as pd
lazy import torch
```

Python < 3.15:
```python
from __future__ import annotations
import typing as ty
import wrapt

np = wrapt.lazy_import("numpy")
pd = wrapt.lazy_import("pandas")
torch = wrapt.lazy_import("torch")

if ty.TYPE_CHECKING:
    import numpy as np
    import pandas as pd
    import torch
```

### "Lazily import just the dumps function from json"

Python >= 3.15:
```python
lazy from json import dumps
```

Python < 3.15:
```python
from __future__ import annotations
import typing as ty
import wrapt

dumps = wrapt.lazy_import("json", "dumps")

if ty.TYPE_CHECKING:
    from json import dumps
```

### "Make this CLI's imports lazy"

Given existing code:
```python
import argparse
import numpy as np
import torch
from rich.console import Console
```

Python >= 3.15 output:
```python
import argparse             # eager — trivial, always needed
lazy import numpy as np
lazy import torch
lazy from rich.console import Console
```

Python < 3.15 output:
```python
from __future__ import annotations
import argparse             # eager — trivial, always needed
import typing as ty
import wrapt

np = wrapt.lazy_import("numpy")
torch = wrapt.lazy_import("torch")
Console = wrapt.lazy_import("rich.console", "Console")

if ty.TYPE_CHECKING:
    import numpy as np
    import torch
    from rich.console import Console
```
