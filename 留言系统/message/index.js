

var express = require('express')
var bodyParser = require('body-parser')
var multer = require('multer')
var fs = require('fs')

var web = express()
var form = multer()

web.use(bodyParser.urlencoded({extended:false}))
web.use(express.static('public'))



web.post('/getinfo',form.array(),function(req,res){
    
    fs.exists('data',function(isExists){
        if(!isExists){
            fs.mkdirSync('data')
        }

        var info = req.body
        var infostring = JSON.stringify(info) + ',\n'

        fs.writeFile('data/info.txt',infostring,{flag:'a'},function(err){
            if(err){
                console.log('写入留言失败'+err)
               
            }
            else{
                console.log('写入留言成功')
               
            }
        })

        setTimeout(function(){
            fs.readFile('data/info.txt',function(err,data){
                if(err){
                    console.log('读取留言失败'+err)
                    res.send('留言失败')
                }
                else{
                    console.log('读取留言成功')
                    res.send(data)
                }
            })
        },200)
    })
})


web.listen('8000',function(req,res){
    console.log('服务器成功。。。')
})




