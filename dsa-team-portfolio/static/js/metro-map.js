/**
 * METRO MANILA 2026 - LOGIC & COORDINATES
 * Fixes: Doroteo Jose/Recto & Cubao Alignment
 */

let startStation = null;
let endStation = null;

document.addEventListener('DOMContentLoaded', () => {
    distributeStations();
    hideInterchangeDuplicateLabels();
});

function distributeStations() {
    const paths = {
        'lrt1': document.getElementById('path-lrt1'),
        'lrt2': document.getElementById('path-lrt2'),
        'mrt3': document.getElementById('path-mrt3')
    };

    // VITAL INTERSECTIONS (Hub Pins) - Fixed to match actual line intersections
    // Doroteo Jose/Recto: LRT1 (x=250) meets LRT2 at start (250,210)
    const HUB_RECTO_DJOSE = { x: 250, y: 260 }; 
    // Cubao: Intersection of LRT2 and MRT3 at (750, 300)
    const HUB_CUBAO = { x: 630, y: 220 };       
    // EDSA/Taft Avenue: LRT1 (x=250) meets MRT3 at (250, 500)
    const HUB_TAFT_EDSA = { x: 250, y: 530 };    

    Object.keys(paths).forEach(line => {
        const path = paths[line];
        const nodes = document.querySelectorAll(`.station-node-group.${line}`);
        if (!path || !nodes.length) return;

        const totalLength = path.getTotalLength();

        nodes.forEach((node, index) => {
            const name = node.getAttribute('data-name');
            let pt;

            // 1. PIN THE HUBS
            if (name.includes("Recto") || name.includes("Doroteo Jose")) {
                pt = HUB_RECTO_DJOSE;
            } else if (name.includes("Cubao")) {
                pt = HUB_CUBAO;
            } else if (name.includes("Taft Avenue") || name === "EDSA") {
                pt = HUB_TAFT_EDSA;
            } else {
                // 2. SPACE REMAINING STATIONS
                const padding = 0.08;
                const distance = (index / (nodes.length - 1)) * (totalLength * (1 - 2*padding)) + (totalLength * padding);
                pt = path.getPointAtLength(distance);
            }

            node.setAttribute('transform', `translate(${pt.x}, ${pt.y})`);

            // 3. STAGGER LABELS
            const text = node.querySelector('.station-text');
            const isEven = index % 2 === 0;

            if (line === 'lrt1') {
                text.setAttribute('dx', '-15');
                text.style.textAnchor = 'end';
            } else if (line === 'mrt3') {
                // MRT3 is on the right, move labels to the right of the line
                text.setAttribute('dx', '15');
                text.style.textAnchor = 'start';
            } else {
                // LRT2: Stagger labels above/below the diagonal line
                text.setAttribute('dy', isEven ? '-15' : '-28');
                text.style.textAnchor = 'middle';
            }
        });
    });
}

function selectStation(name, element) {
    const startIn = document.getElementById('start_input');
    const endIn = document.getElementById('end_input');
    const startDisp = document.getElementById('start_display');
    const endDisp = document.getElementById('end_display');

    if (!startStation) {
        startStation = name;
        startIn.value = name; 
        startDisp.innerText = name.split(' (')[0];
        element.classList.add('active-start');
    } else if (!endStation && name !== startStation) {
        endStation = name;
        endIn.value = name; 
        endDisp.innerText = name.split(' (')[0];
        element.classList.add('active-end');
    } else {
        resetSelection();
        selectStation(name, element);
    }
}

function resetSelection() {
    startStation = null;
    endStation = null;
    document.getElementById('start_input').value = "";
    document.getElementById('end_input').value = "";
    document.getElementById('start_display').innerText = "--";
    document.getElementById('end_display').innerText = "--";
    document.querySelectorAll('.station-node-group').forEach(el => {
        el.classList.remove('active-start', 'active-end');
    });
}

function highlightRouteOnMap(routeNames) {
    const svg = document.getElementById('metro-svg');
    svg.classList.add('route-active');
    
    // Highlight each station on the route with animation
    routeNames.forEach((name, index) => {
        const node = document.querySelector(`[data-name="${name}"]`);
        if (node) {
            node.classList.add('on-route');
            // Add staggered animation timing for each station
            node.style.animationDelay = `${index * 0.1}s`;
        }
    });
    
    // Draw connecting lines between consecutive stations on route
    const baseGroup = svg.querySelector('g#base-tracks');
    const routeGroup = document.createElement('g');
    routeGroup.id = 'route-path';
    routeGroup.setAttribute('style', 'pointer-events: none;');
    
    for (let i = 0; i < routeNames.length - 1; i++) {
        const startNode = document.querySelector(`[data-name="${routeNames[i]}"]`);
        const endNode = document.querySelector(`[data-name="${routeNames[i + 1]}"]`);
        
        if (startNode && endNode) {
            const startTransform = startNode.getAttribute('transform');
            const endTransform = endNode.getAttribute('transform');
            
            // Parse coordinates from transform
            const startMatch = startTransform.match(/translate\(([\d.]+),\s*([\d.]+)\)/);
            const endMatch = endTransform.match(/translate\(([\d.]+),\s*([\d.]+)\)/);
            
            if (startMatch && endMatch) {
                const x1 = parseFloat(startMatch[1]);
                const y1 = parseFloat(startMatch[2]);
                const x2 = parseFloat(endMatch[1]);
                const y2 = parseFloat(endMatch[2]);
                
                // Create animated line segment
                const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                line.setAttribute('x1', x1);
                line.setAttribute('y1', y1);
                line.setAttribute('x2', x2);
                line.setAttribute('y2', y2);
                line.setAttribute('stroke', '#00ff00');
                line.setAttribute('stroke-width', '2.5');
                line.setAttribute('stroke-linecap', 'round');
                line.setAttribute('opacity', '0.8');
                line.setAttribute('class', 'route-segment');
                line.setAttribute('style', `filter: drop-shadow(0 0 8px #00ff00) drop-shadow(0 0 15px #00ff00); animation: routeFlow 1.5s ease-in-out ${i * 0.15}s infinite;`);
                
                routeGroup.appendChild(line);
            }
        }
    }
    
    baseGroup.parentNode.insertBefore(routeGroup, baseGroup.nextSibling);
}

// Hide duplicate interchange station labels - keep only one per interchange
function hideInterchangeDuplicateLabels() {
    const interchanges = {
        'Doroteo Jose-Recto': true,
        'Cubao': true,
        'EDSA-Taft Avenue': true
    };

    const seenInterchanges = {};
    
    document.querySelectorAll('.station-node-group').forEach(node => {
        const name = node.getAttribute('data-name');
        
        if (interchanges[name]) {
            if (seenInterchanges[name]) {
                // Hide duplicate interchange labels (keep text hidden but keep clickable)
                const text = node.querySelector('.station-text');
                if (text) {
                    text.style.display = 'none';
                }
            } else {
                seenInterchanges[name] = true;
            }
        }
    });
}