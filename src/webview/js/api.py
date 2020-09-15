src = """
window.pywebview = {
    token: '%s',
    platform: '%s',
    api: {},

    _createApi: function(funcList) {
        for (var i = 0; i < funcList.length; i++) {
            var funcName = funcList[i].func;
            var params = funcList[i].params;

            var funcBody =
                "var get_id = (Math.random() + '').substring(2); " +
                "var promise = new Promise(function(resolve, reject) { " +
                    "window.pywebview._checkValue('" + funcName + "', resolve, reject, get_id); " +
                "}); " +
                "window.pywebview._bridge.call('" + funcName + "', JSON.stringify(arguments), get_id); " +
                "return promise;"

            console.log("loading " + funcName);

            let funcPath = funcName.split("__")

            let funcNode = window.pywebview.api;
            for (let i = 0; i < funcPath.length - 1; i++) {
                if (!funcNode.hasOwnProperty(funcPath[i])) {
                    funcNode[funcPath[i]] = {};
                }
                funcNode = funcNode[funcPath[i]];
            }

            funcNode[funcPath[funcPath.length - 1]] = new Function(params, funcBody)
            // window.pywebview.api[funcName] = new Function(params, funcBody)
            window.pywebview._returnValues[funcName] = {}
        }
    },

    _bridge: {
        call: function (funcName, params, get_id) {
            switch(window.pywebview.platform) {
                case 'mshtml':
                case 'cef':
                case 'qtwebkit':
                    return window.external.call(funcName, params, get_id);
                case 'edgehtml':
                    return window.external.notify(JSON.stringify([funcName, params, get_id]));
                case 'cocoa':
                    return window.webkit.messageHandlers.jsBridge.postMessage(JSON.stringify([funcName, params, get_id]));
                case 'qtwebengine':
                    new QWebChannel(qt.webChannelTransport, function(channel) {
                        channel.objects.external.call(funcName, params, get_id);
                    });
                    break;
                case 'gtk':
                    document.title = JSON.stringify({"type": "invoke", "uid": "%s", "function": funcName, "param": params, "get_id": get_id});
                    break;
            }
        }
    },

    _checkValue: function(funcName, resolve, reject, get_id) {
         var check = setInterval(function () {
            var returnObj = window.pywebview._returnValues[funcName][get_id];
            if (returnObj) {
                var value = returnObj.value;
                var isError = returnObj.isError;

                delete window.pywebview._returnValues[funcName][get_id];
                clearInterval(check);

                if (isError) {
                    var pyError = JSON.parse(value);
                    console.log(pyError);
                    // var error = new Error(pyError.message);
                    var error = new Error("Python Error: \\n-> " + pyError.stack);
                    error.name = pyError.name;
                    error.stack = pyError.stack;

                    reject(error);
                } else {
                    resolve(JSON.parse(value));
                }
            }
         }, 100)
    },

    _returnValues: {}
}
window.pywebview._createApi(%s);
window.dispatchEvent(new CustomEvent('pywebviewready'));
"""


src_old = """
window.pywebview = {
    token: '%s',
    platform: '%s',
    api: {},

    _createApi: function(funcList) {
        for (var i = 0; i < funcList.length; i++) {
            var funcName = funcList[i].func;
            var params = funcList[i].params;

            var funcBody =
                "var get_id = (Math.random() + '').substring(2); " +
                "var promise = new Promise(function(resolve, reject) { " +
                    "window.pywebview._checkValue('" + funcName + "', resolve, reject, get_id); " +
                "}); " +
                "window.pywebview._bridge.call('" + funcName + "', JSON.stringify(arguments), get_id); " +
                "return promise;"

            window.pywebview.api[funcName] = new Function(params, funcBody)
            window.pywebview._returnValues[funcName] = {}
        }
    },

    _bridge: {
        call: function (funcName, params, get_id) {
            switch(window.pywebview.platform) {
                case 'mshtml':
                case 'cef':
                case 'qtwebkit':
                    return window.external.call(funcName, params, get_id);
                case 'edgehtml':
                    return window.external.notify(JSON.stringify([funcName, params, get_id]));
                case 'cocoa':
                    return window.webkit.messageHandlers.jsBridge.postMessage(JSON.stringify([funcName, params, get_id]));
                case 'qtwebengine':
                    new QWebChannel(qt.webChannelTransport, function(channel) {
                        channel.objects.external.call(funcName, params, get_id);
                    });
                    break;
                case 'gtk':
                    document.title = JSON.stringify({"type": "invoke", "uid": "%s", "function": funcName, "param": params, "get_id": get_id});
                    break;
            }
        }
    },

    _checkValue: function(funcName, resolve, reject, get_id) {
         var check = setInterval(function () {
            var returnObj = window.pywebview._returnValues[funcName][get_id];
            if (returnObj) {
                var value = returnObj.value;
                var isError = returnObj.isError;

                delete window.pywebview._returnValues[funcName][get_id];
                clearInterval(check);

                if (isError) {
                    var pyError = JSON.parse(value);
                    var error = new Error(pyError.message);
                    error.name = pyError.name;
                    error.stack = pyError.stack;

                    reject(error);
                } else {
                    resolve(JSON.parse(value));
                }
            }
         }, 100)
    },

    _returnValues: {}
}
window.pywebview._createApi(%s);
window.dispatchEvent(new CustomEvent('pywebviewready'));
"""