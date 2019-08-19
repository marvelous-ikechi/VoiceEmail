function say(word, onEnd) {
    const utterance = new SpeechSynthesisUtterance(word);
    if (onEnd != null) {

        utterance.onend = onEnd;
    }
    speechSynthesis.speak(utterance);
}

function mute(){
    const word = '';
    const utterance =  new SpeechSynthesisUtterance(word);
    utterance.cancel();
}

function speech_recognition(onResult, onError, options) {
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = options.continuous;
    recognition.interimResults = options.interimResults;

    recognition.lang = 'en-US';
    recognition.start();

    recognition.onresult = function (e) {
        onResult(e.results[0][0].transcript);

    }
    recognition.onerror = function (e) {
        recognition.stop();
        onError(e);
    }

}


function speechRecognitionSendEMail() {
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.lang = 'en-US';
    recognition.start();

    recognition.onresult = function (e) {
        const transcript = e.results[0][0].transcript;
        document.getElementById('message').innerHTML = transcript;
    }
    recognition.onerror = function (e) {
        recognition.stop();
    }

}