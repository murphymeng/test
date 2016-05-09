$(document).ready(function() {
    $.ajax({
        url: 'szzs.json',
    }).done(function(dataList) {
        dataList = dataList.filter(function(data) {
            var d = new Date(data.time);
            var d2 = new Date('2016-01-01');
            return d.getTime() > d2.getTime();
        });
        var preData;
        var money = dataList[0].close;
        //var money = 1;
        var buyData;
        var hasStock;
        var keepDay = 0;
        var moneyArr = [];
        var dateArr = [];
        var baseArr = [];


        var buy = function(data) {
            hasStock = true;
            buyData = data;
        }

        var sell = function(data) {
            hasStock = false;
            //money = money * (data.close / buyData.open);
        }

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


                if (idx >= 4) {
                    data.volume5 = getAvgVol(data, 5);
                    //console.log(data.volume5);
                }
                if (idx >= 29) {
                    data.volume30 = getAvgVol(data, 30);
                    //console.log(data.volume5);
                }

                if (hasStock) {
                    if (data.idx - buyData.idx === 1) {
                        money = money * (data.close / preData.open);
                    } else {
                        money = money * (data.close / preData.close);
                    }
                }
                //if ( preData.close > preData.ma20  ) { // 大于20天均线买入
                //if ( preData.macd > 0 ) { // macd大于0买入
                // data.volume / preData.volume > 1
                if (data.volume / preData.volume > 1 && preData.close > preData.ma20 ) {
                    if (!hasStock) {
                        buy(data);
                        //keepDay = 0;
                    }
                } else {
                    if (hasStock) {
                        sell(data);
                    }
                }

                // if (hasStock && keepDay === 2) {
                //     sell(data);
                // }

                // if (hasStock) {
                //     keepDay++;
                // }
                //
                // if (!hasStock) {
                //
                //     if (data.open >= preData.close) {
                //         buy(data);
                //         keepDay = 0;
                //     }
                //
                // } else if (hasStock && keepDay === 2) {
                //     sell(data);
                // }

                //if (hasStock) {
                // console.log(data.close / data.open);
                // console.log(data.open);
                // console.log(data.close);
                    // money = money * (data.close / preData.close)

                //}
            }
            dateArr.push(formatDate(data.time))
            baseArr.push(data.close);
            moneyArr.push(money);
            preData = data;

        })

        console.log(money)

        //return;
        $('#container').highcharts({
            chart: {
                type: 'line',
                zoomType: 'x'
            },
            title: {
                text: '收益图',
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
            series: [{
                name: '我的策略',
                data: moneyArr
            }, {
                name: '我的策略',
                data: baseArr
            }],
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
