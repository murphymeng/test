var request = require('request');
var url = "https://xueqiu.com/stock/forchartk/stocklist.json?symbol=SH600423&period=1day&type=before&end=1463365186825&_=1463365186825";
var url = "http://baidu.com";
request(url, function (error, response, body) {
  console.log(response.statusCode);
  if (!error && response.statusCode == 200) {
    //console.log(response) // 打印google首页
  }
})
