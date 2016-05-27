var Account = Class.extend({
    init: function(opt){
        this.name = opt.name;
        this.money = opt.money;
        this.originMoney = opt.money;
        this.ma = opt.ma;
        this.moneyArr = [];
        this.needBuy = opt.needBuy;
        this.needSell = opt.needSell;
    },
    name: '',
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
            if (this.needBuy(preData)) {
                this.buy(data);
            }
        }
        if (this.hasStock) {
            if (this.needSell(preData)) {
                //console.log(this.singleProfit);
                this.sell(data);
                //console.log(data.time);
            }
        }
    }
});
