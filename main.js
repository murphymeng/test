$(document).ready(function() {
    $.ajax({
        url: './data/szzs.json',
    }).done(function(obj) {
        //dataList = obj.chartlist;
        dataList = obj;
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
            var d2 = new Date('2005-01-01');
            return d.getTime() > d2.getTime();
        });

        var accountList = [];
        var maArr = [10, 15, 20, 25, 30, 35, 60];

        $.each(maArr, function(idx, ma) {
            var account = new Account({
                ma: ma,
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
            }

            dateArr.push(formatDate(data.time))
            baseArr.push(data.close);
            ma5Arr.push(data.ma5);
            ma10Arr.push(data.ma10);
            preData = data;

        })

        var baseProfit = baseArr[baseArr.length - 1] / dataList[0].close;
        console.log('基准收益：' + baseProfit);
        //return;

        var series = [];
        $.each(accountList, function(idx, account) {

            var profit = account.money / account.originMoney;
            console.log(account.ma + '均线策略收益：' + profit);
            console.log('策略收益／基准收益：' + profit / baseProfit);

            series.push({
                name: account.ma,
                data: account.moneyArr
            })
        });
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

    })
})
