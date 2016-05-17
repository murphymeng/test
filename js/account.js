var Account = Class.extend({
    init: function(opt){
        this.money = opt.money;
        this.originMoney = opt.money;
        this.ma = opt.ma;
        this.moneyArr = [];
    },
    money: 0,
    originMoney: 0,
    hasStock: false,
    keepDays: 0,
    singleProfit: 1,
    moneyArr: null,
    reset: function() {
        this.keepDays = 0;
        this.singleProfit = 1;
    },
    buy: function(data) {
        this.hasStock = true;
        this.buyData = data;
    },
    sell: function(data) {
        this.hasStock = false;
        this.reset();
    },
    run: function(opt) {
        var preData = opt.dataList[opt.data.idx - 1];
        var data = opt.data;
        var ma = this.ma;


        if (!this.hasStock) {
            if (preData.close > preData['ma' + ma]) {
                this.buy(data);
            }
        }
        if (this.hasStock) {
            if (preData.close < preData['ma' + ma]) {
                //console.log(this.singleProfit);
                this.sell(data);
                //console.log(data.time);
            }
        }
    }
});
