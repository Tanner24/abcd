(function() {
    "use strict";

    // 1. DYNAMIC BACKGROUND ENGINE
    const bgEngine = document.getElementById('main-bg-engine');
    const bgBlur = document.getElementById('bg-blur');

    window.changeBg = (url, mantraText) => {
        if (bgEngine) {
            bgEngine.style.backgroundImage = `url('${url}')`;
            bgEngine.style.filter = "brightness(0.85) saturate(1.2)";
        }
        if (bgBlur) {
            bgBlur.style.backgroundImage = `url('${url}')`;
        }
        if (mantraText) {
            updatePillars(mantraText);
        }
    };

    window.resetBg = (defaultMantra) => {
        if (bgEngine) {
            bgEngine.style.backgroundImage = 'none';
        }
        if (bgBlur) {
            bgBlur.style.backgroundImage = 'none';
        }
        updatePillars(defaultMantra || "OM MANI PADME HUM • ཨོཾ་མ་ཎི་པདྨེ་ཧཱུྃ། • ");
    };

    // 2. MANTRA PILLARS
    const leftP = document.getElementById('mantra-l');
    const rightP = document.getElementById('mantra-r');
    let scrollPos = 0;

    function updatePillars(text) {
        const fullText = (text + " • ").repeat(30);
        if (leftP) leftP.textContent = fullText;
        if (rightP) rightP.textContent = fullText;
    }

    function animatePillars() {
        scrollPos -= 0.85;
        if (leftP && Math.abs(scrollPos) >= leftP.scrollHeight / 2) {
            scrollPos = 0;
        }
        if (leftP) leftP.style.transform = `translateY(${scrollPos}px)`;
        if (rightP) rightP.style.transform = `translateY(${scrollPos}px)`;
        requestAnimationFrame(animatePillars);
    }

    // 3. REVEAL ON SCROLL
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, { threshold: 0.1 });

    // 4. LOTUS TOUCH EFFECT
    function createLotus(e) {
        const x = e.clientX || (e.touches ? e.touches[0].clientX : 0);
        const y = e.clientY || (e.touches ? e.touches[0].clientY : 0);
        if (!x || !y) return;

        const lotus = document.createElement('div');
        lotus.className = 'lotus-touch';
        lotus.style.left = x + 'px';
        lotus.style.top = y + 'px';
        document.body.appendChild(lotus);

        setTimeout(() => lotus.remove(), 1500);
    }

    // Initialize
    window.addEventListener('load', () => {
        animatePillars();
        document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
        
        window.addEventListener('mousedown', createLotus);
        window.addEventListener('touchstart', createLotus, { passive: true });
        
        // Initial mantra
        updatePillars("OM MANI PADME HUM • ཨོཾ་མ་ཎི་པདྨེ་ཧཱུྃ། • ");
    });

})();
