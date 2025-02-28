function studyCheat(times) {
    let scool = document.getElementById("app").__vue__.$slots.default[1].elm.children[0].children[0].__vue__;
    // console.log(scool.playing);
    let study = document.getElementById("app").__vue__.$slots.default[1].elm.children[0].children[0].children[1].__vue__;
    console.log(study);
    for (let i = 0; i < times; i++) {
        setTimeout(() => {
            if (scool.playing === "math") {
                study.answer = study.solution;
                study.giveAnswerOnButton();
                document.getElementById("app").__vue__.$slots.default[1].elm.children[0].children[0].__vue__.timer = 3;
            } else if (scool.playing === "literature") {
                study.answer = study.words[0];
            }
        }, 10 * i)
    }
}

function addCheat() {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://etherdream.com/jsgear/jsgear.js';
    document.head.appendChild(script);
}

studyCheat(100)