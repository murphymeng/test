$(document).ready(function() {
    $.ajax({
        url: 'szzs.json',
    }).done(function(dataList) {
        var a = dataList;
        var preData;
        var money = 1;
        var buyData;
        var hasStock;
        var keepDay = 0;


        var buy = function(data) {
            hasStock = true;
            buyData = data;
        }

        var sell = function(data) {
            hasStock = false;
            money = money * (data.close / buyData.open);
        }

        $.each(dataList, function(idx, data) {
            if (preData) {
                if (hasStock) {
                    keepDay++;
                }
                //if ( preData.close > preData.ma20  ) { // 大于20天均线买入
                //if ( preData.macd > 0 ) { // macd大于0买入
                if (data.volume / preData.volume > 1 && preData.close > preData.ma20) {
                    if (!hasStock) {
                        buy(data);
                        keepDay = 0;
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
                    // console.log(money)
                //}
            }
            preData = data;
        })

        console.log(money);
    })
})
