try{
    var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition()
}
catch (e) {
    console.error(e);
    $('.no-browser-support').show();
    $('.app').hide();
}

recognition.onstart = function () {
    instructions.text('Voice recognition activated. Try speaking into the microphone.');
}
recognition.onend = function () {
    instructions.text('You were quiet for a while so voice recognition turned itself off.');
}

var messageTextarea = $('#message-textarea');
var instructions = $('#recording-instructions');
var messageContent = '';


recognition.onerror = function () {
    if (event.error == 'no-speech'){
        instructions.text('No speech was detected. Try again.');
    }
}
recognition.onresult = function (event) {
     // event is a SpeechRecognitionEvent object.
  // It holds all the lines we have captured so far.
  // We only need the current one.
  var current = event.resultIndex;

  // Get a transcript of what was said.
  var transcript = event.results[current][0].transcript;

  // Add the current transcript to the contents of our Note.
  messageContent += transcript;
  messageTextarea.val(messageContent);
}
$('#message-textarea').on('mouseenter', function(e) {
  recognition.start();
});

function readOutLoud(message) {
  var speech = new SpeechSynthesisUtterance();

  // Set the text and voice attributes.
  speech.text = message;
  speech.volume = 1;
  speech.rate = 1;
  speech.pitch = 1;

  window.speechSynthesis.speak(speech);
}