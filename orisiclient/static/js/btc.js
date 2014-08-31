(function(){
  var global = this;

  var btc_observedAddresses = {};
  var btc_filterFunctionForAddress = {};
  var btc_alreadySeenTransactions = {};
  var btc_alwaysCheckTransactions = {};
  var btc_dateForAddress = {}
  var btc_waitingRequests = new Array();
  var btc_apiInterval = 300; // miliseconds before sending another request
  var btc_observeInterval = 5000;
  var btc_throttleIntervalId = null;
  var btc_observeIntervalId = null;

  var btc_throttle = function() {
    if (btc_waitingRequests.length == 0) {
      return;
    }

    request = btc_waitingRequests.shift();
    $.ajax(request);
  }

  var btc_filterTransactions = function(transactionList) {
    resultingList = new Array();

    for (var i=0; i < transactionList.length; ++i) {
      if (transactionList[i]['tx'] in btc_alwaysCheckTransactions) {
        resultingList.push(transactionList[i]);
      }
      if (!(transactionList[i]['tx'] in btc_alreadySeenTransactions)) {
        resultingList.push(transactionList[i]);
      }
    }
    return resultingList;
  }

  var btc_parseTransaction = function(data) {
    if (data['status'] != 'success') {
      return;
    }

    data = data['data'];

    trade = data['trade'];
    vouts = trade['vouts'];
    for (var i=0; i < vouts.length; ++i) {
      vout = vouts[i]
      if (vout['address'] in btc_observedAddresses) {
        if (btc_filterFunctionForAddress[vout['address']](data)) {
          btc_alwaysCheckTransactions[data['tx']] = true;
          btc_observedAddresses[vout['address']].push(data);
        }
      }
    }

    btc_alreadySeenTransactions[data['tx']] = true;
  }

  var btc_logError = function(data) {
    console.log(data);
  }

  var btc_investigateTransaction = function(tx) {
    btc_waitingRequests.push({
      dataType: 'json',
      url: 'http://btc.blockr.io/api/v1/tx/info/' + tx['tx'],
      data: {format:'json',cors:true},
      crossDomain:true,
      success: btc_parseTransaction,
      error: btc_logError,
    });
  }

  // Please partially apply address
  var btc_parseLastTransactions = function(data, textStatus, jqXHR, address) {
    if (typeof(address) === "undefined") {
      console.log("Please partially apply address!");
      return;
    }

    console.log(data);
    console.log(textStatus);
    console.log(jqXHR);

    if (data['status'] != 'success') {
      return;
    }

    data = data['data'];
    pre_transactions = data['txs'];
    transactions = []

    // We don't need too old transactions
    minimalDate = btc_dateForAddress[address];
    for (var i=0; i < pre_transactions.length; ++i) {
      txDate = new Date(pre_transactions[i]['time_utc']);
      if (txDate >= minimalDate) {
        transactions.push(pre_transactions[i]);
      }
    }

    transactions = btc_filterTransactions(transactions);

    for (var i = 0; i < transactions.length; ++i) {
      btc_investigateTransaction(transactions[i]);
    }
  }

  var btc_getLastTransactions = function(address) {
    console.log(btc_parseLastTransactions.bind(undefined, undefined, undefined, address));
    btc_waitingRequests.push({
      dataType: 'json',
      url: 'http://btc.blockr.io/api/v1/address/txs/' + address,
      data: {format:'json','limit':5, cors:true},
      crossDomain:true,
      success: btc_parseLastTransactions.bind(undefined, undefined, undefined, address)
    });
  }


  var btc_addObservedAddress = function(address, filterFunction, minimumDate) {
    btc_filterFunctionForAddress[address] = filterFunction;
    btc_observedAddresses[address] = []
    btc_dateForAddress[address] = minimumDate
  }

  var btc_observe = function() {
    for (address in btc_observedAddresses) {
      btc_getLastTransactions(address);
    }
  }

  var btc_run = function() {
    if (!btc_throttleIntervalId) {
      btc_throttleIntervalId = setInterval(btc_throttle, btc_apiInterval);
    }
    if (!btc_observeIntervalId) {
      btc_observe();
      btc_observeIntervalId = setInterval(btc_observe, btc_observeInterval);
    }
  }

  var btc_stop = function() {
    if (btc_throttleIntervalId) {
      clearInterval(btc_throttleIntervalId);
      btc_throttleIntervalId = null;
    }
    if (btc_observeIntervalId) {
      clearInterval(btc_observeIntervalId);
      btc_observeIntervalId = null;
    }
  }

  var btc_getMarkFunction = function(address, mark) {
    var myMark = mark;
    var myAddress = address;
    var markFunction = function(data) {
      trade = data['trade'];
      vouts = trade['vouts'];
      for (var i=0; i < vouts.length; ++i) {
        vout = vouts[i];
        if (vout['address'] == myAddress) {
          valueFloat = vout['amount'];
          valueString = valueFloat.toFixed(8);
          foundMark = valueString.substr(valueString.length - 4);
          if (foundMark == myMark) {
            return true;
          }
        }
      }
      return false;
    }
    return markFunction;
  }

  var btc_addObservedByMark = function(address, mark, minimumDate) {
    minimumDate = (typeof(minimumDate) === "undefined") ? new Date(0) : minimumDate;
    mark_fun = btc_getMarkFunction(address, mark);
    btc_addObservedAddress(address, mark_fun, minimumDate);
  }

  var btc_getResults = function() {
    return btc_observedAddresses;
  }

  global.btcMonitor = function () {

    return {
      addObservedAddress: btc_addObservedAddress,
      addObservedByMark: btc_addObservedByMark,
      getResults: btc_getResults,
      run: btc_run,
      stop: btc_stop,
    };
  }
})();
