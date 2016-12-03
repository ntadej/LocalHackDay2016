const Communicaton = {
  init: () => {
    const evtSrc = new EventSource("http://stark.pyphy.com/server/subscribe");

    evtSrc.onmessage = (e) => {
        console.log(e.data);

        if (e.data == "x" || e.data == "o") {
          TicTacToe.changePlayer(e.data);
        } else {
          TicTacToe.update(e.data);
        }
    };
  }
};
