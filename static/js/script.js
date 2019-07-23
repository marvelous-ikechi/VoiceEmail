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
    recognition.continuous = true;
    recognition.interimResults = true;

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