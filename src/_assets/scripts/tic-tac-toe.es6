const TicTacToe = {
  status: "         ",
  currentPlayer: "x",
  spectators: 0,
  winner: false,

  changePlayer: (player) => {
    if (TicTacToe.winner)
      return

    TicTacToe.currentPlayer = player;
    $('.subtitle').html('player: ' + (player == 'x' ? '<strong>Iron Man</strong> (X)' : '<strong>Captain America</strong> (O)'));
  },

  changeSpectators: (spectators) => {
    TicTacToe.spectators = spectators;
    $('.spectators').html('spectators: ' + spectators);
  },

  update: (pixels) => {
    console.log(pixels.indexOf('x'), pixels.indexOf('o'))
    if (pixels.indexOf('x') == -1 && pixels.indexOf('o') == -1)
      TicTacToe.winner = false

    if (TicTacToe.winner)
      return

    TicTacToe.status = pixels;
    for (var i = 0; i < pixels.length; i++) {
      TicTacToe.setPixel(i + 1, pixels[i]);
    }

    TicTacToe.setWinner();
  },

  setPixel: (index, player) => {
    let cl = TicTacToe.classFromPlayer(player);
    if (cl) {
      $('.pixel-' + index).html('<div class="' + cl + '"></div>');
    } else {
      $('.pixel-' + index).empty();
    }
  },

  setWinner: () => {
    let winner = TicTacToe.state();
    if (!winner.length) {
      $('.pixel').removeClass('winner');
      return;
    }

    TicTacToe.winner = true;

    $('.subtitle').html('winner: ' + (winner[0] == 'x' ? '<strong>Iron Man</strong> (X)' : '<strong>Captain America</strong> (O)'));

    for (var i = 1; i < winner.length; i++) {
      $('.pixel-' + (winner[i] + 1)).addClass('winner');
    }
  },

  classFromPlayer: (player) => {
    switch (player) {
      case "x":
        return "cross";
      case "o":
        return "circle";
      default:
        return ""
    }
  },


  state: () => {
    let polje = TicTacToe.status;
    for (var i = 0; i < 3; i++) {
      if (polje[i] != " ") {
        if (polje[i] == polje[i + 3] && polje[i + 3] == polje[i + 6]) {
          return [polje[i], i, i + 3, i + 6];
        }
      }

      if (polje[3 * i] != " ") {
        if (polje[3 * i] == polje[3 * i + 1] && polje[3 * i + 1] == polje[3 * i + 2]) {
          return [polje[3 * i], 3 * i, 3 * i + 1, 3 * i + 2];
        }
      }
    }

    if (polje[0] != " ") {
      if (polje[0] == polje[4] && polje[4] == polje[8]) {
        return [polje[0], 0, 4, 8];
      }
    }

    if (polje[2] != " ") {
      if (polje[2] == polje[4] && polje[4] == polje[6]) {
        return [polje[2], 2, 4, 6];
      }
    }

    return [];
  }
};
