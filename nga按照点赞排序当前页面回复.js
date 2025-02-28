
let sortList = []
let recommendvalueList = document.getElementsByClassName("recommendvalue")
for (let i in recommendvalueList) {
    if (isNaN(parseInt(i))) {
        continue
    }
    sortList.push({
        recommendvalue: recommendvalueList[i].innerHTML === "&nbsp;" ? 0 : parseInt(recommendvalueList[i].innerHTML),
        recommendvalueDOM: recommendvalueList[i]
    })
}
sortList.sort((start, next) => {
    return next.recommendvalue - start.recommendvalue
})
sortList.map(e => {
    console.log("推荐值：", e.recommendvalue, e.recommendvalueDOM)
})