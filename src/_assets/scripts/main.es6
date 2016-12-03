//= require communication
//= require tic-tac-toe

$(document).ready(() => {
  Communicaton.init();
  TicTacToe.changePlayer(TicTacToe.currentPlayer);
})
