# 身份证校验器-JS

一个用JS编写的身份证校验器，可校验身份证地区是否存在，身份证有效期是否合法，校验位检查。

以及获取对应省市区数据，身份证有效期，性别。

# 依赖

1. [中华人民共和国行政区划](https://github.com/modood/Administrative-divisions-of-China) -
   [“省份、城市、区县” 三级联动数据](https://raw.githubusercontent.com/modood/Administrative-divisions-of-China/master/dist/pca-code.json)
2. [jquery](https://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.8.0.js)

# 说明

## 目录结构

0. 行政区划在将来可能会有变化，此处```pca-code.json```文件作为缓存以便可以查找到可用版本。
1. 对于需要引用该校验器的项目来说，只需要引用```verifyId.js```后使用```verifyId函数```即可。
2. ```test.html``` 为使用实例，其中默认填写的身份证号来源于[网络](http://www.ip33.com/shenfenzheng.html)。

```
├─areas.json    # 引用的行政区划数据
├─readme.md     # 说明文旦
├─test.html     # 测试html 以及 用法实例
├─verifyId.js   # 主要验证js
```
