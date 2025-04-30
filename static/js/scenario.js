$(document).ready(function() {
    let bubbleText     = $('.speech-bubble').find('.speech-bubble-text');
    let clickZones     = $('.click-zone');
    let totalParts     = clickZones.length;
    let nextButton     = $('.kawaii-button.next-button');
    let exploredParts  = new Set();
    let currentAudio   = null;
    let currentIcon    = null;
  
    // disable next button initially
    nextButton.prop('disabled', true).addClass('disabled');
  
    clickZones.on('click', function() {
        let part        = $(this).data('part');
        let bodyLanguage= $(this).data('response').toLowerCase();
        let response    = `You found the <span class="kawaii-behavior-highlight">${part}</span><ul class="kawaii-behavior-list">`;
    
        if (part === 'sound' && $(this).data('sound-files')) {
            let descriptions = bodyLanguage.split(',');
            let soundFiles   = $(this).data('sound-files').split(',');
    
            descriptions.forEach((desc, i) => {
            let cap = desc.trim().replace(/^./, c => c.toUpperCase());
            response += `
                <li>
                ${cap}
                <span class="sound-icon" data-sound="/static/sounds/${soundFiles[i].trim()}">🎵</span>
                </li>`;
            });
        } else {
            response += bodyLanguage
            .split(',')
            .map(item => `<li>${item.trim().replace(/^./, c => c.toUpperCase())}</li>`)
            .join('');
        }
        response += '</ul>';

        exploredParts.add(part);
        $(this).addClass('explored');
    
        // update progress + enable Next if done
        let prog = `Progress: ${exploredParts.size}/${totalParts}`;
        if (exploredParts.size === totalParts) {
            response += `<div class="progress-message">${prog} Great job!</div>`;
            nextButton.prop('disabled', false).removeClass('disabled').addClass('scale');
        } else {
            response += `<div class="progress-message">${prog}</div>`;
        }
    
        bubbleText.html(response);
    });
  
    // sound icon click event
    $(document).on('click', '.sound-icon', function(e) {
        e.stopPropagation();
        let icon      = $(this);
        let soundFile = icon.data('sound');
    
        // If same icon clicked again, stop playback
        if (currentAudio && icon.is(currentIcon)) {
            currentAudio.pause();
            currentAudio.currentTime = 0;
            icon.css('transform', 'scale(1)').text('🎵');
            currentAudio = currentIcon = null;
            return;
        }
    
        // Otherwise, stop any existing audio & reset all icons
        if (currentAudio) {
            currentAudio.pause();
            currentAudio.currentTime = 0;
            currentIcon.css('transform', 'scale(1)').text('🎵');
        }
    
        // Start new audio
        currentAudio = new Audio(soundFile);
        currentIcon  = icon;
        icon.css('transform', 'scale(1.2)').text('🎶');
    
        currentAudio.play()
            .then(() => {
            currentAudio.onended = () => {
                icon.css('transform', 'scale(1)').text('🎵');
                currentAudio = currentIcon = null;
            };
            })
            .catch(err => {
                console.error('Audio playback failed:', err);
                icon.css('transform', 'scale(1)').text('🎵');
                currentAudio = currentIcon = null;
            });
    });
  });
  