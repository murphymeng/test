$(document).ready(function() {


    $('#search').on('click', function() {
      var start_time = $('#start-time').val();
      var end_time = $('#end-time').val();
      $.get( "http://localhost:8000/results", {
        'start_time': start_time,
        'end_time': end_time
      }, function( res ) {
          $('#money').html(parseInt(res.money));
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

          if (!window.historyTable) {
             window.historyTable = $('#history-list').dataTable({
                "order": [[ 2, 'asc' ]],
                "data": res.myList,
                paging: true,
                "columns": [{
                  data: 'symbol'
                }, {
                  "data": "name",
                  render: function(val, d, obj) {
                      return "<a class='chart' data-buytime='"+obj.buyTime+"' data-selltime='"+obj.sellTime+"' name='"+val+"' id='"+ obj.symbol +"'>" + val + "</a><div class='hide'><div name='"+val+"' class='chart-content' id='chart-"+obj.symbol+"'></div></div>";
                  }
                }, {
                  "data": "buyTime"
                }, {
                  "data": 'sellTime'
                }, {
                  'data': 'profit'
                }]
              });
          } else {
              window.historyTable.fnClearTable();
              window.historyTable.fnAddData(res.myList);
          }


          $('#history-list').on('mouseover', '.chart', function() {
              targetEl = this;
              var symbol = this.id;
              var name = $(this).attr('name');
              var sell_time = this.dataset.selltime;
              var buy_time = this.dataset.buytime;

              $.get("http://localhost:8000/days", {
                    name: name,
                    symbol: symbol,
                    sell_time: sell_time,
                    buy_time: buy_time
              }).done(function(res) {
                  var symbol = res.symbol,
                      name = res.symbol;
                  var data = res.arr;
                  // split the data set into ohlc and volume
                  var ohlc = [],
                      volume = [],
                      dataLength = data.length,
                      // set the allowed units for data grouping
                      groupingUnits = [],

                      i = 0,
                      obj,
                      time;

                  for (i; i < dataLength; i += 1) {
                      time = new Date(data[i].time);
                      time = time.getTime();
                      obj = {
                          x: time, // the date
                          open: Number(data[i].open), // open
                          high: Number(data[i].high), // high
                          low: Number(data[i].low), // low
                          close: Number(data[i].close) // close,
                      };

                      if (data[i].time === res.sellTime || data[i].time === res.buyTime) {
                        if (data[i].close >= data[i].open) {
                          obj.color = 'red';
                        } else {
                          obj.color = 'blue';
                        }
                      }
                      ohlc.push(obj);

                      volume.push([
                          time, // the date
                          Number(data[i].volume) // the volume
                      ]);
                  }

                  if (!$('#chart-' + symbol).highcharts()) {

                      $('#chart-' + symbol).highcharts('StockChart', {
                          rangeSelector: {
                              buttons: [{
                                  type: 'day',
                                  count: 1,
                                  text: '1d'
                              }, {
                                  type: 'month',
                                  count: 3,
                                  text: '3m'
                              }, {
                                  type: 'year',
                                  count: 1,
                                  text: '1y'
                              }, {
                                  type: 'all',
                                  text: 'All'
                              }],
                              inputEnabled: false, // it supports only days
                              selected : 1, // all
                              inputDateFormat: '%Y-%m-%d'
                          },
                          colors: ['#080', '#434348', '#90ed7d', '#f7a35c',
                      '#8085e9', '#f15c80', '#e4d354', '#2b908f', '#f45b5b', '#91e8e1'],
                          title: {
                              text: name
                          },
                          tooltip: {
                              // borderColor: '#434348',
                              // crosshairs: true,
                              // animation: false,
                              //pointFormat: '开盘: {point.open} <br /> 收盘: {point.close} <br/> 最高： {point.high} <br /> 最低： {point.low}  <br /> 涨幅： {point.percentage}'
                              dateTimeLabelFormats: {
                                  day:"<strong>%Y-%m-%d</strong>",
                              }
                          },
                          yAxis: [{
                              labels: {
                                  align: 'right',
                                  x: -3
                              },
                              title: {
                                  text: 'k线图'
                              },
                              height: '76%',
                              lineWidth: 2
                          }, {
                              labels: {
                                  align: 'right',
                                  x: -3
                              },
                              title: {
                                  text: '成交量'
                              },
                              top: '80%',
                              height: '20%',
                              offset: 0,
                              lineWidth: 2
                          }],

                          chart: {
                              type: 'candlestick',
                              zoomType: 'x'
                          },

                          exporting: {
                              enabled: false
                          },

                          series: [{
                              name: name,
                              data: ohlc,
                              dataGrouping : {
                                  units : [
                                      [
                                          'day', // unit name
                                          [1] // allowed multiples
                                      ]
                                  ]
                              }
                          }, {
                              type: 'column',
                              name: '成交量',
                              data: volume,
                              yAxis: 1,
                              dataGrouping: {
                                  enabled: false
                                  //units: groupingUnits
                              }
                          }]
                      });
                  }
                  // create the chart
                  tooltip.pop(targetEl, '#chart-' + symbol);
              });
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
})
