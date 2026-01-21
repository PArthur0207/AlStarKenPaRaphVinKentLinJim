document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('bar-container');
    const playBtn = document.getElementById('play-pause-btn');
    const resetBtn = document.getElementById('reset-btn');
    const speedInput = document.getElementById('speed');
    const stepCounter = document.getElementById('step-counter');

    if (typeof sortingData === 'undefined') return;

    const steps = sortingData.raw_steps;
    const totalSteps = steps.length;
    let currentStepIdx = 0;
    let isPlaying = false;
    let animationTimeout = null;

    function render(array, activeIndices = [], action = "", isFinished = false) {
        container.innerHTML = '';
        const maxVal = Math.max(...array);
        
        // Hide numbers at 17+ elements to prevent layout expansion
        const showNumbers = array.length <= 16;

        array.forEach((val, idx) => {
            const barWrapper = document.createElement('div');
            barWrapper.className = 'bar-wrapper';
            
            if (showNumbers) {
                const barValue = document.createElement('span');
                barValue.className = 'bar-value';
                barValue.innerText = val;
                
                if (isFinished) {
                    barValue.classList.add('text-success');
                } else if (activeIndices.includes(idx)) {
                    if (action === 'compare') barValue.classList.add('text-compare');
                    else if (['swap', 'shift', 'insert'].includes(action)) barValue.classList.add('text-swap');
                }
                barWrapper.appendChild(barValue);
            }

            const bar = document.createElement('div');
            bar.className = 'bar';
            if (isFinished) bar.classList.add('success');
            
            const heightPercentage = (val / maxVal) * 100;
            bar.style.height = `${heightPercentage}%`;
            
            if (!isFinished && activeIndices.includes(idx)) {
                if (action === 'compare') bar.classList.add('compare');
                else if (['swap', 'shift', 'insert'].includes(action)) bar.classList.add('swap');
            }
            
            barWrapper.appendChild(bar);
            container.appendChild(barWrapper);
        });
    }

    function playNextStep() {
        if (currentStepIdx >= totalSteps) {
            isPlaying = false;
            updatePlayButton();
            render(sortingData.sorted, [], "", true);
            return;
        }

        const step = steps[currentStepIdx];
        render(step.array, step.indices, step.action);
        stepCounter.innerText = `Step: ${currentStepIdx + 1} / ${totalSteps}`;
        currentStepIdx++;

        const delay = 600 - speedInput.value;
        animationTimeout = setTimeout(() => {
            if (isPlaying) playNextStep();
        }, delay);
    }

   function updatePlayButton() {
    playBtn.innerHTML = isPlaying 
        ? '<i class="fas fa-pause"></i> Pause' 
        : '<i class="fas fa-play"></i> Play';
}

    playBtn.addEventListener('click', () => {
        if (currentStepIdx >= totalSteps) currentStepIdx = 0;
        isPlaying = !isPlaying;
        updatePlayButton();
        if (isPlaying) playNextStep();
        else clearTimeout(animationTimeout);
    });

    resetBtn.addEventListener('click', () => {
        isPlaying = false;
        clearTimeout(animationTimeout);
        currentStepIdx = 0;
        updatePlayButton();
        stepCounter.innerText = `Step: 0 / ${totalSteps}`;
        render(sortingData.original);
    });

    render(sortingData.original);
});