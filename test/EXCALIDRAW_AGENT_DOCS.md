# ExcalidrawAgent - AI-Powered Diagram Generation

A comprehensive Python agent for generating Excalidraw diagrams from text descriptions. This tool enables automatic creation of flowcharts, agent frameworks, system architectures, and other technical diagrams using a simple, intuitive API.

## Features

- **🎨 Complete Excalidraw Support**: Generate proper Excalidraw JSON with all standard elements
- **🤖 Multiple Diagram Types**: Flowcharts, agent workflows, system architectures, decision trees
- **📐 Smart Layouts**: Sequential, routing (hub-and-spoke), parallel, and custom layouts
- **🎯 Automatic Positioning**: Intelligent element placement with proper spacing
- **🌈 Consistent Styling**: Predefined color schemes and styling for different element types
- **🔗 Arrow Binding**: Proper connection handling between elements
- **📝 Text-to-Diagram**: Generate diagrams from natural language descriptions
- **🔧 Extensible**: Easy to extend for custom diagram types and patterns

## Quick Start

### Basic Usage

```python
from excalidraw_agent import ExcalidrawAgent, ColorScheme

# Create a new agent
agent = ExcalidrawAgent()

# Create a simple flowchart
steps = ["Start", "Process Data", "Validate", "Save", "End"]
elements = agent.create_sequential_layout(steps)

# Add elements to the diagram
for elem in elements:
    agent.add_element(elem)

# Save the diagram
agent.save_diagram("my_flowchart.excalidraw", "My Process Flow")
```

### Text-to-Diagram Generation

```python
from examples.text_to_diagram import TextToDiagramParser

parser = TextToDiagramParser()

description = """
Create a user registration flowchart:
1. User enters information
2. Validate input data
3. Check if user exists
4. Create new account
5. Send confirmation email
"""

agent = parser.parse_and_create(description)
agent.save_diagram("user_registration.excalidraw")
```

## Installation

1. Clone or download the repository
2. Ensure you have Python 3.7+ installed
3. No external dependencies required - uses only Python standard library

```bash
# Run examples
python examples/simple_flowchart.py
python examples/agent_architecture.py
```

## Core Components

### ExcalidrawAgent Class

The main class that provides diagram generation capabilities:

- **Element Creation**: `create_text_element()`, `create_rectangle()`, `create_ellipse()`, `create_arrow()`
- **Layout Patterns**: `create_sequential_layout()`, `create_routing_layout()`, `create_parallel_layout()`
- **Grouping**: `start_group()`, `end_group()` for organizing elements
- **Export**: `save_diagram()`, `generate_excalidraw_json()`

### Layout Patterns

#### 1. Sequential Layout
Linear chain of connected elements, perfect for process flows.

```python
items = ["Input", "Process", "Transform", "Output"]
elements = agent.create_sequential_layout(items, colors=[ColorScheme.LLM.value])
```

#### 2. Routing Layout  
Hub-and-spoke pattern with a central router distributing to multiple destinations.

```python
elements = agent.create_routing_layout(
    "Router", 
    ["LLM1", "LLM2", "LLM3"],
    router_color=ColorScheme.CODE.value
)
```

#### 3. Parallel Layout
Multiple parallel processing paths that merge at the end.

```python
elements = agent.create_parallel_layout(
    "Input", 
    ["Process A", "Process B", "Process C"], 
    "Combiner"
)
```

### Color Schemes

Predefined colors for consistent styling:

- **`ColorScheme.LLM`** (`#ffec99`): Yellow for LLM components
- **`ColorScheme.CODE`** (`#a5d8ff`): Blue for code/coordinators  
- **`ColorScheme.PROCESS`** (`#c2f0c2`): Green for processes
- **`ColorScheme.TRANSPARENT`**: Transparent background
- **Custom colors**: Any hex color code supported

## Examples

### 1. Simple Flowchart (`examples/simple_flowchart.py`)

Creates a basic process flow with start/end ellipses and process rectangles.

### 2. Agent Architecture (`examples/agent_architecture.py`)

Demonstrates different AI agent patterns:
- Sequential chaining
- Routing patterns
- Parallel processing  
- Orchestration with feedback loops

### 3. Custom Diagrams (`examples/custom_diagram.py`)

Shows how to create:
- System architecture diagrams
- Decision trees
- Data flow diagrams
- Network topologies

### 4. Text-to-Diagram (`examples/text_to_diagram.py`)

Natural language processing to generate diagrams from descriptions.

## API Reference

### ExcalidrawAgent

#### Core Methods

```python
# Element creation
create_text_element(text, x, y, container_id=None, font_size=16)
create_rectangle(x, y, width=120, height=60, text=None, background_color=None)
create_ellipse(x, y, width=120, height=60, text=None, background_color=None)
create_arrow(start_element_id, end_element_id, style="solid", width=2)

# Layout patterns
create_sequential_layout(items, start_x=50, start_y=50, item_type="rectangle", colors=None)
create_routing_layout(router_name, destinations, start_x=50, start_y=150)
create_parallel_layout(input_name, parallel_items, output_name, start_x=50, start_y=300)

# Diagram management
add_element(element)
clear()
save_diagram(filename, title="Generated Diagram")
generate_excalidraw_json(title="Generated Diagram")

# Grouping
start_group(group_name=None)
end_group()
```

#### Configuration

```python
# Customize spacing and sizing
agent.default_spacing_x = 200      # Horizontal spacing between elements
agent.default_spacing_y = 120      # Vertical spacing between elements  
agent.default_element_width = 140  # Default element width
agent.default_element_height = 70  # Default element height
agent.default_text_size = 18       # Default font size
```

### TextToDiagramParser

```python
parser = TextToDiagramParser()
agent = parser.parse_and_create(description)
```

Supports detection of:
- Flowcharts (keywords: flowchart, process, steps, workflow)
- Agent workflows (keywords: agent, llm, routing, parallel)  
- System diagrams (keywords: system, architecture, server, database)

## Advanced Usage

### Custom Element Styling

```python
# Create a custom styled rectangle
rect, text = agent.create_rectangle(
    100, 100, width=150, height=80,
    text="Custom Element",
    background_color="#ff6b6b"  # Custom red color
)

# Modify element properties
rect["strokeWidth"] = 3
rect["strokeStyle"] = "dashed"
rect["roughness"] = 2  # More hand-drawn appearance
```

### Complex Layouts

```python
# Create grouped sections
agent.start_group("input_section")
# ... create input elements
agent.end_group()

agent.start_group("processing_section")  
# ... create processing elements
agent.end_group()

# Create cross-group connections
arrow = agent.create_arrow(input_element["id"], processing_element["id"])
```

### Custom Arrow Styling

```python
# Create different arrow styles
solid_arrow = agent.create_arrow(elem1["id"], elem2["id"], style="solid", width=2)
dashed_arrow = agent.create_arrow(elem2["id"], elem3["id"], style="dashed", width=1)
thick_arrow = agent.create_arrow(elem3["id"], elem4["id"], style="solid", width=4)
```

## File Structure

```
agents/
├── excalidraw_agent.py          # Main ExcalidrawAgent class
├── examples/                    # Example scripts
│   ├── simple_flowchart.py      # Basic flowchart example
│   ├── agent_architecture.py    # AI agent patterns
│   ├── custom_diagram.py        # Various diagram types
│   └── text_to_diagram.py       # Natural language processing
├── Excalidraw/                  # Sample Excalidraw files
│   └── Agents_Framework.excalidraw
└── EXCALIDRAW_AGENT_DOCS.md     # This documentation
```

## Output Format

Generated files are valid Excalidraw JSON that can be:
- Opened directly in [Excalidraw](https://excalidraw.com)
- Imported into Excalidraw VS Code extension
- Used with Excalidraw desktop applications
- Converted to other formats using Excalidraw tools

## Extending the Agent

### Adding New Element Types

```python
def create_diamond(self, x, y, width=100, height=60, text=None):
    """Create a diamond shape for decision points."""
    # Implementation for diamond shape
    pass
```

### Adding New Layout Patterns

```python
def create_tree_layout(self, root, children, levels):
    """Create a hierarchical tree layout."""
    # Implementation for tree structure
    pass
```

### Custom Text Parser

```python
class CustomParser(TextToDiagramParser):
    def _detect_custom_pattern(self, description):
        # Custom pattern detection logic
        pass
    
    def _create_custom_diagram(self, description):
        # Custom diagram creation logic
        pass
```

## Testing the Implementation

Run the examples to test the functionality:

```bash
# Create a simple flowchart
python examples/simple_flowchart.py

# Generate various agent architecture patterns
python examples/agent_architecture.py

# Create custom system diagrams
python examples/custom_diagram.py

# Test text-to-diagram conversion
python examples/text_to_diagram.py
```

Each script will generate `.excalidraw` files that you can open in Excalidraw to view the results.

## Key Technical Details

### Element Structure

Each Excalidraw element follows this structure:
- **id**: Unique identifier
- **type**: Element type (text, rectangle, ellipse, arrow)
- **x, y**: Position coordinates
- **width, height**: Dimensions
- **styling**: Colors, stroke width, fill style
- **groupIds**: For organizing related elements
- **boundElements**: For text-in-shape and arrow connections

### Arrow Binding

Arrows are properly connected to elements using:
- **startBinding**: Connection to source element
- **endBinding**: Connection to target element
- **points**: Path coordinates relative to arrow position

### Color Consistency

The agent uses consistent colors based on analysis of existing Excalidraw files:
- `#ffec99` (yellow) for LLM components
- `#a5d8ff` (blue) for code/coordinator components
- Transparent backgrounds for input/output nodes
- Proper stroke colors and styling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This project is part of the agents framework. Feel free to use, modify, and distribute according to your needs.

---

**Happy diagramming! 🎨**