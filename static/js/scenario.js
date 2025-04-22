$(document).ready(function() {
    let bubbleText = $('.speech-bubble').find('.speech-bubble-text');
    let clickZones = $('.click-zone');
    let totalParts = clickZones.length;
    let nextButton = $('.kawaii-button.next-button');
    let exploredParts = new Set();
    
    console.log(nextButton.text);
    nextButton.prop('disabled', true).addClass('disabled');

    clickZones.on('click', function() {
        let part = $(this).data('part');
        let bodyLanguage = $(this).data('response').toLowerCase();
        let response =  `You found the <span class="speech-bubble-text kawaii-behavior-highlight">${part}</span>
         <ul class="kawaii-behavior-list">
            ${bodyLanguage.split(',')
            .map(item => {
                let trimmed = item.trim();
                let capitalized = trimmed.charAt(0).toUpperCase() + trimmed.slice(1);
                return `<li>${capitalized}</li>`;
            })
            .join('')}
        </ul>`;

        exploredParts.add(part);

        if (exploredParts.size === totalParts) {
            response += `<div class="progress-message">Progress: ${exploredParts.size}/${totalParts} Great job!</div>`;
            nextButton.prop('disabled', false).removeClass('disabled').addClass('scale');
        }
        else {
            response += `<div class="progress-message">Progress: ${exploredParts.size}/${totalParts}</div>`;
        }
        bubbleText.html(response);
    });
});