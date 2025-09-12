// Check if mobile
function isMobileDevice() {
    return window.innerWidth <= 450;
}

function initTableauViz(vizId) {
    // Show static images on mobile
    if (isMobileDevice()) {
        return;
    }
    
    const divElement = document.getElementById(vizId);
    if (divElement) {
        const vizElement = divElement.getElementsByTagName('object')[0];
        if (divElement.offsetWidth > 800) { 
            vizElement.style.width = '100%';
            vizElement.style.height = '627px';
        } else if (divElement.offsetWidth > 500) { 
            vizElement.style.width = '100%';
            vizElement.style.height = '627px';
        } else { 
            vizElement.style.width = '100%';
            vizElement.style.height = '727px';
        }
        
        const scriptElement = document.createElement('script');
        scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
        vizElement.parentNode.insertBefore(scriptElement, vizElement);
    }
}

const dashboardIds = [
    'viz1757276102353',  // Acceptance Rates
    'viz1757276138501',  // Retention Rates
    'viz1757276208403',  // Graduation Rates
    'viz1757276243041',  // Berklee 2022 Outcomes
    'viz1757276268581',  // MSM 2022 Outcomes
    'viz1757276304188',  // NEC 2022 Outcomes
    'viz1757276373111',  // Juilliard 2022 Outcomes
    'viz1757276395434',  // Curtis 2022 Outcomes
    'viz1757276451152',  // Tuition w/o Curtis
    'viz1757276474042',  // Tuition (All institutions)
    'viz1757276493141',  // Average Net Price
    'viz1757276515581',  // Berklee 2022 Cost Comparison
    'viz1757276551675',  // MSM 2022 Cost Comparison
    'viz1757276594331',  // NEC 2022 Cost Comparison
    'viz1757276608719',  // Juilliard 2022 Cost Comparison
    'viz1757276626375',  // Curtis 2022 Cost Comparison
    'viz1757276660099',  // Enrollment w/o Berklee
    'viz1757276680506',  // Enrollment (All institutions)
    'viz1757282252334'   // Total Enrollment 2022
];

function initAllTableauViz() {
    dashboardIds.forEach(function(id) {
        initTableauViz(id);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    initAllTableauViz();
});