function say(word){
    var utter = new SpeechSynthesisUtterance(word);
    speechSynthesis.speak(utter);
}

let webSpeech = function(words){

        let synth = window.speechSynthesis;
        let utterance = window.SpeechSynthesisUtterance;
        utterance.rate = 0.1;

        return synth.speak(new utterance(words));
    }
    window.addEventListener('load',function(){

     say("You can read mails, create mails, delete mails and sign out on this page.");
    })

function speech_recognition(){
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.lang = 'en-Us';
    recognition.start();

    recognition.onresult = function (e) {
        document.getElementById('message').value = e.results[0][0].transcript;
    }
    recognition.onerror = function(e){
        recognition.stop();
    }


}