var common_ops = {

    errmsg: function (msg) {
        layer.msg(msg, {icon: 5, offset: '100px'})
    },
    msg: function (msg) {
        layer.msg(msg, {icon: 1, offset: '100px'})
    },
    confirm: function (msg, callback) {
        callback = ( callback != undefined ) ? callback : {'ok': null, 'cancel': null};
        layer.confirm(msg, {
            btn: ['确定', '取消'] //按钮
        }, function (index) {
            //确定事件
            if (typeof callback.ok == "function") {
                callback.ok();
            }
            layer.close(index);
        }, function (index) {
            //取消事件
            if (typeof callback.cancel == "function") {
                callback.cancel();
            }
            layer.close(index);
        });
    },
    ajax: function (method, url, data,contentType="application/json; charset=utf-8",async=true,processData=true) {
        var p = new Promise(function (resolve, reject) {
            $.ajax({
                type: method,
                url: url,
                data: data,
                async: async,
                dataType:'json',
                contentType: contentType,
                processData: processData,
                success: function (ret) {
                    if (ret.code == 0) {
                        if (ret.data) {
                            resolve(ret.data);
                        } else {
                            layer.msg(ret.msg, {icon: 1, offset: '100px'})
                            resolve(true);
                        }
                    } else {
                        resolve(false);
                        layer.msg(ret.msg, {icon: 5, offset: '100px'})
                    }

                },
                error: function (xhr, textStatus, errorThrown) {
                    var msg = "系统错误 状态码:"
                    if (xhr.status == 403) {
                        msg = "操作没有权限"
                        layer.msg(msg, {icon: 5, offset: '100px'})
                    }else if(xhr.status == 500){
                        msg = xhr.responseJSON.msg
                        layer.msg(msg, {icon: 5, offset: '100px'})
                    } else {
                        layer.msg(msg + xhr.status, {icon: 5, offset: '100px'})
                    }
                    console.log(xhr)
                    reject();
                }
            });
        })
        return p;
    },

    highLight: function (e) {
        var old = e.css("border-color")
        e.css("border-color", "red")
        setTimeout(function () {
            e.css("border-color", old)
        }, 1000);
    }
}

Date.prototype.pattern = function (fmt) {
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours() % 12 == 0 ? 12 : this.getHours() % 12, //小时
        "H+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    var week = {
        "0": "/u65e5",
        "1": "/u4e00",
        "2": "/u4e8c",
        "3": "/u4e09",
        "4": "/u56db",
        "5": "/u4e94",
        "6": "/u516d"
    };
    if (/(y+)/.test(fmt)) {
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    }
    if (/(E+)/.test(fmt)) {
        fmt = fmt.replace(RegExp.$1, ((RegExp.$1.length > 1) ? (RegExp.$1.length > 2 ? "/u661f/u671f" : "/u5468") : "") + week[this.getDay() + ""]);
    }
    for (var k in o) {
        if (new RegExp("(" + k + ")").test(fmt)) {
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
        }
    }
    return fmt;
}
String.prototype.bool = function () {
    return (/^true$/i).test(this);
};
