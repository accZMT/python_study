

var express = require('express')

var bodyParser = require('body-parser')
var fs = require('fs')
var multer = require('multer')
var web = express()
var form = multer()

web.use(express.static('public'))
web.use(bodyParser.urlencoded({ extended: false }))

web.post('/addNew', form.array(), function (req, res) {
    // 判断是否存在指定文件夹，如果存在则回调函数为True
    // 如果不存在 则回调函数值为False
    fs.exists('data', function (isExists) {
        if (!isExists) {
            fs.mkdirSync('data')

            var data = req.body
            var json = {
                data: data,
                des: '新增员工'
            }

            var jsonString = JSON.stringify(json)
            fs.writeFile('data/info.txt', jsonString, { flag: 'a' }, function (err) {
                if (err) {
                    console.log('写入失败')
                    res.send('添加失败')
                }
                else {
                    console.log('写入成功')
                    res.send('添加成功')

                }
            })
        }

        // var name = req.body.name
        // var code = req.body.code
        // var job = req.body.job
        // var card = req.body.card
        // var tel = req.body.tel
        // var time = req.body.currentTime

        // var json = {
        //     name: name,
        //     code: code,
        //     job: job,
        //     card: card,
        //     tel: tel,
        //     time: time
        // }
        else {
            var data = req.body
            var json = {
                data: data,
                des: '新增员工'
            }

            var jsonString = ',\n' + JSON.stringify(json)
            fs.writeFile('data/info.txt', jsonString, { flag: 'a' }, function (err) {
                if (err) {
                    console.log('写入失败')
                    res.send('添加失败')
                }
                else {
                    console.log('写入成功')
                    res.send('添加成功')

                }
            })
        }

    })

})

web.get('/getinfo', function (req, res) {

    fs.exists('data', function (isExists) {
        if (isExists) {
            fs.readFile('data/info.txt', function (err, data) {
                if (err) {
                    res.send('读取失败')
                }
                else {
                    res.send('[' + data + ']')
                }
            })
        }
        else {
            res.send('员工信息为空！请添加信息')
        }
    })
})

web.listen('8080', function (req, res) {
    console.log('服务器启动。。。')
})

// 1.index页面到new页面  window.location.href = 'new.html'
// 2.放置input标签，获取input标签 getElementsByName()后面不要追加.value 因为按照现在的代码input输入框里面还没有来得及写入内容  程序就已经加载完毕
// 3.将数据发送到后台 xhr的form请求方式
//   var form = new FormData()
//   form.append()
// 4.后台接收到数据“追加”到本地文件里面 appendFile  同时主要拼接成json格式  所以在后面追加","
// 5.index页面进行数据请求 获取全部数据
// 6.后台接收到请求后读取本地文件 readFile 将读取到的数据全部发送到前端  数据格式为 "1,2,3"
// 7.前端接收数据 将数据改为标准json字符串 转化成json 遍历 拼接 显示
