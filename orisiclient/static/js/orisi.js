(function(){
  var global = this;

  var orisi_waitingRequests = new Array();
  var orisi_contracts = {};
  var orisi_seenMessages = {};
  var orisi_apiInterval = 300; // miliseconds before sending another request
  var orisi_throttleIntervalId = null;

  var orisi_statcastInterval = 1000;
  var orisi_statcastIntervalId = null;

  var orisi_throttle = function() {
    if (orisi_waitingRequests.length == 0) {
      return;
    }

    request = orisi_waitingRequests.shift();
    $.ajax(request);
  }

  var orisi_filterMessages = function(results) {
    var interestingMessages = new Array();

    for (var i=0; i<results.length; ++i) {
      result = results[i];



      if (result['contract_id'] in orisi_contracts) {
        interestingMessages.push(result);
      }


    }

    return interestingMessages;
  }

  var orisi_parseMessages = function(data) {
    var interestingMessages = orisi_filterMessages(data['results']);

    // For now - just add those messages to parse
    for (var i = 0; i < interestingMessages.length; ++i) {
      message = interestingMessages[i];
      if (message['message_id'] in orisi_seenMessages) {
        continue;
      }
      orisi_seenMessages[message['message_id']] = true;
      orisi_contracts[message['contract_id']].push(message);
    }
  }

  var orisi_statcast = function() {
    orisi_waitingRequests.push({
      dataType: 'json',
      url: 'http://hub.orisi.org:81',
      data: {format:'json',cors:true},
      crossDomain:true,
      success: orisi_parseMessages,
    });
  }

  var orisi_run = function() {
    if (!orisi_throttleIntervalId) {
      orisi_throttleIntervalId = setInterval(orisi_throttle, orisi_apiInterval);
    }
    if (!orisi_statcastIntervalId) {
      orisi_statcastIntervalId = setInterval(orisi_statcast, orisi_statcastInterval);
    }
  }

  var orisi_stop = function() {
    if (orisi_throttleIntervalId) {
      clearInterval(orisi_throttleIntervalId);
      orisi_throttleIntervalId = null;
    }
    if (orisi_statcastIntervalId) {
      clearInterval(orisi_statcastIntervalId);
      orisi_statcastIntervalId = null;
    }
  }

  var orisi_addContract = function(contract) {
    orisi_contracts[contract] = new Array();
  }

  var orisi_getResults = function(){
    return orisi_contracts;
  }

  global.orisiMonitor = function () {
    return {
      run: orisi_run,
      stop: orisi_stop,
      addContract: orisi_addContract,
      getResults: orisi_getResults,
    };
  }
})();
