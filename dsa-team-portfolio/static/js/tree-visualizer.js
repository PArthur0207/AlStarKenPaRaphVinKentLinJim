/**
 * Tree Visualizer - Binary Tree & BST Visual Representation
 * Converts Python Node objects to animated interactive visual display
 * Usage: initTreeVisualizer('container-id', treeObject, animatePath)
 */

(function() {
  'use strict';

  window.initTreeVisualizer = function(containerId, treeRoot, animatePath) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // If there's no tree data, show an empty placeholder so the preview column remains visible
    if (!treeRoot) {
      container.innerHTML = '';
      const empty = document.createElement('div');
      empty.className = 'tree-empty';
      empty.textContent = 'No nodes yet — add a root to visualize the tree.';
      container.appendChild(empty);
      return;
    }

    // Clear previous content
    container.innerHTML = '';

    // Configuration
    const config = {
      nodeRadius: 25,
      nodeWidth: 50,
      nodeHeight: 50,
      hGap: 120,        // base horizontal spacing (pixels)
      vGap: 100,        // vertical spacing
      animationDelay: 600, // ms between highlights
      highlightDuration: 700 // ms node stays highlighted
    };

    // Step 1: Compute a non-overlapping layout using inorder positions
    const nodes = new Map(); // value -> {x, y, depth, parentValue, element}
    let maxDepth = 0;

    // Convert the provided plain object tree into a lightweight node wrapper we can augment
    function cloneNode(obj, parentValue = null) {
      if (!obj) return null;
      const n = { value: obj.value, left: cloneNode(obj.left, obj.value), right: cloneNode(obj.right, obj.value), parentValue };
      return n;
    }

    const root = cloneNode(treeRoot, null);

    // Assign inorder indices so nodes are spaced without overlapping
    let xIndex = 0;
    function assignPositions(n, depth) {
      if (!n) return;
      maxDepth = Math.max(maxDepth, depth);

      // traverse left
      if (n.left) assignPositions(n.left, depth + 1);

      // this node: assign inorder x index
      n._ix = xIndex++;
      n._depth = depth;

      // traverse right
      if (n.right) assignPositions(n.right, depth + 1);
    }

    assignPositions(root, 0);

    // Determine effective spacing based on node size and minimum gap
    const minGap = 12; // minimal gap between node boxes
    const spacing = Math.max(config.hGap, config.nodeWidth + minGap);

    // Populate nodes Map with pixel positions
    function populateNodes(n) {
      if (!n) return;
      const x = n._ix * spacing;
      const y = n._depth * config.vGap;

      nodes.set(String(n.value), {
        value: n.value,
        x: x,
        y: y,
        depth: n._depth,
        parentValue: n.parentValue === undefined ? null : n.parentValue,
        element: null
      });

      if (n.left) populateNodes(n.left);
      if (n.right) populateNodes(n.right);
    }

    populateNodes(root);

    // Calculate container dimensions
    const treeWidth = Math.pow(2, maxDepth + 1) * config.hGap;
    const treeHeight = (maxDepth + 1) * config.vGap + config.nodeHeight;

    // Set container size
    container.style.position = 'relative';
    container.style.width = '100%';
    container.style.height = Math.max(400, treeHeight + 60) + 'px';
    container.style.overflow = 'auto';

    // Create a stage to hold svg and nodes; this allows centering and scaling
    const stage = document.createElement('div');
    stage.className = 'vt-stage';
    stage.style.position = 'relative';
    stage.style.transformOrigin = 'top center';
    stage.style.zIndex = '1';
    container.appendChild(stage);

    // Create SVG for connection lines inside the stage
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', 'vt-svg');
    svg.style.position = 'absolute';
    svg.style.top = '0';
    svg.style.left = '0';
    svg.style.pointerEvents = 'none';
    svg.style.zIndex = '1';
    stage.appendChild(svg);

    // (Positions already assigned via inorder assignPositions & populateNodes)

    // Step 2: Draw connection lines using DOM element positions (works after nodes appended to stage)
    function drawConnections() {
      // Remove existing lines if any
      while (svg.firstChild) svg.removeChild(svg.firstChild);

      nodes.forEach((nodeData, value) => {
        if (nodeData.parentValue !== null) {
          const parentObj = nodes.get(String(nodeData.parentValue));
          if (!parentObj || !parentObj.element || !nodeData.element) return;

          const pEl = parentObj.element;
          const cEl = nodeData.element;

          // Coordinates relative to stage
          const px = pEl.offsetLeft + pEl.offsetWidth / 2;
          const py = pEl.offsetTop + pEl.offsetHeight / 2;
          const cx = cEl.offsetLeft + cEl.offsetWidth / 2;
          const cy = cEl.offsetTop + cEl.offsetHeight / 2;

          const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
          line.setAttribute('x1', px);
          line.setAttribute('y1', py);
          line.setAttribute('x2', cx);
          line.setAttribute('y2', cy);
          line.setAttribute('class', 'vt-line');
          svg.appendChild(line);
        }
      });
    }

    // Step 3: Create node elements inside the stage
    nodes.forEach((nodeData, value) => {
      const nodeEl = document.createElement('div');
      nodeEl.className = 'vt-node-container';
      nodeEl.id = 'node-' + value;
      nodeEl.style.position = 'absolute';
      nodeEl.style.left = nodeData.x + 'px';
      nodeEl.style.top = nodeData.y + 'px';
      nodeEl.style.minWidth = config.nodeWidth + 'px';
      nodeEl.style.height = config.nodeHeight + 'px';
      nodeEl.style.zIndex = '2';

      // Inner div for styling (reuse existing tree-node class)
      const innerDiv = document.createElement('div');
      innerDiv.className = 'tree-node';
      innerDiv.textContent = value;
      innerDiv.style.width = '100%';
      innerDiv.style.height = '100%';
      innerDiv.style.display = 'flex';
      innerDiv.style.alignItems = 'center';
      innerDiv.style.justifyContent = 'center';

      nodeEl.appendChild(innerDiv);
      stage.appendChild(nodeEl);
      nodeData.element = nodeEl;
    });

    // Compute bounding box from actual element sizes, reposition nodes relative to leftmost, size stage and svg, then draw connections
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    nodes.forEach((d) => {
      const el = d.element;
      const left = el.offsetLeft;
      const right = left + el.offsetWidth;
      const top = el.offsetTop;
      const bottom = top + el.offsetHeight;

      minX = Math.min(minX, left);
      maxX = Math.max(maxX, right);
      minY = Math.min(minY, top);
      maxY = Math.max(maxY, bottom);
    });
    if (minX === Infinity) { minX = 0; maxX = config.nodeWidth; }

    const contentWidth = maxX - minX;
    const contentHeight = maxY - minY;

    // Position nodes relative to minX (so leftmost is at 0 in stage)
    nodes.forEach((d) => {
      d.element.style.left = (d.x - minX) + 'px';
      d.element.style.top = (d.y - minY) + 'px';
    });

    // Size the stage and svg: stage width equals content width (+ padding)
    const stageWidth = contentWidth + 40;
    const stageHeight = contentHeight + 40;
    stage.style.width = stageWidth + 'px';
    stage.style.height = stageHeight + 'px';
    svg.setAttribute('width', stageWidth);
    svg.setAttribute('height', stageHeight);
    svg.style.width = stageWidth + 'px';
    svg.style.height = stageHeight + 'px';

    // Draw lines now that nodes are positioned inside stage
    drawConnections();

    // Centering and scaling behavior
    const containerW = container.clientWidth || container.offsetWidth || 800;
    let scale = 1;
    if (stageWidth > containerW) {
      scale = Math.max(0.35, (containerW - 40) / stageWidth);
    }
    // Center stage using container's flexbox centering; apply scaling transform only
    stage.style.position = 'relative';
    stage.style.margin = '0 auto';
    stage.style.transformOrigin = 'top center';
    stage.style.transform = `scale(${scale})`;
    // If scaled to 1 but content overflows, center scroll
    if (scale === 1 && stageWidth > containerW) {
      container.scrollLeft = Math.floor((stageWidth - containerW) / 2);
    }

    // Step 4: Animation - highlight search path
    function animateSearchPath(path) {
      if (!path || !Array.isArray(path) || path.length === 0) return;

      path.forEach((nodeValue, index) => {
        setTimeout(() => {
          const nodeData = nodes.get(String(nodeValue));
          if (nodeData && nodeData.element) {
            // Add highlight effect
            nodeData.element.classList.add('vt-highlight');
            nodeData.element.style.zIndex = '10';

            // Remove highlight after duration
            setTimeout(() => {
              nodeData.element.classList.remove('vt-highlight');
              nodeData.element.style.zIndex = '2';
            }, config.highlightDuration);
          }
        }, index * config.animationDelay);
      });
    }

    if (animatePath && animatePath.length > 0) {
      animateSearchPath(animatePath);
    }
  };
})();
