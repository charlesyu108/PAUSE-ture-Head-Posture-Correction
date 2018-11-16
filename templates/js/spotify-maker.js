var SpotifyWebPlayback = (function ($, w) {
  $SCRIPT_ROOT = {{request.script_root|tojson|safe}}

  async function spotifyGetAccessToken() {
    var deferred_token = $.Deferred();
    $.ajax({
      url: $SCRIPT_ROOT + '{{ url_for("spotifyGetAccessToken") }}',
      type: 'GET',
      success: response => {
        console.log(response["access_token"]);
        deferred_token.resolve(response["access_token"]);
      },
      error: err => {
        console.log("Error!", err);
        deferred_token.resolve("Error!");
      }
    });
    return deferred_token;
  }

  async function spotifyOAuth() {
    var deferred_token = $.Deferred();
    var oauth_popup = window.open("", "_blank", "");
    $.ajax({
      url: $SCRIPT_ROOT + '{{ url_for("authSpotify") }}',
      type: 'GET',
      success: response => {
          oauth_popup.location.href = response["auth_url"];
        },
      error: err => {
        console.log("Error!", err);
      }
    });
    // On close of OAuth popup, resolve with the fetched token
    $(oauth_popup).on("unload", () => {
      deferred_token.resolve(spotifyGetAccessToken());
    });
    return deferred_token;
  }


  async function createPlayer() {
    var deferred_player = $.Deferred();
    spotifyOAuth().then(token => {
      const player = new Spotify.Player({
        name: 'PAUSE-ture Head Posture Correction',
        getOAuthToken: cb => { cb(token); }
      });
      // Error handling
      player.addListener('initialization_error', ({ message }) => { console.error(message); });
      player.addListener('authentication_error', ({ message }) => { console.error(message); });
      player.addListener('account_error', ({ message }) => { console.error(message); });
      player.addListener('playback_error', ({ message }) => { console.error(message); });
      // Playback status updates
      player.addListener('player_state_changed', state => { console.log(state); });
      // Ready
      player.addListener('ready', ({ device_id }) => {
        console.log('Ready with Device ID', device_id);
      });
      // Not Ready
      player.addListener('not_ready', ({ device_id }) => {
        console.log('Device ID has gone offline', device_id);
      });
      deferred_player.resolve(player);
    });
    return deferred_player;
  }

  return {
    "createPlayer" : createPlayer
  }

}(jQuery, window));
