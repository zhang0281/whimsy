let nameList = []
let idList = []
let resultList = []

document.querySelectorAll("div.collectionItemDetails > a").forEach((e)=>{
    nameList.push(e.querySelector("div").innerText)
    idList.push(e.href.split("?id=")[1])
    resultList.push({
        name:e.querySelector("div").innerText,
        id:e.href.split("?id=")[1]
    })
})

function fmtResult(rList){
    let str = "";
    rList.forEach(e => {
        str += `${e.id}.jpg\n${e.id}.vpk\n`
    });
    return str;
}
console.log(resultList)
console.log(fmtResult(resultList))