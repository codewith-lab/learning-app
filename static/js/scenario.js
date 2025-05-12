// Global state variables
let category, bubbleText, warning, clickZones, nextButton;
let totalParts, exploredParts, exploredSounds;
let soundFiles = [], currentSound = null, currentIcon = null, prevPart = null;

let soundWarning = '<span class="speech-bubble-text-highlight">❗</span> Please listen to ALL <span class="speech-bubble-text-highlight">audio clips 🎵</span> before continuing<br>';
let bodyWarning = '<span class="speech-bubble-text-highlight">❗</span> Please explore ALL <span class="speech-bubble-text-highlight">body parts</span> before continuing<br>';

// Function to prepopulate progress
function prepProgress() {
    exploredParts = new Set(explored_parts || []);
    exploredSounds = new Set(explored_sounds || []);
    finishedSet = new Set(finished_sessions || []);
    
    // Update UI for already explored parts
    clickZones.each(function() {
        let part = $(this).data('part');
        if (exploredParts.has(part)) {
            $(this).addClass('explored');
        }
    });

    // Update UI for fully finished stage
    $('.stage-item').each(function() {
        let key = $(this).data('stage');
        if (finishedSet.has(key)) {
            $(this).addClass('completed');
        }
      });

    updateProgress();
}

function saveProgress(part=null, sound=null) {
    let partStatus = false, soundStatus = false;
    if (part == null || explored_parts.includes(part)) partStatus = true;
    if (sound == null || explored_sounds.includes(sound)) soundStatus = true;
    if (partStatus && soundStatus) return;

    $.ajax({
        url: '/save_tutorial_progress',
        type: 'POST',
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            category: category,
            part: part,
            sound: sound,
            finished: exploredParts.size == totalParts,
        }),
        success: function(response) {
            console.log('Progress saved:', response);
            console.log('Part:', part);
            console.log('Sound:', sound);
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request);
            console.log(status);
            console.log(error);
        }
    });
}

// Function to calculate progress
function calcProgress() {
    let progress = `Progress: <span class="speech-bubble-text-highlight">  ${exploredParts.size}/${totalParts}</span>`;
    return progress;
}

// Function to update bubble text content
function updateResponse(content) {
    bubbleText.html(content);
}

// Function to update warning message 
function updateWarning(content) {
    warning.removeClass('inactive').html(`<div class="speech-bubble-text warning">${content}</div>`);
}

// Function to build bubble text content
function buildResponse(part, bodyLanguage, soundFilesData) {
    let response = `You found the <span class="kawaii-behavior-highlight">${part}</span>`;
    
    if (part == 'sound' && soundFilesData) response += ` (check out 🎵)`
    
    response += `<ul class="kawaii-behavior-list">`;
    if (part == 'sound' && soundFilesData) {
        soundFiles = soundFilesData.split(',');
        bodyLanguage.split(',').forEach((desc, i) => {
            let cap = desc.trim().replace(/^./, c => c.toUpperCase());
            response += `<li>${cap} <span class="sound-icon" data-sound="/static/sounds/${soundFiles[i].trim()}">🎵</span></li>`;
        });
    } else {
        response += bodyLanguage.split(',')
                .map(item => `<li>${item.trim().replace(/^./, c => c.toUpperCase())}</li>`)
                .join('');
    }
    
    response += '</ul>';
    return response;
}

// Function to play sound
function playSound(icon, soundFile) {
    // If same icon clicked again or other body parts are clicked, stop playback
    if (currentSound && icon.is(currentIcon)) {
        currentSound.pause();
        currentSound.currentTime = 0;
        icon.css('transform', 'scale(1)').text('🎵');
        currentSound = currentIcon = null;
        return;
    }

    $(document).on('click', 'button, a.kawaii-button, .other-clickable', function(e){
        // if this click wasn’t on .sound-icon, stop the audio
        if (currentAudio) {
          currentAudio.pause();
          currentAudio.currentTime = 0;
          currentAudio = null;
        }
    });
    // Stop any existing audio
    if (currentSound) {
        currentSound.pause();
        currentSound.currentTime = 0;
        currentIcon.css('transform', 'scale(1)').text('🎵');
    }

    // Play new audio
    currentSound = new Audio(soundFile);
    currentIcon = icon;
    icon.css('transform', 'scale(1.2)').text('🎶');

    currentSound.play()
        .then(() => {
            currentSound.onended = () => {
                icon.css('transform', 'scale(1)').text('🎵');
                currentSound = currentIcon = null;                
            };
        })
        .catch(err => {
            console.error('Audio playback failed:', err);
            icon.css('transform', 'scale(1)').text('🎵');
            currentSound = currentIcon = null;
        });

    // Track played sounds and update progress
    exploredSounds.add(soundFile);
    saveProgress(null, soundFile);
    if (exploredSounds.size == soundFiles.length) {
        exploredParts.add('sound');
        saveProgress('sound');
        clickZones.filter('[data-part="sound"]').addClass('explored');
        warning.addClass('inactive').empty();
        updateProgress();
    };

    $(document).on('click', 'button, a.kawaii-button, .click-zone', function(e) {
        if (!currentSound) return;

        currentSound.pause();
        currentSound.currentTime = 0;
        if (currentIcon) {
          currentIcon.css('transform','scale(1)').text('🎵');
        }
    });
}

// Function to update progress
function updateProgress() {
    let existProg = bubbleText.find('.progress-message');
    let prog = calcProgress();
    let finishedSet = new Set(finished_sessions || []);
    let newProg; 
    
    if (exploredParts.size == totalParts) {
        finishedSet.add(category);
        newProg = `<div class="progress-message">${prog}&nbsp;&nbsp;Click <span class="kawaii-behavior-highlight">next</span> to continue</div>`;
        //nextButton.addClass('scale');
        warning.empty();
        $('.stage-item').filter(`[data-stage="${category}"]`).addClass('completed');

        if (finishedSet.size === 4) {
            $('.stage-start-quiz').html(`
            <a href="/quiz/start" class="kawaii-button start-button"> Go To Quiz</a>`)
        }
    } else {
        newProg = `<div class="progress-message">${prog}</div>`;
    }

    if(existProg.length) 
        existProg.replaceWith(newProg);
    else
        bubbleText.append(newProg);
    
}

function getWarning(e) {
    let isValid = true;
    let warningMessage = '';

    // Check body parts exploration
    if (exploredParts.size < totalParts) {
        warningMessage += bodyWarning;
        isValid = false;
    }
    // Check sound exploration (only if sound files exist)
    if (soundFiles.length > 0 && exploredSounds.size < soundFiles.length) {
        warningMessage += soundWarning;
        isValid = false;
    }

    // Show warning if validation failed
    if (!isValid && e) {
        e.preventDefault();
        updateWarning(warningMessage);
    }

    return isValid;
}

// Document ready handler
$(document).ready(function() {
    // Initialize DOM elements
    category = scenario['emotion'];
    bubbleText = $('.speech-bubble .speech-bubble-text.small');
    warning = $('.speech-bubble.warning');
    clickZones = $('.click-zone');
    nextButton = $('.kawaii-button.next-button');
    
    // Initialize state variables
    totalParts = clickZones.length;
    prepProgress();

    // Initialize UI
    warning.addClass('inactive').empty();
    updateResponse(`Explore the cat to reveal clickable points <br><br>${calcProgress()}`);

    // Click zone handler
    clickZones.on('click', function() {
        warning.addClass('inactive').empty();

        let part = $(this).data('part');
        let bodyLanguage = $(this).data('response').toLowerCase();
        let soundFilesData = $(this).data('sound-files');
    
        response = buildResponse(part, bodyLanguage, soundFilesData);

        if (prevPart == 'sound' && exploredSounds.size < soundFiles.length) {
            updateWarning(soundWarning);
        }
        else {
            // Update explored parts
            if (part !== 'sound' || soundFiles.length == 0) {
                exploredParts.add(part);
                saveProgress(part);
                $(this).addClass('explored');
            }

            updateResponse(response);
            updateProgress();

            prevPart = part;
        }
    });

    // Next button handler
    nextButton.on('click', function(e) {
        getWarning(e);
    });
    
    // Sound icon click handler
    $(document).on('click', '.sound-icon', function() {
        playSound($(this), $(this).data('sound'));
    });

    // Clean up on page unload
    $(window).on('beforeunload', function() {
        if (currentSound) {
            currentSound.pause();
            currentSound = null;
        }
    });
});