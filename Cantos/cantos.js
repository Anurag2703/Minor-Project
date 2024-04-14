// Go To Top Button
let mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}



// SPEECH SYNTHESIS API
// Global variable to store the current utterance
var currentUtterance = null;

// Function to start reading the content
function startReading(contentID) {
    // Cancel any ongoing speech session
    stopReading();

    // Get the text content
    var text = document.getElementById(contentID).textContent;

    // Split text into sentences
    var sentences = text.split('.');

    // Create an empty array to store SpeechSynthesisUtterance objects
    var utterances = [];

    // Iterate over each sentence and create SpeechSynthesisUtterance objects
    sentences.forEach(function(sentence) {
        var utterance = new SpeechSynthesisUtterance(sentence.trim());
        utterances.push(utterance);
    });

    // Store the utterances array in the currentUtterance variable
    currentUtterance = utterances;

    // Start speaking each utterance in the utterances array sequentially
    speakUtterances(0);
}

// Function to start speaking each utterance in the utterances array sequentially
function speakUtterances(index) {
    if (index < currentUtterance.length) {
        window.speechSynthesis.speak(currentUtterance[index]);
        currentUtterance[index].onend = function() {
            speakUtterances(index + 1);
        }
    }
}

// Function to stop reading
function stopReading() {
    if (currentUtterance) {
        // Cancel any ongoing speech session
        window.speechSynthesis.cancel();
        // Reset the currentUtterance variable to null
        currentUtterance = null;
    }
}