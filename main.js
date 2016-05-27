$(document).ready(function() {
    $.ajax({
<<<<<<< HEAD
        url: './data/SH601688.json',
=======
        url: './data/cybz.json',
>>>>>>> origin/master
    }).done(function(obj) {
        //dataList = obj.chartlist;
        var symbol;
        if (obj.chartlist) {
            dataList = obj.chartlist;
            symbol = obj.stock.symbol;
        } else {
            dataList = obj;
        }

        var getAvgVol = function(data, day) {
            var sum = 0;
            for (i = day; i >= 1; i--) {
                sum += dataList[data.idx - (i-1)].volume;
            }
            return sum / day;
        }

        var getAvgPrice = function(data, day) {
            var sum = 0;
            for (i = day; i >= 1; i--) {
                sum += dataList[data.idx - (i-1)].close;
            }
            return sum / day;
        }

        // 预处理数据
        $.each(dataList, function(idx, data) {
            data.idx = idx;
            if (idx > 60) {

                for (var i = 5; i < 61; i++) {
                    data['ma' + i] = getAvgPrice(data, i);
                }
                // data.ma3 = getAvgPrice(data, 3);
                // data.vol20 = getAvgVol(data, 20);
                // data.vol10 = getAvgVol(data, 10);
                // data.vol5 = getAvgVol(data, 5);
                // data.vol30 = getAvgVol(data, 30);
                // data.vol60 = getAvgVol(data, 60);
            }
            //
            // console.log('my ma5: ' + data.ma5_me);
            // console.log('ma5:' + data.ma5);
        });

        dataList = dataList.filter(function(data) {
            var d = new Date(data.time);
            var d2 = new Date('2007-10-16');
            return d.getTime() > d2.getTime() && data.ma60;
        });

        var accountList = [];


        // macd策略
        var account = new Account({
            name: 'macd',
            needBuy: function(preData) {
                return preData.macd >= 0;
            },
            needSell: function(preData) {
                return preData.macd < 0;
            },
            money: dataList[0].close
        });
        accountList.push(account);

        var maArr = [];
        for (var i = 5; i < 60; i++) {
            maArr.push(i);
        }

        //maArr = [20];

        $.each(maArr, function(idx, ma) {
            var account = new Account({
                name: 'ma' + ma,
                needBuy: function(preData) {
                    return preData.close > preData['ma' + ma];
                },
                needSell: function(preData) {
                    return preData.close < preData['ma' + ma];
                },
                money: dataList[0].close
            });
            accountList.push(account);
        })



        var preData;
        var moneyArr = [];
        var dateArr = [];
        var baseArr = [];
        var ma5Arr = [];
        var ma10Arr = [];
        var ma20Arr = [];

        var getAvgVol = function(data, day) {
            var sum = 0;
            for (i = day; i >= 1; i--) {
                sum += dataList[data.idx - (i-1)].volume;
            }
            return sum / day;
        }

        $.each(dataList, function(idx, data) {
            data.idx = idx;
            if (preData) {
                $.each(accountList, function(index, account) {
                    if (account.hasStock) {
                        if (data.idx - account.buyData.idx === 1) {
                            account.money = account.money * (data.close / preData.open);
                            account.keepDays += 2;
                            account.singleProfit = account.singleProfit * (data.close / preData.open);
                        } else {
                            account.money = account.money * (data.close / preData.close);
                            account.singleProfit = account.singleProfit * (data.close / preData.close);
                            account.keepDays++;
                        }
                    }
                    //if ( preData.close > preData.ma20  )  // 大于20天均线买入
                    //if ( preData.macd > 0 )  // macd大于0买入
                    // data.volume / preData.volume > 1
                    account.run({data: data, dataList:dataList});
                    account.moneyArr.push(account.money);
                });
                dateArr.push(formatDate(data.time))
                baseArr.push(data.close);
            }


            preData = data;

        })
        $.each(accountList, function(idx, account) {
            account.profit = account.money / account.originMoney;
        });

        var baseProfit = baseArr[baseArr.length - 1] / dataList[0].close;
        console.log('基准收益：' + baseProfit);
        //return;

        var series = [];

        var bestAccount = _.max(accountList, function(account) {
            return account.money;
        });
        console.log(bestAccount.ma + '均线策略收益：' + bestAccount.profit);
        console.log('策略收益／基准收益：' + bestAccount.profit / baseProfit);

        series.push({
            name: bestAccount.name,
            data: bestAccount.moneyArr
        });

        // series.push({
        //     name: accountList[15].ma,
        //     data: accountList[15].moneyArr
        // })

        series.push({
            name: '基准',
            data: baseArr
        });

        $('#container').highcharts({
            chart: {
                type: 'line',
                zoomType: 'x'
            },
            title: {
                text: '',
                x: -20 //center
            },
            subtitle: {
                text: 'by murphy    ',
                x: -20
            },
            xAxis: {
                categories: dateArr,
                min: 0,
                max: 600
            },
            yAxis: {
                title: {
                    text: ''
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                //valueSuffix: '°C'
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: series,
            scrollbar: {
                enabled: true,
                barBackgroundColor: 'gray',
                barBorderRadius: 7,
                barBorderWidth: 0,
                buttonBackgroundColor: 'gray',
                buttonBorderWidth: 0,
                buttonArrowColor: 'yellow',
                buttonBorderRadius: 7,
                rifleColor: 'yellow',
                trackBackgroundColor: 'white',
                trackBorderWidth: 1,
                trackBorderColor: 'silver',
                trackBorderRadius: 7
            }
        });

        var maList = ['base'];
        var profitList = [baseProfit];
        $.each(accountList, function(idx, account) {
            maList.push(account.name);
            profitList.push(account.profit);
        });

        $('#container2').highcharts({
            chart: {
                zoomType: 'xy'
            },
            title: {
                text: symbol
            },
            subtitle: {
                text: 'by murphy'
            },
            xAxis: [{
                categories: maList,
                crosshair: true
            }],
            yAxis: [{ // Primary yAxis
                labels: {
                    format: '',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                },
                title: {
                    text: '收益',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                }
            }, { // Secondary yAxis
                title: {
                    text: 'Rainfall',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                labels: {
                    format: '{value} mm',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                opposite: true
            }],
            tooltip: {
                shared: true
            },
            legend: {
                layout: 'vertical',
                align: 'left',
                x: 120,
                verticalAlign: 'top',
                y: 100,
                floating: true,
                backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
            },
            series: [{
                name: '收益',
                type: 'column',
                data: profitList,
                tooltip: {
                    valueSuffix: ''
                }
            }]
        });

    })
})
