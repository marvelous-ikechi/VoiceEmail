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
