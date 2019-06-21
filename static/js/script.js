function say(word){
    var utter = new SpeechSynthesisUtterance(word);
    speechSynthesis.speak(utter);
}

function sendMail_say(word){
    var utter = new SpeechSynthesisUtterance(word);
    speechSynthesis.speak(utter);
}

let say_1 = function (words){
        webSpeech(words);
            }

    let webSpeech = function(words){

        let synth = window.speechSynthesis;
        let utterance = window.SpeechSynthesisUtterance;
        utterance.rate = 0.1;

        return synth.speak(new utterance(words));
    }
    window.addEventListener('load',function(){

     say("Welcome. You can read mail, create mail, delete mail and sign out on this page, Thank you");
    })
