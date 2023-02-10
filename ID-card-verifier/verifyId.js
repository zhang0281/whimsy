/**
 * json文件位置
 * @type {string} 文件地址
 */
// let jsonFilePath = "./pca-code.json"
let jsonFilePath = "https://raw.githubusercontent.com/modood/Administrative-divisions-of-China/master/dist/pca-code.json"

/**
 * 校验结果
 *
 *  success：成功
 *  failIdIllegal：身份证非法
 *  failAreaDoesNotExist：地区不存在
 *  failAgeTooOld：年龄超限
 *  failCheckCodeError：校验失败
 */
let result = {
    success: {
        code: '0',
        msg: '校验成功',
        data: {}
    },
    failIdIllegal: {
        code: '1',
        msg: '校验失败，身份证未输入或位数不为18位'
    },
    failAreaDoesNotExist: {
        code: '1',
        msg: '校验失败，身份证地区不存在'
    },
    failAgeTooOld: {
        code: '1',
        msg: '校验失败，身份证年龄错误'
    },
    failCheckCodeError: {
        code: '1',
        msg: '校验失败，身份证校验位错误'
    }
}

/**
 * 身份证校验
 * @param id 身份证
 * 返回校验结果
 * 校验成功 - {msg: string, code: string, data: {}}
 *      code为0
 *      msg为"校验成功"
 *      数据结构解释
 *          "data":{"provinceName": 省名称,"cityName": 市名称,"areaName": 县名称,"code": 行政区划编码,"validPeriod": 身份证有效期，可要求填入有效期以作对比,"gender":性别}}
 * 失败 - {msg: string, code: string}
 *      code为1
 *      msg为错误详情
 */
function verifyId(id) {
    if (!id || id.length !== 18) {
        return result.failIdIllegal
    }

    let date = new Date();
    // 当前年
    let year = date.getFullYear();
    // 身份证相关信息 start
    // 省市县
    let idArea = id.substring(0, 6);
    // 出生日期-年
    let idYear = id.substring(6, 10);
    // 顺序码
    let idSequenceCode = id.substring(14, 17);
    // 校验码
    let idCheckCode = id.substring(17, 18);
    // 身份证相关信息 end

    // 校验地区是否存在 start
    let pcaCodeJson = JSON.parse(loadAreasJson(jsonFilePath));
    // 省数据查找
    pcaCodeJson.forEach(pcaItem => {
        if (pcaItem.code === idArea.substring(0, 2)) {
            // 市数据查找
            pcaItem.children.forEach(cityItem => {
                if (cityItem.code === idArea.substring(0, 4)) {
                    // 县数据查找
                    cityItem.children.forEach(areaItem => {
                        if (areaItem.code === idArea) {
                            result.success.data = {
                                provinceName: pcaItem.name,
                                cityName: cityItem.name,
                                areaName: areaItem.name,
                                code: areaItem.code,
                            }
                        }
                    })
                }
            })
        }
    })
    if (!result.success.data.provinceName) {
        return result.failAreaDoesNotExist
    }
    // 校验地区是否存在 end

    // 校验有效期是否合法 start
    let idAge = year - idYear;
    if (idAge < 16) {
        result.success.data.validPeriod = "5"
    } else if (idAge >= 16 && idAge <= 25) {
        result.success.data.validPeriod = "10"
    } else if (idAge >= 26 && idAge <= 45) {
        result.success.data.validPeriod = "20"
    } else if (idAge >= 46 && idAge <= 150) {
        result.success.data.validPeriod = "长期有效"
    } else {
        return result.failAgeTooOld
    }
    // 校验有效期是否合法 end

    // 获取出生年月日
    result.success.data.birthday = idYear + "-" + id.substring(10, 12) + "-"  + id.substring(12, 14)
    // 获取年龄
    result.success.data.age = idAge
    // 获取性别
    result.success.data.gender = idSequenceCode % 2 === 0 ? "女" : "男"

    // 校验位检查 start
    // 校验系数数组校验系数
    let checkCodeArray = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
    // 位数对应校验位
    let checkDigit = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'];
    let checkCode = 0;
    id.substring(0, id.length - 1).split("").forEach((item, index) => {
        checkCode += parseInt(item) * checkCodeArray[index]
    })
    checkCode = checkCode % 11;
    if (checkDigit[checkCode].toLowerCase() !== idCheckCode.toLowerCase()) {
        return result.failCheckCodeError
    }
    // 校验位检查 end

    return result.success;
}

/**
 * 读取JSON文件
 * @param jsonFilePath json文件地址
 * @returns {string} json文件内容
 */
function loadAreasJson(jsonFilePath) {
    return $.ajax({
        url: jsonFilePath,
        type: "GET",
        dataType: "json",
        async: false,
        success: data => {
            return data
        }
    }).responseText;
}

