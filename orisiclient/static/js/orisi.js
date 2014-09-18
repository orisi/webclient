(function(){
  var global = this;

  var orisi_waitingRequests = new Array();
  var orisi_apiInterval = 300; // miliseconds before sending another request
  var orisi_throttleIntervalId = null;

  var orisi_throttle = function() {
    if (orisi_waitingRequests.length == 0) {
      return;
    }

    request = orisi_waitingRequests.shift();
    $.ajax(request);
  }

  var orisi_run = function() {
    if (!orisi_throttleIntervalId) {
      orisi_throttleIntervalId = setInterval(orisi_throttle, orisi_apiInterval);
    }
  }

  var orisi_stop = function() {
    if (orisi_throttleIntervalId) {
      clearInterval(orisi_throttleIntervalId);
      orisi_throttleIntervalId = null;
    }
  }

  global.orisiMonitor = function () {
    return {
      run: orisi_run,
      stop: orisi_stop,
    };
  }
})();
