$(document).ready(function() {


    $.get( "http://localhost:8000/results", {
    }, function( res ) {
        $('#money').html(res.money);
        var dateArr = [];
        var moneyArr = [];
        var baseArr = [];
        _.each(res.myList, function(item, idx) {
            //item.x = idx;
            item.y = item.money;
            dateArr.push(item.time);
            moneyArr.push(item.money);
            //baseArr.push(res['baseList'][idx].y);
        });

        new Vue({
          el: 'body',
          data: {
            sortKey: '',
            sortOrders: {},
            historyList: res.myList
          },
          methods: {
            sortBy: function(key) {
                this.sortKey = key;
                this.sortOrders[key] = this.sortOrders[key] * -1;
            }
          }
        })

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
                pointFormat: '{point.name} <br /> {point.y} 元 <br/> 买入日期： {point.buyTime} <br /> 买入日期： {point.sellTime} 单次收益：{point.profit}',
                //backgroundColor: 'red'
                //valueSuffix: '°C'
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: [{
                'name': '我的策略',
                'data': moneyArr
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

    });
})
