"""
ExcalidrawAgent - A comprehensive agent for generating Excalidraw diagrams from text descriptions.

This module provides a complete implementation for creating Excalidraw JSON diagrams
with support for common patterns like flowcharts, agent frameworks, and system architectures.

Features:
- Generate proper Excalidraw JSON structure
- Support for text, rectangle, ellipse, and arrow elements
- Automatic positioning and layout management
- Consistent styling and color schemes
- Arrow binding and connection system
- Multiple layout patterns (sequential, routing, parallel)
"""

import json
import uuid
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import math


class ElementType(Enum):
    """Supported Excalidraw element types."""
    TEXT = "text"
    RECTANGLE = "rectangle"
    ELLIPSE = "ellipse"
    ARROW = "arrow"


class ColorScheme(Enum):
    """Predefined color schemes for different element types."""
    LLM = "#ffec99"           # Yellow for LLMs
    CODE = "#a5d8ff"          # Blue for code/coordinators
    PROCESS = "#c2f0c2"       # Green for processes
    TRANSPARENT = "transparent"
    DEFAULT_STROKE = "#1e1e1e"


class LayoutType(Enum):
    """Supported layout patterns."""
    SEQUENTIAL = "sequential"    # Linear chain of elements
    ROUTING = "routing"         # Hub-and-spoke pattern
    PARALLEL = "parallel"       # Multiple parallel paths
    GRID = "grid"              # Grid layout


@dataclass
class Position:
    """Represents a 2D position."""
    x: float
    y: float


@dataclass
class Size:
    """Represents element dimensions."""
    width: float
    height: float


@dataclass
class ExcalidrawElement:
    """Base structure for an Excalidraw element."""
    id: str
    type: str
    x: float
    y: float
    width: float
    height: float
    angle: float = 0
    strokeColor: str = "#1e1e1e"
    backgroundColor: str = "transparent"
    fillStyle: str = "solid"
    strokeWidth: int = 2
    strokeStyle: str = "solid"
    roughness: int = 1
    opacity: int = 100
    groupIds: List[str] = None
    frameId: Optional[str] = None
    index: str = "a0"
    roundness: Optional[Dict] = None
    seed: int = 1
    version: int = 1
    versionNonce: int = 1
    isDeleted: bool = False
    boundElements: List[Dict] = None
    updated: int = 1757460000000
    link: Optional[str] = None
    locked: bool = False

    def __post_init__(self):
        if self.groupIds is None:
            self.groupIds = []
        if self.boundElements is None:
            self.boundElements = []


class ExcalidrawAgent:
    """
    Main agent class for generating Excalidraw diagrams.
    
    This class provides methods to create various types of diagrams from text descriptions,
    handle element positioning, styling, and arrow connections.
    """

    def __init__(self):
        """Initialize the ExcalidrawAgent."""
        self.elements: List[Dict] = []
        self.element_counter = 0
        self.group_counter = 0
        self.current_group_id = None
        
        # Default spacing and sizing
        self.default_spacing_x = 150
        self.default_spacing_y = 100
        self.default_text_size = 16
        self.default_element_width = 120
        self.default_element_height = 60

    def _generate_id(self, prefix: str = "element") -> str:
        """Generate a unique ID for an element."""
        self.element_counter += 1
        return f"{prefix}-{self.element_counter}"

    def _generate_group_id(self) -> str:
        """Generate a unique group ID."""
        self.group_counter += 1
        return f"group-{self.group_counter}"

    def _create_base_element(self, element_type: ElementType, x: float, y: float, 
                           width: float, height: float, element_id: str = None) -> Dict:
        """Create a base element with common properties."""
        if element_id is None:
            element_id = self._generate_id()
        
        return {
            "id": element_id,
            "type": element_type.value,
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "angle": 0,
            "strokeColor": ColorScheme.DEFAULT_STROKE.value,
            "backgroundColor": ColorScheme.TRANSPARENT.value,
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": 100,
            "groupIds": [self.current_group_id] if self.current_group_id else [],
            "frameId": None,
            "index": f"a{self.element_counter}",
            "roundness": None,
            "seed": self.element_counter,
            "version": 1,
            "versionNonce": self.element_counter * 1000,
            "isDeleted": False,
            "boundElements": [],
            "updated": 1757460000000 + self.element_counter,
            "link": None,
            "locked": False
        }

    def create_text_element(self, text: str, x: float, y: float, 
                          container_id: str = None, font_size: int = None) -> Dict:
        """
        Create a text element.
        
        Args:
            text: The text content
            x, y: Position coordinates
            container_id: ID of container element if text is inside a shape
            font_size: Font size (defaults to self.default_text_size)
        
        Returns:
            Dict representing the text element
        """
        if font_size is None:
            font_size = self.default_text_size

        # Calculate text dimensions (approximate)
        char_width = font_size * 0.6  # Approximate character width
        text_width = len(text) * char_width
        text_height = font_size * 1.2

        element = self._create_base_element(ElementType.TEXT, x, y, text_width, text_height)
        element.update({
            "text": text,
            "fontSize": font_size,
            "fontFamily": 5,  # Excalidraw default font
            "textAlign": "center" if container_id else "left",
            "verticalAlign": "middle" if container_id else "top",
            "containerId": container_id,
            "originalText": text,
            "autoResize": True,
            "lineHeight": 1.25
        })

        return element

    def create_rectangle(self, x: float, y: float, width: float = None, 
                        height: float = None, text: str = None, 
                        background_color: str = None) -> Tuple[Dict, Optional[Dict]]:
        """
        Create a rectangle element, optionally with contained text.
        
        Args:
            x, y: Position coordinates
            width, height: Dimensions (use defaults if None)
            text: Optional text to place inside the rectangle
            background_color: Background color (defaults to transparent)
        
        Returns:
            Tuple of (rectangle_element, text_element) where text_element is None if no text
        """
        if width is None:
            width = self.default_element_width
        if height is None:
            height = self.default_element_height
        if background_color is None:
            background_color = ColorScheme.TRANSPARENT.value

        rect_id = self._generate_id("rect")
        rect_element = self._create_base_element(ElementType.RECTANGLE, x, y, width, height, rect_id)
        rect_element.update({
            "backgroundColor": background_color,
            "roundness": {"type": 3}  # Rounded corners
        })

        text_element = None
        if text:
            # Center the text in the rectangle
            text_x = x + width / 2 - len(text) * self.default_text_size * 0.3
            text_y = y + height / 2 - self.default_text_size / 2
            
            text_element = self.create_text_element(text, text_x, text_y, rect_id)
            
            # Add text binding to rectangle
            rect_element["boundElements"].append({
                "type": "text",
                "id": text_element["id"]
            })

        return rect_element, text_element

    def create_ellipse(self, x: float, y: float, width: float = None, 
                      height: float = None, text: str = None, 
                      background_color: str = None) -> Tuple[Dict, Optional[Dict]]:
        """
        Create an ellipse element, optionally with contained text.
        
        Args:
            x, y: Position coordinates
            width, height: Dimensions (use defaults if None)
            text: Optional text to place inside the ellipse
            background_color: Background color (defaults to transparent)
        
        Returns:
            Tuple of (ellipse_element, text_element) where text_element is None if no text
        """
        if width is None:
            width = self.default_element_width
        if height is None:
            height = self.default_element_height
        if background_color is None:
            background_color = ColorScheme.TRANSPARENT.value

        ellipse_id = self._generate_id("ellipse")
        ellipse_element = self._create_base_element(ElementType.ELLIPSE, x, y, width, height, ellipse_id)
        ellipse_element.update({
            "backgroundColor": background_color,
            "roundness": {"type": 2}  # Ellipse roundness
        })

        text_element = None
        if text:
            # Center the text in the ellipse
            text_x = x + width / 2 - len(text) * self.default_text_size * 0.3
            text_y = y + height / 2 - self.default_text_size / 2
            
            text_element = self.create_text_element(text, text_x, text_y, ellipse_id)
            
            # Add text binding to ellipse
            ellipse_element["boundElements"].append({
                "type": "text",
                "id": text_element["id"]
            })

        return ellipse_element, text_element

    def create_arrow(self, start_element_id: str, end_element_id: str, 
                    start_pos: Position = None, end_pos: Position = None,
                    style: str = "solid", width: int = 2) -> Dict:
        """
        Create an arrow connecting two elements.
        
        Args:
            start_element_id: ID of the starting element
            end_element_id: ID of the ending element
            start_pos: Starting position (calculated if None)
            end_pos: Ending position (calculated if None)
            style: Arrow style ("solid" or "dashed")
            width: Arrow line width
        
        Returns:
            Dict representing the arrow element
        """
        # Find the start and end elements to calculate positions
        start_element = None
        end_element = None
        
        for element in self.elements:
            if element["id"] == start_element_id:
                start_element = element
            elif element["id"] == end_element_id:
                end_element = element

        if not start_element or not end_element:
            raise ValueError("Start or end element not found")

        # Calculate connection points if not provided
        if start_pos is None:
            start_pos = Position(
                start_element["x"] + start_element["width"],
                start_element["y"] + start_element["height"] / 2
            )
        
        if end_pos is None:
            end_pos = Position(
                end_element["x"],
                end_element["y"] + end_element["height"] / 2
            )

        # Calculate arrow dimensions
        arrow_width = end_pos.x - start_pos.x
        arrow_height = end_pos.y - start_pos.y

        arrow_id = self._generate_id("arrow")
        arrow_element = self._create_base_element(
            ElementType.ARROW, start_pos.x, start_pos.y, 
            abs(arrow_width), abs(arrow_height), arrow_id
        )

        arrow_element.update({
            "strokeStyle": style,
            "strokeWidth": width,
            "roundness": {"type": 2},
            "startBinding": {
                "elementId": start_element_id,
                "focus": 0,
                "gap": 1
            },
            "endBinding": {
                "elementId": end_element_id,
                "focus": 0,
                "gap": 1
            },
            "lastCommittedPoint": None,
            "startArrowhead": None,
            "endArrowhead": "arrow",
            "points": [
                [0, 0],
                [arrow_width, arrow_height]
            ]
        })

        # Add arrow bindings to connected elements
        start_element["boundElements"].append({
            "id": arrow_id,
            "type": "arrow"
        })
        end_element["boundElements"].append({
            "id": arrow_id,
            "type": "arrow"
        })

        return arrow_element

    def start_group(self, group_name: str = None) -> str:
        """
        Start a new group for organizing related elements.
        
        Args:
            group_name: Optional name for the group
        
        Returns:
            The group ID
        """
        group_id = self._generate_group_id()
        if group_name:
            group_id = f"{group_name}-{group_id}"
        
        self.current_group_id = group_id
        return group_id

    def end_group(self):
        """End the current group."""
        self.current_group_id = None

    def add_element(self, element: Dict):
        """Add an element to the diagram."""
        self.elements.append(element)

    def create_sequential_layout(self, items: List[str], start_x: float = 50, 
                                start_y: float = 50, item_type: str = "rectangle",
                                colors: List[str] = None) -> List[Dict]:
        """
        Create a sequential (chain) layout of elements.
        
        Args:
            items: List of text labels for elements
            start_x, start_y: Starting position
            item_type: Type of elements ("rectangle" or "ellipse")
            colors: List of background colors (cycles if shorter than items)
        
        Returns:
            List of created elements
        """
        if colors is None:
            colors = [ColorScheme.LLM.value]

        elements = []
        shapes = []  # Store shapes for arrow creation
        current_x = start_x
        current_y = start_y

        # First pass: create all shapes
        for i, item in enumerate(items):
            color = colors[i % len(colors)]
            
            if item_type == "rectangle":
                shape, text = self.create_rectangle(
                    current_x, current_y, text=item, background_color=color
                )
            else:
                shape, text = self.create_ellipse(
                    current_x, current_y, text=item, background_color=color
                )

            elements.append(shape)
            if text:
                elements.append(text)
            
            shapes.append(shape)
            current_x += self.default_element_width + self.default_spacing_x

        # Second pass: create arrows between consecutive shapes
        for i in range(len(shapes) - 1):
            # Temporarily add shapes to internal list for arrow creation
            if shapes[i] not in self.elements:
                self.add_element(shapes[i])
            if shapes[i + 1] not in self.elements:
                self.add_element(shapes[i + 1])
                
            arrow = self.create_arrow(shapes[i]["id"], shapes[i + 1]["id"])
            elements.append(arrow)
            
            # Remove temporarily added elements to avoid duplicates
            if shapes[i] in self.elements:
                self.elements.remove(shapes[i])
            if shapes[i + 1] in self.elements:
                self.elements.remove(shapes[i + 1])

        return elements

    def create_routing_layout(self, router_name: str, destinations: List[str],
                            start_x: float = 50, start_y: float = 150,
                            router_color: str = None, dest_colors: List[str] = None) -> List[Dict]:
        """
        Create a routing (hub-and-spoke) layout.
        
        Args:
            router_name: Name of the central router element
            destinations: List of destination names
            start_x, start_y: Starting position for router
            router_color: Color for router element
            dest_colors: Colors for destination elements
        
        Returns:
            List of created elements
        """
        if router_color is None:
            router_color = ColorScheme.CODE.value
        if dest_colors is None:
            dest_colors = [ColorScheme.LLM.value]

        elements = []
        
        # Create router (central element)
        router, router_text = self.create_rectangle(
            start_x, start_y, text=router_name, background_color=router_color
        )
        elements.extend([router, router_text])
        self.add_element(router)
        self.add_element(router_text)

        # Create destinations around the router
        angle_step = 2 * math.pi / len(destinations)
        radius = self.default_spacing_x * 1.5

        for i, dest_name in enumerate(destinations):
            angle = i * angle_step
            dest_x = start_x + radius * math.cos(angle)
            dest_y = start_y + radius * math.sin(angle)
            
            color = dest_colors[i % len(dest_colors)]
            dest, dest_text = self.create_rectangle(
                dest_x, dest_y, text=dest_name, background_color=color
            )
            elements.extend([dest, dest_text])
            self.add_element(dest)
            self.add_element(dest_text)

            # Create arrow from router to destination
            arrow = self.create_arrow(router["id"], dest["id"])
            elements.append(arrow)

        return elements

    def create_parallel_layout(self, input_name: str, parallel_items: List[str],
                             output_name: str, start_x: float = 50, start_y: float = 300,
                             colors: List[str] = None) -> List[Dict]:
        """
        Create a parallel processing layout.
        
        Args:
            input_name: Name of input element
            parallel_items: List of parallel processing elements
            output_name: Name of output element
            start_x, start_y: Starting position
            colors: Colors for parallel elements
        
        Returns:
            List of created elements
        """
        if colors is None:
            colors = [ColorScheme.LLM.value, ColorScheme.CODE.value]

        elements = []
        
        # Create input element
        input_elem, input_text = self.create_ellipse(
            start_x, start_y, text=input_name, background_color=ColorScheme.TRANSPARENT.value
        )
        elements.extend([input_elem, input_text])
        self.add_element(input_elem)
        self.add_element(input_text)

        # Create parallel elements
        parallel_x = start_x + self.default_spacing_x * 2
        parallel_elements = []
        
        for i, item_name in enumerate(parallel_items):
            item_y = start_y + (i - len(parallel_items) / 2) * self.default_spacing_y
            color = colors[i % len(colors)]
            
            item, item_text = self.create_rectangle(
                parallel_x, item_y, text=item_name, background_color=color
            )
            elements.extend([item, item_text])
            self.add_element(item)
            self.add_element(item_text)
            parallel_elements.append(item)

            # Create arrow from input to this parallel element
            arrow = self.create_arrow(input_elem["id"], item["id"])
            elements.append(arrow)

        # Create output element
        output_x = parallel_x + self.default_spacing_x * 2
        output_elem, output_text = self.create_ellipse(
            output_x, start_y, text=output_name, background_color=ColorScheme.TRANSPARENT.value
        )
        elements.extend([output_elem, output_text])
        self.add_element(output_elem)
        self.add_element(output_text)

        # Create arrows from parallel elements to output
        for parallel_elem in parallel_elements:
            arrow = self.create_arrow(parallel_elem["id"], output_elem["id"])
            elements.append(arrow)

        return elements

    def generate_excalidraw_json(self, diagram_title: str = "Generated Diagram") -> Dict:
        """
        Generate the complete Excalidraw JSON structure.
        
        Args:
            diagram_title: Title for the diagram
        
        Returns:
            Complete Excalidraw JSON structure
        """
        return {
            "type": "excalidraw",
            "version": 2,
            "source": "https://github.com/your-username/excalidraw-agent",
            "elements": self.elements,
            "appState": {
                "gridSize": 20,
                "viewBackgroundColor": "#ffffff",
                "currentItemFontFamily": 5,
                "currentItemFontSize": 16,
                "currentItemStrokeColor": "#1e1e1e",
                "currentItemBackgroundColor": "transparent",
                "currentItemFillStyle": "solid",
                "currentItemStrokeWidth": 2,
                "currentItemStrokeStyle": "solid",
                "currentItemRoughness": 1,
                "currentItemOpacity": 100,
                "currentItemTextAlign": "left",
                "currentItemStartArrowhead": None,
                "currentItemEndArrowhead": "arrow"
            },
            "files": {}
        }

    def save_diagram(self, filename: str, diagram_title: str = "Generated Diagram"):
        """
        Save the diagram to a file.
        
        Args:
            filename: Output filename (should end with .excalidraw)
            diagram_title: Title for the diagram
        """
        excalidraw_json = self.generate_excalidraw_json(diagram_title)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(excalidraw_json, f, indent=2, ensure_ascii=False)

    def clear(self):
        """Clear all elements and reset counters."""
        self.elements.clear()
        self.element_counter = 0
        self.group_counter = 0
        self.current_group_id = None

    def create_flowchart_from_description(self, description: str) -> List[Dict]:
        """
        Create a flowchart from a text description.
        
        This is a simple example that parses basic descriptions.
        In practice, you might want to use NLP or more sophisticated parsing.
        
        Args:
            description: Text description of the flowchart
        
        Returns:
            List of created elements
        """
        # Simple parser - look for keywords and create appropriate layouts
        description = description.lower()
        
        if "sequential" in description or "chain" in description:
            # Extract items (this is a simplified example)
            items = ["Step 1", "Step 2", "Step 3", "Step 4"]
            return self.create_sequential_layout(items)
        
        elif "routing" in description or "router" in description:
            router = "Router"
            destinations = ["LLM1", "LLM2", "LLM3"]
            return self.create_routing_layout(router, destinations)
        
        elif "parallel" in description:
            input_name = "Input"
            parallel_items = ["Process A", "Process B", "Process C"]
            output_name = "Output"
            return self.create_parallel_layout(input_name, parallel_items, output_name)
        
        else:
            # Default to sequential
            items = ["Input", "Process", "Output"]
            return self.create_sequential_layout(items)


# Example usage and convenience functions
def create_agent_framework_diagram() -> ExcalidrawAgent:
    """
    Create an example agent framework diagram showing different patterns.
    
    Returns:
        ExcalidrawAgent instance with the generated diagram
    """
    agent = ExcalidrawAgent()
    
    # Create title
    title_element = agent.create_text_element("Agent Framework Patterns", 50, 20, font_size=24)
    agent.add_element(title_element)
    
    # Create sequential pattern
    agent.start_group("sequential")
    sequential_title = agent.create_text_element("1. Sequential", 50, 60, font_size=18)
    agent.add_element(sequential_title)
    
    sequential_elements = agent.create_sequential_layout(
        ["Input", "LLM1", "LLM2", "LLM3", "Output"],
        start_y=80,
        colors=[ColorScheme.TRANSPARENT.value, ColorScheme.LLM.value, 
               ColorScheme.LLM.value, ColorScheme.LLM.value, ColorScheme.TRANSPARENT.value]
    )
    for elem in sequential_elements:
        agent.add_element(elem)
    agent.end_group()
    
    # Create routing pattern
    agent.start_group("routing")
    routing_title = agent.create_text_element("2. Routing", 50, 180, font_size=18)
    agent.add_element(routing_title)
    
    routing_elements = agent.create_routing_layout(
        "Router", ["LLM1", "LLM2", "LLM3"],
        start_x=150, start_y=220
    )
    for elem in routing_elements:
        agent.add_element(elem)
    agent.end_group()
    
    # Create parallel pattern
    agent.start_group("parallel")
    parallel_title = agent.create_text_element("3. Parallel", 50, 400, font_size=18)
    agent.add_element(parallel_title)
    
    parallel_elements = agent.create_parallel_layout(
        "Input", ["LLM1", "LLM2", "LLM3"], "Output",
        start_y=440
    )
    for elem in parallel_elements:
        agent.add_element(elem)
    agent.end_group()
    
    return agent


if __name__ == "__main__":
    # Example usage
    agent = create_agent_framework_diagram()
    agent.save_diagram("agent_framework_example.excalidraw")
    print("Agent framework diagram saved to 'agent_framework_example.excalidraw'")