// http://www.cuishuai.cc/game/
let a = 0
let interval = setInterval(function () {
    if (++a >= 50) {
        clearInterval(interval)
    }
    let resultColorArr = []
    for (let i in $('#box')[0].children) {
        let element = $('#box')[0].children[i]
        if (element.tagName === 'SPAN') {
            let elementBackgroundColor = element.style.backgroundColor
            if (resultColorArr[elementBackgroundColor] != null) {
                resultColorArr[elementBackgroundColor] += 1
            } else {
                resultColorArr[elementBackgroundColor] = 1
            }
        }
    }
    let resultColor = ''
    for (let i in resultColorArr) {
        if (resultColorArr[i] === 1) {
            resultColor = i
        }
    }
    for (let i in $('#box')[0].children) {
        let element = $('#box')[0].children[i]
        if (element.tagName === 'SPAN') {
            if (element.style.backgroundColor == resultColor) {

                i = parseInt(i) + 1

                let spanNum = $('#box')[0].children.length
                let l = Math.ceil(i / Math.sqrt(spanNum))
                let c = i % Math.sqrt(spanNum)
                if (i % Math.sqrt(spanNum) === 0) {
                    c = Math.sqrt(spanNum)
                }
                element.click()
                console.log(`点击了第${(i)}个方块 (第${l}行第${c}列)`)
                break
            }
        }
    }
}, 100)