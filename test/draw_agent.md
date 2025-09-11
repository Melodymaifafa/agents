 Excalidraw JSON Generation Instructions

  Basic Structure

  {
    "type": "excalidraw",
    "version": 2,
    "source": "https://marketplace.visualstudio.com/ite
  ms?itemName=pomdtr.excalidraw-editor",
    "elements": [/* array of elements */],
    "appState": {/* optional app state */},
    "files": {/* optional files */}
  }

  Element Types and Properties

  1. Text Elements

  {
    "id": "unique-id",
    "type": "text",
    "x": 100, "y": 100,
    "width": 200, "height": 35,
    "angle": 0,
    "strokeColor": "#1971c2",
    "backgroundColor": "transparent",
    "fillStyle": "solid",
    "strokeWidth": 2,
    "strokeStyle": "solid",
    "roughness": 1,
    "opacity": 100,
    "text": "Your text here",
    "fontSize": 28,
    "fontFamily": 5,
    "textAlign": "left",
    "verticalAlign": "top",
    "autoResize": true,
    "lineHeight": 1.25
  }

  2. Rectangle Elements

  {
    "id": "unique-id",
    "type": "rectangle",
    "x": 100, "y": 100,
    "width": 80, "height": 30,
    "strokeColor": "#1e1e1e",
    "backgroundColor": "#ffec99",
    "roundness": {"type": 3},
    "boundElements": [
      {"type": "text", "id": "text-element-id"},
      {"id": "arrow-id", "type": "arrow"}
    ]
  }

  3. Ellipse Elements

  {
    "id": "unique-id",
    "type": "ellipse",
    "x": 100, "y": 100,
    "width": 60, "height": 50,
    "roundness": {"type": 2},
    "boundElements": [
      {"type": "text", "id": "text-element-id"}
    ]
  }

  4. Arrow Elements

  {
    "id": "unique-id",
    "type": "arrow",
    "x": 100, "y": 100,
    "width": 50, "height": 10,
    "strokeStyle": "solid", // or "dashed"
    "strokeWidth": 2, // or 1 for dashed
    "points": [[0, 0], [50, 10]],
    "startBinding": {
      "elementId": "source-element-id",
      "focus": 0.1,
      "gap": 5
    },
    "endBinding": {
      "elementId": "target-element-id",
      "focus": -0.1,
      "gap": 5
    },
    "startArrowhead": null,
    "endArrowhead": "arrow"
  }

⏺ Color Schemes and Styles

  Common Colors:

  - Text/Stroke: #1e1e1e (dark), #1971c2 (blue for titles)
  - Backgrounds: #ffec99 (yellow for LLM boxes), #a5d8ff
  (light blue for code/coordinator)
  - Transparent: "transparent"

  Element Styling:

  - LLM Components: Yellow background (#ffec99)
  - Code/Coordinator: Light blue background (#a5d8ff)
  - Input/Output: Transparent ellipses
  - Arrows: Solid lines (width 2) or dashed lines (width 1)

  Arrow Connection System

  Binding Rules:

  1. startBinding: Connects arrow start to source element
  2. endBinding: Connects arrow end to target element
  3. focus: Controls connection point (-1 to 1, where 0 is
  center)
  4. gap: Distance from element edge (typically 5-10)

  Arrow Types:

  - Solid arrows: strokeStyle: "solid", strokeWidth: 2
  - Dashed arrows: strokeStyle: "dashed", strokeWidth: 1

  Layout Patterns

  1. Prompt Chaining (Sequential):

  [In] → [LLM1] → [Code] → [LLM2] → [LLM3] → [Out]

  2. Routing (Conditional):

  [In] → [Router] → [LLM1] → [Out]
                  → [LLM2] → [Out]
                  → [LLM3] → [Out]

  3. Parallelization:

  [In] → [Coordinator] → [LLM1] → [Aggregator] → [Out]
                       → [LLM2] →
                       → [LLM3] →

  Required Properties for All Elements:

  {
    "id": "unique-string",
    "type": "text|rectangle|ellipse|arrow",
    "x": number, "y": number,
    "width": number, "height": number,
    "angle": 0,
    "strokeColor": "#color",
    "backgroundColor": "#color|transparent",
    "fillStyle": "solid",
    "strokeWidth": 1|2,
    "strokeStyle": "solid|dashed",
    "roughness": 1,
    "opacity": 100,
    "groupIds": [],
    "frameId": null,
    "index": "string",
    "roundness": null|{"type": 2|3},
    "seed": number,
    "version": number,
    "versionNonce": number,
    "isDeleted": false,
    "boundElements": [],
    "updated": timestamp,
    "link": null,
    "locked": false
  }

  Text-in-Shape Pattern:

  When adding text to shapes, create two elements:
  1. Shape element with boundElements: [{"type": "text", 
  "id": "text-id"}]
  2. Text element with containerId: "shape-id"

⏺ Generation Tips for LLMs:

  1. IDs: Use descriptive IDs like "title1", "chain-llm1",
  "router", "arrow-connection"
  2. Positioning:
    - Start layouts from x=50, y=50
    - Space elements ~100-150px apart horizontally
    - Space elements ~50-80px apart vertically
  3. Grouping: Use groupIds to logically group related
  elements (e.g., all elements in "Routing" section)
  4. Arrows: Always include both startBinding and
  endBinding for proper connections
  5. Text Sizing:
    - Titles: fontSize 28-30
    - Element labels: fontSize 10-12
    - Body text: fontSize 16

  This structure enables LLMs to generate consistent,
  well-formatted Excalidraw diagrams that follow the
  established patterns for agent frameworks and workflow
  visualizations.