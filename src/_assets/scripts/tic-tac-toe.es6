const TicTacToe = {
  currentPlayer: "x",

  changePlayer: (player) => {
    TicTacToe.currentPlayer = player;
  },

  update: (pixels) => {
    for (var i = 0; i < pixels.length; i++) {
      TicTacToe.setPixel(i + 1, pixels[i]);
    }
  },

  setPixel: (index, player) => {
    let cl = TicTacToe.classFromPlayer(player);
    if (cl) {
      $('.pixel-' + index).html('<div class="' + cl + '"></div>');
    } else {
      $('.pixel-' + index).empty();
    }
  },

  classFromPlayer: (player) => {
    switch(player) {
      case "x":
        return "cross";
      case "o":
        return "circle";
      default:
        return ""
    }
  }
};
