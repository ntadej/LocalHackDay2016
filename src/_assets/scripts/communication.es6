const Communicaton = {
  init: () => {
    var eventOutputContainer = document.getElementById("event");
    var evtSrc = new EventSource("http://127.0.0.1:5000/subscribe");

    evtSrc.onmessage = function(e) {
        console.log(e.data);
        eventOutputContainer.innerHTML = e.data;
    };
  }
}
