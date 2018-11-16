var SensorReader = (function ($, w) {

  var isActive = false;
  var controls = {};
  //`sensor_read_action(resp, controls)` dictates an action to take on sensor read.
  // By default: No-op
  var sensor_read_action = (resp, controls) => {console.log(resp)};

  /**
   * Helper function to sleep for some number of ms.
   */
  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  };

  /**
   * Make a request to server for sensor read data.
   * @returns Promise
   */
  function sensor_read_deferred() {
    var deferred = $.Deferred();
    $.ajax({
      url: $SCRIPT_ROOT + '{{url_for("getSensorData")}}',
      type: 'GET',
      success: response => {
          deferred.resolve(response);
        },
      error: err => {
        console.log("Error!", err);
      }
    });
    return deferred;
  };

  /**
   * Recursively make continuous requests to get sensor data.
   */
  async function sensor_read_loop() {
    if (isActive) {
      sensor_read_deferred().then(resp => {
        // Process read response & process here
        sensor_read_action(resp, controls);
      });
    }
    await sleep(1000);
    sensor_read_loop();
  };

  // This is always looping (start and stop denote whether the action should be active)
  sensor_read_loop();

  return {
    "setAction" : (f) => {sensor_read_action = f; return true;},
    "setControls" : (c) => {controls = c; return true;},
    "start" : () => {isActive = true; return true;},
    "stop" : () => {isActive = false; return false;},
    "isRunning" : () => {return isActive;}
  }
}(jQuery, window))
