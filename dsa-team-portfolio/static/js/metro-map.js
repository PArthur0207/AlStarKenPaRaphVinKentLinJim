/**
 * METRO MANILA 2026 - LOGIC & COORDINATES
 * Fixes: Doroteo Jose / Recto Alignment
 */

let startStation = null;
let endStation = null;

document.addEventListener('DOMContentLoaded', () => {
    distributeStations();
});

function distributeStations() {
    const paths = {
        'lrt1': document.getElementById('path-lrt1'),
        'lrt2': document.getElementById('path-lrt2'),
        'mrt3': document.getElementById('path-mrt3')
    };

    // VITAL INTERSECTIONS (Hub Pins) - Fixed to match actual line intersections
    // Doroteo Jose/Recto: LRT1 (x=250) meets LRT2 at start (250,210)
    const HUB_RECTO_DJOSE = { x: 250, y: 210 }; 
    // Araneta Center-Cubao: LRT2 and MRT3 both reach (750, 300)
    const HUB_CUBAO = { x: 750, y: 300 };       
    // EDSA/Taft Avenue: LRT1 (x=250) meets MRT3 at (250, 500)
    const HUB_TAFT_EDSA = { x: 250, y: 500 };    

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
            } else if (name.includes("Araneta Center-Cubao")) {
                pt = HUB_CUBAO;
            } else if (name.includes("Taft Avenue") || name === "EDSA") {
                pt = HUB_TAFT_EDSA;
            } else {
                // 2. SPACE REMAINING STATIONS
                // We use a specific distribution to ensure they follow the SVG track path
                const padding = 0.08;
                const distance = (index / (nodes.length - 1)) * (totalLength * (1 - 2*padding)) + (totalLength * padding);
                pt = path.getPointAtLength(distance);
            }

            node.setAttribute('transform', `translate(${pt.x}, ${pt.y})`);

            // 3. STAGGER LABELS
            const text = node.querySelector('.station-text');
            const isEven = index % 2 === 0;

            if (line === 'lrt1') {
                text.setAttribute('dx', '-12');
                text.style.textAnchor = 'end';
            } else if (line === 'mrt3') {
                text.setAttribute('dx', '12');
                text.style.textAnchor = 'start';
            } else {
                // Stagger LRT2 labels so they don't overlap the angled path
                text.setAttribute('dy', isEven ? '-12' : '-25');
                text.style.textAnchor = 'middle';
            }
        });
    });
}

// Selection logic remains the same
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
    routeNames.forEach(name => {
        const node = document.querySelector(`[data-name="${name}"]`);
        if (node) node.classList.add('on-route');
    });
}